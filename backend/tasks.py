from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery.schedules import crontab
from celery import Celery
import requests
import smtplib
import sqlite3
import csv
import os


google_chat_webhook_url = os.environ['GOOGLE_CHAT_ID']
app = Celery('tasks', broker='redis://localhost:6379')
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=16, minute=10),
        send_daily_reminder.s(),
        name="Daily Reminders"
    )

    sender.add_periodic_task(
        # crontab(day_of_month=1, hour=0, minute=0),
        crontab(hour=12, minute=30),
        send_email.s(),
        name="Scheduled Monthly Report Email"
    )


@app.task
def send_daily_reminder():

    response = requests.get("http://127.0.0.1:5000/api/visited_status")
    user_names = response.json()

    if user_names == []:
        pass

    else:
        for user_name in user_names:
            message = f"Hey, {user_name}! Don't forget to buy something today."
            send_message_to_google_chat(message)


@app.task
def send_email():

    sender = '21f1005945@ds.study.iitm.ac.in'
    receiver = 'menonaishwarya1101@gmail.com'
    subject = 'GrocerEase - Monthly Report'
    message = 'This is a monthly report generated by the GrocerEase Application at the backend.'
    attachment = 'monthly_report.pdf'

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    # Add attachment
    filename = attachment
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition',
                              'attachment', filename=filename)
        msg.attach(attachment)

    # Set up the SMTP Server and send the email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender
    smtp_password = os.environ['SMTP_PASSWORD']

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())

    return "Email Sent!"


@app.task
def export_product_data_to_csv(file_path):

    # Connect to the SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLITE_DB_DIR = os.path.join(basedir, "./instance")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(SQLITE_DB_DIR, "store.db")
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_URI)

    cursor = conn.cursor()

    # Fetch data from the Product table
    cursor.execute(
        "SELECT p.product_id, c.name, p.product_name, p.price FROM product p JOIN category c ON p.category_id = c.category_id")
    product_data = cursor.fetchall()

    # Define CSV header
    header = ['Product ID', 'Category Name',
              'Product Name', 'Price']

    # Write data to CSV file
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(product_data)

    # Close the database connection
    conn.close()



def send_message_to_google_chat(message):
    try:
        response = requests.post(
            google_chat_webhook_url, json={"text": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Google Chat: {e}")

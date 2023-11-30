from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from models import Order, OrderItem, Product, Category, db
from reportlab.lib.pagesizes import letter
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from sqlalchemy import func
import os


basedir = os.path.abspath(os.path.dirname(__file__))

def generate_pdf_report():
    # Calculate start and end date of the current month
    today = datetime.today()
    start_date = today.replace(day=1)
    end_date = (today + timedelta(days=32 - today.day)).replace(day=1) - timedelta(days=1)

    # 1. Top 5 selling products (quantity-wise)
    top_selling_products = (
        db.session.query(Product.product_name, func.sum(OrderItem.quantity).label('total_sold'))
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.order_id)
        .filter(Order.order_date.between(start_date, end_date))
        .group_by(Product.product_id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    # 2. Least 5 selling products
    least_selling_products = (
        db.session.query(Product.product_name, func.sum(OrderItem.quantity).label('total_sold'))
        .join(OrderItem, Product.product_id == OrderItem.product_id)
        .join(Order, OrderItem.order_id == Order.order_id)
        .filter(Order.order_date.between(start_date, end_date))
        .group_by(Product.product_id)
        .order_by(func.sum(OrderItem.quantity))
        .limit(5)
        .all()
    )

    # 3. Out of stock items (stock = 0)
    out_of_stock_items = Product.query.filter_by(stock=0).all()

    # 4. Limited in stock items (stock <= 10)
    limited_stock_items = Product.query.filter(Product.stock <= 10).filter(Product.stock > 0).all()

    # 5. Profit compared to last month
    last_month_start = start_date - timedelta(days=start_date.day)
    last_month_end = start_date - timedelta(days=1)
    profit_last_month = (
        db.session.query(func.sum(OrderItem.total_price).label('total_profit'))
        .select_from(OrderItem)
        .join(Order, Order.order_id == OrderItem.order_id)
        .filter(Order.order_date.between(last_month_start, last_month_end))
        .scalar() or 0
    )

    # 6. Total items sold this month
    total_items_sold_this_month = (
        db.session.query(func.sum(OrderItem.quantity).label('total_items_sold'))
        .select_from(OrderItem)
        .join(Order, Order.order_id == OrderItem.order_id)
        .filter(Order.order_date.between(start_date, end_date))
        .scalar() or 0
    )

    # Print statements for debugging
    print(f"Today: {today}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Profit Last Month: {profit_last_month}")
    print(f"Total Items Sold This Month: {total_items_sold_this_month}")


    # Save the PDF to a file
    file_path = os.path.join(basedir, 'monthly_report.pdf')
    
    # Create a PDF document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Define custom styles for title and report period
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=12
    )

    period_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=6,
        textColor='#02367b',  # Change the color as needed
        alignment=1
    )

    # Content to be added to the PDF
    content = []

    # Define the background color
    background_color = "#c1e1c1"
    
    # Add a colored rectangle as the background
    content.append(canvas.Canvas(file_path, pagesize=letter).setFillColor(background_color))

    # Add title and report period with custom styles
    title = Paragraph("Monthly Grocery Store Report", title_style)
    period = Paragraph(
        f"Report Period: {start_date.strftime('%B %Y')}",
        period_style
    )
    content.extend([title, period, Spacer(1, 20)])

    # Create a data table for Top 5 Selling Products
    top_selling_title = Paragraph("1. Top 5 Selling Products", styles['Heading2'])
    content.extend([top_selling_title])

    top_selling_data = [
        ["Product", "Quantity"]
    ]
    top_selling_data.extend([(product, str(quantity) + " units") for product, quantity in top_selling_products])

    top_selling_table = Table(top_selling_data, colWidths=[100, 100])
    top_selling_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([top_selling_table, Spacer(1, 20)])

    # Create a data table for Least 5 Selling Products
    least_selling_title = Paragraph("2. Least 5 Selling Products", styles['Heading2'])
    content.extend([least_selling_title])

    least_selling_data = [
        ["Product", "Quantity"]
    ]
    least_selling_data.extend([(product, str(quantity) + " units") for product, quantity in least_selling_products])

    least_selling_table = Table(least_selling_data, colWidths=[100, 100])
    least_selling_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([least_selling_table, Spacer(1, 20)])

     # Create a data table for Out of Stock Items
    out_of_stock_title = Paragraph("3. Out of Stock Items", styles['Heading2'])
    content.extend([out_of_stock_title])

    out_of_stock_data = [
        ["Product"]
    ]
    out_of_stock_data.extend([(product.product_name,) for product in out_of_stock_items])

    out_of_stock_table = Table(out_of_stock_data, colWidths=[100])
    out_of_stock_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([out_of_stock_table, Spacer(1, 20)])

    # Create a data table for Limited in Stock Items
    limited_stock_title = Paragraph("4. Limited in Stock Items", styles['Heading2'])
    content.extend([limited_stock_title])

    limited_stock_data = [
        ["Product", "Stock"]
    ]
    limited_stock_data.extend([(product.product_name, f"Stock: {product.stock}") for product in limited_stock_items])

    limited_stock_table = Table(limited_stock_data, colWidths=[100, 100])
    limited_stock_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([limited_stock_table, Spacer(1, 20)])

    # Create a data table for Profit compared to last month
    profit_last_month_title = Paragraph("5. Profit Compared to Last Month", styles['Heading2'])
    content.extend([profit_last_month_title])

    # Format profit_last_month as a string with a dollar sign and two decimal places
    formatted_profit_last_month = "${:.2f}".format(profit_last_month)

    profit_last_month_data = [
        ["Total Profit"],
        [formatted_profit_last_month]
    ]

    profit_last_month_table = Table(profit_last_month_data, colWidths=[100])
    profit_last_month_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([profit_last_month_table, Spacer(1, 20)])

    # Create a data table for Total items sold this month
    total_items_sold_title = Paragraph("6. Total Items Sold This Month", styles['Heading2'])
    content.extend([total_items_sold_title])

    total_items_sold_data = [
        ["Total Items Sold"]
    ]
    total_items_sold_data.extend([[total_items_sold_this_month]])

    total_items_sold_table = Table(total_items_sold_data, colWidths=[100])
    total_items_sold_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#457e96'),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),  # Header text color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('GRID', (0, 0), (-1, -1), 1, background_color),  # Table grid lines
        ('BACKGROUND', (0, 1), (-1, -1), background_color),  # Table body background color
        ('GRID', (0, 1), (-1, -1), 1, 'white'),  # Table body grid lines
    ]))
    content.extend([total_items_sold_table, Spacer(1, 20)])

    # Build the PDF document
    doc.build(content)

    return file_path

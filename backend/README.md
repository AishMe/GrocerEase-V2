# BACKEND


<!-- ## Setup and Run Guide -->

This guide will walk you through the steps to set up and run the GrocerEase web app on your local machine.

> [!IMPORTANT]  
> Open a web browser and go to ```http://127.0.0.1:5000``` to access the APIs.

<br/>

## Prerequisites

Make sure you have the following software installed:

- ```Python 3.x```
- ```venv```(virtual environment) package (usually included with Python)
- Redis server (install with ```brew install redis```)

<br/>

## Installation and Setup

1. Clone the repository to your local machine:
```console
git clone https://github.com/AishMe/GrocerEase-V2.git
cd backend
```

2. Create a virtual environment and activate it:
```console
python3 -m venv .env
source .env/bin/activate
```

3. Upgrade pip and install required Python libraries:
```console
pip install --upgrade pip
pip install -r requirements.txt
```

4. In the .env folder, go to the activate file, and set the following variables:
```console
export GOOGLE_CHAT_ID="Enter_the_id_here"
export SMTP_PASSWORD='enter_the_password_here'
```

5. Start the Redis server in the background (in a new terminal):
```console
brew services start redis
```

> [!TIP]
> To confirm if Redis server is working, type:\
```redis-cli ping. ```\
\
> If it replies with ```PONG```, the server is running.

<br/>

## Running the App

1. Navigate to the project directory if you're not already there:
```console
cd backend
```

2. Activate the virtual environment:
```console
source .env/bin/activate
```

3. Set the environment variable for development mode (optional but recommended):
```console
export ENV=development
```

4. Run the GrocerEase app:
```console
python3 app.py
```

5. Start Celery for batch jobs (in separate terminals):
```console
celery -A tasks beat --loglevel=info
celery -A tasks worker --loglevel=info -P eventlet
```

   
6. When you're done using the app, deactivate the virtual environment:
```console
deactivate
```

<br/>

> [!NOTE]
> If you encounter any issues, make sure you have followed all the steps correctly and have the necessary prerequisites installed.
> Remember to activate the virtual environment every time you run the app.
> You can customize the environment variable and other settings as needed.

<br/>

## Demo (Video):

[![GrocerEase Demo](./LogoPlay.png)](https://drive.google.com/file/d/1yrhvZo5FB9l6-yUVlrwpFkLLTofX75mN/view?usp=share_link)
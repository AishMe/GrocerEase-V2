# BACKEND

## Setup and Run Guide

This guide will walk you through the steps to set up and run the GrocerEase web app on your local machine.

## Prerequisites

Make sure you have the following software installed:

```Python 3.x```
```venv```(virtual environment) package (usually included with Python)

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

4. Deactivate the virtual environment:
```console
deactivate
```

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

5. Open a web browser and go to ```http://localhost:5000``` to access the app.
6. When you're done using the app, deactivate the virtual environment:
```console
deactivate
```

## Important Notes

If you encounter any issues, make sure you have followed all the steps correctly and have the necessary prerequisites installed.
Remember to activate the virtual environment every time you run the app.
You can customize the environment variable and other settings as needed.


**Video Demo**: [here](https://drive.google.com/file/d/13PUZ6_JXlm96J3UgIaJF8srtpjQHuTUW/view?usp=sharing)
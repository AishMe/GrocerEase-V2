#! /bin/sh
echo "=================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can re-run this without any issues."
echo "------------------------------------------------------------------"

# Create a virtual environment and activate it

if [ -d ".env" ];
then 
	echo ".env folder exists. Installing using pip"
else
	echo "creating .env and install using pip"
	python3 -m venv .env
fi

# Activate virtual env
source .env/bin/activate


# Upgrade pip and install required Python libraries
pip install --upgrade pip
pip install -r requirements.txt

# Set the necessary environment variables in the activate file
echo 'export GOOGLE_CHAT_ID="Enter_the_id_here"' >> .env/bin/activate
echo "export SMTP_PASSWORD='enter_the_password_here'" >> .env/bin/activate

# Work done. So deactivate the virtual env
deactivate

# Start the Redis server in the background
brew services start redis



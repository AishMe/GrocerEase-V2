#! /bin/sh
echo "=================================================================="
echo "Welcome to the setup. This will setup the local virtual env."
echo "And then it will install all the required python libraries."
echo "You can re-run this without any issues."
echo "------------------------------------------------------------------"

if [ -d ".env" ];
then 
	echo "Enabling virtual env"
else
	echo "No virtual env. Please run setup.sh first"
	exit N
fi

# Activate virtual env
source .env/bin/activate

export ENV=development

# Run the GrocerEase app
python3 app.py &

# Start Celery for batch jobs in the background
celery -A tasks beat --loglevel=info &
celery -A tasks worker --loglevel=info -P eventlet &

echo "The GrocerEase app is running."

# Work done. So deactivate the virtual env
deactivate


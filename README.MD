# Pinpoint Webhook Verification Example

This is a simple flask app that demonstrates how to correcly implement webhook signing validation

## Set Up
* Within a working directory create a python virtual env by running `python3 -m venv .venv`
* activate the virual envrionment: `source .venv/bin/activate`
* install requirements: `pip3 install -r requirements.txt`
* create a `.env` file in root of directory that contains: `SIGNING_SECRET="YOUR_SIGNING_SECRET"`

## Usage
* In the command line make sure the virtual environment is acivated and run: `gunicorn -w 4 'main:app'`
* visit `localhost:8000` in your browser and you should see a Hello World index page which means the flask app is running correctly
* You can then use ngrok to expose port 8000 to external traffic: `ngrok http 8000`
* Set up a webhook in Pinpoint using the URL: `https://<random_ngrok_id>.ngrok-free.app/webhook/<client_name>`
* Update the signig secret env variable in `.env`
* Test the webhook in Pinpoint (scroll to the bottom of the webhook page)



# Webhook Testing App

This is a simple flask app that demonstrates how to correcly implement webhook signing validation

## Set Up
* Within a working directory create a python virtual env by running `python3 -m venv .venv`
* activate the virual envrionment: `source .venv/bin/activate`
* install requirements: `pip3 install -r requirements.txt`
* create a `.env` file in root of directory that contains: `SIGNING_SECRET="YOUR_SIGNING_SECRET"`

## Usage
* In the command line make sure the virtual environment is acivated and run: `gunicorn -w 4 'main:app'`
* visit `localhost:8000` in your browser and you should see a `Hello from Pinpoint Webhook testing` index page which means the flask app is running correctly
* You can then use ngrok to expose port 8000 to external traffic: `ngrok http 8000`
* Set up a webhook in Pinpoint using the one of the below URLs: 
1. `https://<random_ngrok_id>.ngrok-free.app/signed_webhook/<client_name>` - use if testing signing
2. `https://<random_ngrok_id>.ngrok-free.app/unsigned_webhook/<client_name>` - use if just testing genrally
* Update the signig secret env variable in `.env` if testing signing of webhooks
* Test the webhook in Pinpoint (scroll to the bottom of the webhook page)

**If you already have ngrok and Gunicorn installed**
run: `python3 main.py` - this will run both the gunicorn command and ngrok command

**If you have a custom ngrok domain**
Add your domain as an env variable - `NGROK_URL="my-random-domain.ngrok.app"`. This has the nice advantage of not having to update webhooks when every time you exit the ngrok service

A file called `app.log` will be created on fisrt load of flask and this will also contain additional confirmation and time stamps of the status of webhook validations



# COINAPP core

This app make simple to buy airtime with your favourite crypto currency, and dose an immediate conversion to fiat with best rates to lock in profit and avoid loss.

## Features

Coin app core features include:

- Convert crypto to fiat instantly
- Give proper profitable estimate when converting fiat to crypto
- Recieve webhook events on transaction executed.
- Fetch all processed transactions with automatic profit calculations

## Installation

- `git clone <this_url> && cd <repo_name>`
- Run `pipenv install`
- Configure Server
    - Create `.env`
    - Update `.env` with the current attributes
        - `DATABASE_NAME = <DATABASE_NAME>` your prefered database name
        - `DATABASE_USER = <DATABASE_USER>` your user config for your prefered database
        - `DATABASE_PASSWORD = <DATABASE_PASSWORD>` your database password
        - `DATABASE_ENGINE = <DATABASE_ENGINE>`your prefered database engine
        - `DATABASE_HOST = <DATABASE_HOST>` your database host
        - `DATABASE_PORT = <DATABASE_PORT>` your database port
        - `PROJECT_SECRET_KEY = <PROJECT_SECRET_KEY>` your project secret key
        - `BILL_PROVIDER_SECRET_KEY = <BILL_PROVIDER_SECRET_KEY>` your bill provider api key
        - `CRYPTO_PROVIDER_SECRET_KEY = <CRYPTO_PROVIDER_SECRET_KEY>` your quidax api key
        - `CLOUDINARY_API_KEY = <CLOUDINARY_API_KEY>` string must be 16 in length
        - `CLOUDINARY_API_SECRET = <CLOUDINARY_API_SECRET>`
        - `CLOUD_NAME = <CLOUD_NAME>`
        - `WEBHOOK_SECRET = <WEBHOOK_SECRET>`
- Run the app locally `python manage.py runserver`
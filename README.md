# wStocks (Watch Stocks)

It keeps you informed about your stocks prices (Sending emails when stocks go above or under a expected value). It works with Brazilian Stocks.

## Instalation
 - Clone this repo:

        $ git clone https://github.com/engleovictor/wStocks

        $ cd wStocks

 - Install requiriments.txt

        $ pip install -r requiriments.txt -v

 - Make Django migrations

        $ python3 manage.py makemigrations

        $ python3 manage.py migrate

 - Change api_key

        {
            "api_key": "YOUR_API_KEY_HERE"
        }

    get your [api_key here](https://fcsapi.com/)

 - Change email_data

        {
            "sender_email": "FROM_EMAIL",   # You will receive information updates from this email address
            "sender_password" : "PASSWORD" # You must generate a new password (when using gmail)
        }

 - Finally:

        $ python3 manage.py runserver

Acess the web page in http://127.0.0.1:8000 (Or any one you have configured :smile:)
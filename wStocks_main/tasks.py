import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_stock_price(ticker: str) -> float:
    with open('api_key', 'r') as api_key_json:
        apikey = json.load(api_key_json)['apikey']    
    
    params = {
        "access_key": apikey,
        "symbol": ticker
    }

    response = requests.get(url="https://fcsapi.com/api-v3/stock/latest", params=params)

    if response.status_code == 200:
        return float(response.json()['response'][0]["c"])
    else:
        return "error"


def send_email(to_data: dict):
    with open('email_data', 'r') as root_email_data:
        root_data = json.load(root_email_data)

    message = MIMEMultipart()
    message["From"] = root_data['sender_email']
    message["To"] = to_data['To']
    message["Subject"] = to_data['subject']
    message.attach(MIMEText(to_data['body'], "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(root_data['sender_email'], root_data['sender_password'])
        smtp_server.send_message(message)


# to_data -> To, subject, body

def get_to_data(to_email: str, ticker: str, action: bool) -> dict:
    # True -> BUY, False -> SELL
    to_data = {}

    if action:
        delta = 'caindo'
        act = 'comprar'
        absolute = 'abaixo'

    else:
        delta = 'subindo'
        act = 'vender'
        absolute = 'acima'


    to_data['To'] = to_email
    to_data['subject'] = f"Preço de {ticker} está {delta}!"
    to_data['body'] = f"Recomendamos {act} {ticker}, preço {delta} {absolute} do estabelecido."

    return to_data

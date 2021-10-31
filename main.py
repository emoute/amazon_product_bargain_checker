from bs4 import BeautifulSoup
from os import environ
from smtplib import SMTP
import requests

sender_email = environ.get('SENDER_EMAIL')
sender_password = environ.get('SENDER_PASSWORD')
receiver_email = environ.get('RECEIVER_EMAIL')
user_agent = environ.get('USER_AGENT')

amazon_product_url = 'https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07CRG94G3/?th=1'
headers = {
    'User-Agent': user_agent,
    'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
}

response = requests.get(url=amazon_product_url, headers=headers).text

soup = BeautifulSoup(response, 'lxml')
product_price_text = soup.find(id='priceblock_ourprice').get_text()
# Converting price to float number and remove currency sign
product_price = float(product_price_text.removeprefix('$'))
# Fix '\u2013' character error in product title
title = soup.find(id='productTitle').get_text().strip()
title = title.replace('\u2013', '')

# Checking if price is less than 50$ US than send a message
if product_price < 50:
    message = f'{"-"*100}\n{title}\n{"-"*100}\nis now {product_price}$'
    with SMTP('smtp.gmail.com', port=587) as smtp:
        smtp.starttls()
        result = smtp.login(sender_email, sender_password)
        smtp.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=f'Subject: Bargain on Amazon (Price checker)\n\n{message}\n{amazon_product_url}'
        )

# Python program to scrape website / Price Monitor
# Save the product data and notify the customer if the price is good.
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import smtplib
import time
from random import randint
from IPython.core.display import clear_output


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

url = 'https://www.amazon.com/DJI-Mavic-Air-More-Combo/dp/B086XCGMN7/ref=sr_1_2_sspa?dchild=1&keywords=DJI+Mavic+2+' \
      'Pro&qid=1630533943&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzSEw2VENUQzg4RE84JmVuY3J5cHRlZElkPUEx' \
      'MDEzODQzV0c0OUlVUkdOSUpEJmVuY3J5cHRlZEFkSWQ9QTAzNTIzMDEyS1JQS0VHS0ozN05FJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbG' \
      'lja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

# path to file in the folder
save_data_file = '.../Amazon_Price_Monitoring/PriceHistory.csv'

# Initializing the variables that we'll going to use...
start_time = time.time()
code = 'B086XCGMN7'
Tracking_Price = 98700
requests = 0

# preparation for the email to send
gmail_user = 'exemple@gmail.com'
gmail_password = '*********'
sent_from = gmail_user
to = ['exemple@gmail.com']
subject = 'Buy ' + code + ' !!!'
body = 'Alert!!!,\n The product is bellow ' + str(Tracking_Price) + '$ right now.'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

# We'll going to scrape the data from amazon (price, title of the product, reviews ..)
# The loop is infinite, we break the loop if we get the price we want..
while True:
    date = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    # Request from the server the content of the web page by using get(),
    # and store the server’s response in the variable response
    response = get(url, headers=HEADERS)
    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')

    # get the title of the product
    title = page_html.find("span", class_='a-size-large product-title-word-break').text.strip()

    # the price could be none so we prevent this case
    if page_html.find(id='priceblock_ourprice') is not None:
        price = float(page_html.find("span", class_='a-size-medium a-color-price priceBlockBuyingPriceString').text
                      .replace('.', '').replace('$', '').replace('€', '').replace(',', '.').strip())
    elif page_html.find(id='priceblock_saleprice') is not None:
        # this part gets the price in dollars from amazon.com store
        price = float(page_html.find("span", id='priceblock_saleprice').text.replace('$', '').replace('€', '').replace(
            ',', '').strip())
    else:
        price = None

    # Compiling the product info
    data = [date, code, title, Tracking_Price, price, url]
    Information = pd.DataFrame([data],
                               columns=['date', 'code', 'title', 'tracking price', 'price', 'url'])

    # If the price is good enough we send an email...
    if price is not None and price <= Tracking_Price:
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong….", ex)

    # Pause the loop
    time.sleep(randint(10, 20))

    # Monitor the requests
    requests += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Save the data in each loop...
    previous_data = pd.read_csv(save_data_file)
    all_data = previous_data.append(Information, sort=False)
    all_data.to_csv(save_data_file, index=False)

    # We break the loop if the price is good enough..
    if price is not None and price < Tracking_Price:
        break

print('Finally!!!')

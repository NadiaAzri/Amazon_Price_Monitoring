# Amazon Price Monitoring
Scrap the product data and alert if the price is the tracking one

Language used is Python 3.8. / Pycharm.

This Python program is designed to scrape product information from the Amazon website and monitor the price of a specific product. If the current price falls below a predefined threshold, the program sends an email notification to alert the user.

## Features

- **Web Scraping:** Utilizes the `requests` library to fetch the HTML content of the Amazon product page and `BeautifulSoup` for parsing.

- **Data Storage:** Stores the product information, including date, product code, title, tracking price, current price, and URL, in a CSV file (`PriceHistory.csv`).

- **Email Notification:** Sends an email alert if the current price is below the specified tracking price. Uses the `smtplib` library for SMTP communication.

- **Continuous Monitoring:** The program runs in an infinite loop, periodically checking the product price. The loop is paused for a random time interval between 10 to 20 seconds after each iteration.

## Setup

1. Install the required libraries:

   ```bash
   pip install requests beautifulsoup4 pandas
   ```

2. Update the following variables in the script:

   - `url`: The URL of the Amazon product page.
   - `save_data_file`: The path to the CSV file for storing price history.
   - `code`: Product code.
   - `Tracking_Price`: The desired price threshold for triggering an email alert.
   - `gmail_user`: Your Gmail email address.
   - `gmail_password`: Your Gmail account password.
   - `to`: Email addresses to receive notifications.

3. Run the script:

   ```bash
   python your_script_name.py
   ```

## Notes

- Make sure to keep your Gmail credentials secure and consider using an application-specific password for enhanced security.
- Adjust the monitoring frequency and other parameters according to your preferences.

Feel free to customize the script further based on your needs and preferences. Happy monitoring!


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

url = "https://www.google.com/finance/quote/USD-LKR"



# CRITICAL STEP: Add headers to avoid being blocked
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}



def get_live_rate():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_div = soup.find("div", class_="YMlKec fxKbKc")

    if price_div:
        return float(price_div.text.replace(',', ''))
    return None



# Get current rate and time

current_rate = get_live_rate()
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



if current_rate:

    # Prepare data for CSV
    new_entry = pd.DataFrame([[current_time, current_rate]], columns=["Timestamp", "USD_to_LKR"])

    file_exists = os.path.isfile("currency_history.csv")
    new_entry.to_csv("currency_history.csv", mode='a', index=False, header=not file_exists)

    print(f"Success! Saved Rate: {current_rate} at {current_time}") 
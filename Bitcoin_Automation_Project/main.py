import requests
import json
import time
import pytz
import logging
from datetime import datetime
from pathlib import Path
from Price_Graph import generate_graph
from Send_Mail import send_email

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API endpoint to retrieve the current Bitcoin price in USD from Coinbase.
Base_url = 'https://api.coinbase.com/v2/prices/BTC-USD/spot'
# Specifies the filename where Bitcoin price data will be stored or read from.
json_file = 'btc_prices.json'
# Defines the timezone object for Israel, used to convert datetime values to Israel local time.
israel_tz = pytz.timezone('Asia/Jerusalem')


# Sends a GET request to the provided API URL to fetch the current Bitcoin price.
# If the request is successful, returns the response data as JSON.
# If the request fails, logs the error and returns None.
def get_current_bitcoin_price(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logging.info(f'Successfully fetched data from API: {data}')
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to fetch data from API: {e}')
        return None




# Deletes the old JSON and graph files if they exist.
# Logs each deletion attempt and its result.
# Helps ensure a clean run every time the program starts.
def delete_old_files():
    logging.info('Checking and deleting old JSON and graph files if they exist...')

    if Path(json_file).exists():
        try:
            Path(json_file).unlink()
            logging.info(f'Deleted old JSON file: {json_file}')
        except Exception as e:
            logging.error(f'Failed to delete old JSON file: {e}')

    graph_file = 'btc_price_graph.png'
    if Path(graph_file).exists():
        try:
            Path(graph_file).unlink()
            logging.info(f'Deleted old graph file: {graph_file}')
        except Exception as e:
            logging.error(f'Failed to delete old graph file: {e}')









# Fetches the current Bitcoin price every minute, 60 times total (for 1 hour).
# Each price is saved into a local JSON file with a timestamp (in Israel time).
# Logs success or error messages during the process.
def fetch_bitcoin_prices_for_one_hour():
    logging.info('Starting to fetch Bitcoin prices every minute for the next hour...')
    minute = 0
    while minute < 60:
        logging.info(f'Minute {minute + 1}: Sending request to fetch current Bitcoin price...')
        bitcoin_info = get_current_bitcoin_price(Base_url)

        if bitcoin_info:
            try:
                logging.debug('API response received successfully.')
                if Path(json_file).exists():
                    logging.info('JSON file found, loading existing data...')
                    with open(json_file, 'r') as file:
                        data_to_file = json.load(file)
                else:
                    logging.info('JSON file not found. Starting with a new list...')
                    data_to_file = []

                data_to_file.append({
                    'current_time': datetime.now(israel_tz).isoformat(),
                    'price_usd': bitcoin_info['data']['amount']
                })

                with open(json_file, 'w') as file:
                    json.dump(data_to_file, file, indent=2)

                logging.info(f'{minute + 1} - New data was added to the file successfully')

            except Exception as e:
                logging.error(f'Error writing to file: {e}')
        else:
            logging.warning('The request failed, no new data was saved this time')

        minute += 1
        time.sleep(60)
        logging.info('Finished fetching Bitcoin prices for the past hour.')


# Main entry point
if __name__ == '__main__':
    logging.info('=== Program started ===')
    delete_old_files()
    fetch_bitcoin_prices_for_one_hour()
    max_val, max_time = generate_graph()
    send_email(max_val, max_time)
    logging.info('Program finished successfully.')





import json
import matplotlib.pyplot as plt
import pytz
import logging
from datetime import datetime
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter

# Configures the logging system to display messages with timestamps, severity levels, and the log message itself.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Formats the y-axis price values as currency with commas and no decimal places (e.g., $25,000).
def format_price(y, _):
    return f'${y:,.0f}'


# Loads Bitcoin price data from a JSON file.
# Converts timestamps to the specified timezone and prices to float values.
# Returns two lists: one of datetime objects and one of price values.
def load_data(json_file, timezone):
    logging.info(f'Loading data from JSON file: {json_file}')
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            logging.info(f'Successfully loaded {len(data)} records from {json_file}')


        timestamps = []
        prices = []

        for entry in data:
            time_str = entry['current_time']
            price_str = entry['price_usd']

            time_obj = datetime.fromisoformat(time_str).astimezone(timezone)
            price_float = float(price_str)

            timestamps.append(time_obj)
            prices.append(price_float)

        logging.info('Timestamps and prices successfully parsed.')
        return timestamps, prices

    except FileNotFoundError:
        logging.error(f'File {json_file} not found.')
        return [], []
    except Exception as e:
        logging.error(f'Error loading data: {e}')
        return [], []


# Creates and saves a line graph of Bitcoin prices over time.
# Takes a list of timestamps and corresponding prices.
# Saves the graph as an image file with the given filename.
def create_graph(timestamps, prices, filename,israel_time):
    logging.info('Generating graph for Bitcoin price data...')
    try:
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, prices, marker='o', linestyle='-', color='blue')
        plt.title('Bitcoin Price Over Time (USD)')
        plt.xlabel('Time')
        plt.ylabel('Price (USD)')
        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S', tz=israel_time))
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(format_price))
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        logging.info(f'Graph saved to {filename}')
    except Exception as e:
        logging.error(f'Failed to create graph: {e}')



# Loads Bitcoin price data from a JSON file, creates a graph from the data,
# and returns the maximum price along with the timestamp it occurred.
# If loading fails, returns None, None.
def generate_graph():
    logging.info('Generating graph and extracting maximum Bitcoin price...')
    israel_tz = pytz.timezone('Asia/Jerusalem')
    json_file = 'btc_prices.json'

    timestamps, prices = load_data(json_file, israel_tz)

    if not timestamps or not prices:
        return None, None

    create_graph(timestamps, prices, 'btc_price_graph.png',israel_tz)

    max_price = max(prices)
    max_index = prices.index(max_price)
    max_time = timestamps[max_index]

    logging.info(f"Max price: ${max_price:,.2f} at {max_time.strftime('%Y-%m-%d %H:%M:%S')}")
    return max_price, max_time


# main.py
import pandas as pd
from scraper import load_all_items
from driver_setup import set_up_driver
from utils import load_existing_ids, save_new_ids
from config import SOURCE
import os


def main():
    driver = set_up_driver()  # Initialize the WebDriver
    data = pd.DataFrame()  # Initialize an empty DataFrame

    scraped_ids = load_existing_ids()  # Load already scraped article IDs
    # Start the scraping process
    data = load_all_items(driver, data, scraped_ids)
    # Check if new data was fetched and append it to the existing data
    if not data.empty:
        # Append new data to existing data
        data = pd.concat([data, data], ignore_index=True)
    else:
        print("No new data was scraped.")
    driver.quit()  # Close the WebDriver once scraping is complete

    # Create a 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the data to a CSV file in the 'data' folder
    data.to_csv(os.path.join(
        'data', f'{SOURCE}.csv'), index=False, encoding='utf-8')

    # Save the scraped article IDs
    save_new_ids(scraped_ids)


if __name__ == "__main__":
    main()

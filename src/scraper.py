# scraper.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils import save_new_ids
from config import BASE_URL
from driver_setup import set_up_driver


def load_all_items(driver, data, scraped_ids, max_scrolls=2):
    driver.get(BASE_URL)  # Open the base URL in the browser
    wait = WebDriverWait(driver, 20)  # Define an explicit wait of 20 seconds
    scrolls = 0  # Initialize scroll counter
    last_height = driver.execute_script(
        "return document.body.scrollHeight")  # Get initial page height
    new_ids = []  # List to store new successfully scraped article IDs

    while scrolls < max_scrolls:
        print(f"Processing batch {scrolls + 1}")

        # Extract and process items from the current page
        items = parse_items(driver)
        for item in items:
            # Use article URL as unique ID
            article_id = item.get_attribute("href")

            if article_id in scraped_ids:
                print(f"Article {article_id} already scraped, skipping.")
                continue  # Skip if the article has already been scraped

            sub_data = extract_item_data(item)  # Extract data for each item
            if not sub_data.empty:  # Check if data was successfully extracted
                # Append new data
                data = pd.concat([data, sub_data], ignore_index=True)
                # Add the ID of the successfully scraped article
                new_ids.append(article_id)

        # Scroll to the bottom of the page and wait for new content
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        try:
            # Wait for new items to load (up to 5 seconds)
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.thar')))
        except TimeoutException:
            print("Timeout while waiting for new content to load.")
            break  # Exit the loop if new content doesn't load in time

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # If the height hasn't changed, stop scrolling
            print("No more content to load.")
            break

        last_height = new_height  # Update the page height for the next iteration
        scrolls += 1  # Increment the scroll counter

    save_new_ids(new_ids)  # Save newly scraped article IDs to the JSON file
    return data


def parse_items(driver):
    try:
        items = driver.find_elements(By.CSS_SELECTOR, 'a.thar')
        print(f"Found {len(items)} items")
        return items
    except NoSuchElementException:
        print("No items found on the page.")
        return []


def extract_item_data(item):
    try:
        href = item.get_attribute("href")  # Get the article URL
        title_element = item.find_element(
            By.CSS_SELECTOR, "div.thar__title1")  # Get the title element
        title = title_element.text.strip()  # Extract and clean the title text

        article_text = 'N/A'
        trends_text = 'N/A'

        if href != 'N/A':
            try:
                r = requests.get(href, timeout=10)  # Send HTTP GET request
                r.raise_for_status()  # Raise error if the response is not 200 (OK)
                soup = BeautifulSoup(r.text, 'lxml')

                # Extract the title and references from the article page
                title_element = soup.find(
                    'h2', class_='tha__title2').get_text(strip=True)
                references_element = soup.find('div', class_='tha__references')
                date_element = references_element.find(text=lambda t: '—' in t)
                if date_element:
                    publication_date = date_element.split(
                        '—')[1].strip()  # Extract publication date
                reference_links = references_element.find_all(
                    'a', class_='tha__referenceLink')
                references = [link['href']
                              # Extract reference links
                              for link in reference_links]

                # Extract the main article text
                article_text = soup.find('div', class_='tha__articleText').get_text(
                    separator=' ', strip=True)

                # Extract related trends
                trends = soup.find_all('div', class_='tpt__aItemText')
                if trends:
                    trends_text = ' '.join(
                        [trend.get_text(separator=' ', strip=True) for trend in trends])

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Page not found (404 error): {href}")
                else:
                    print(f"Request error: {e}")
                return pd.DataFrame()  # Return empty DataFrame to continue
            except Exception as e:
                print(f"Error fetching or parsing content: {e}")

        article_details = f"""
        Title: {title_element}
        Date: {date_element}
        References: {references}
        Article Text: {article_text}
        Trend Themes and Industry Implications:
        {trends_text}
        """

        data_row = {
            'source': 'trendhunter',
            'title': title,
            'href': href,
            'article_text': article_details
        }

        # Return the scraped data as a DataFrame
        return pd.DataFrame([[data_row['source'], data_row['title'], data_row['href'], date_element, article_details]],
                            columns=['source', 'title', 'href', 'date_element', 'article_text'])

    except Exception as e:
        print(f"Error extracting data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error

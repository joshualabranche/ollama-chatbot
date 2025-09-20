#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 18:00:57 2025

@author: jlab
"""

import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_nyt_titles():
    """Scrapes article titles from the New York Times website."""
    url = 'https://www.nytimes.com/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all headline elements using regular expression
        headlines = soup.find_all('p', re.compile(r"indicate-hover css-"))

        titles = [headline.text.strip() for headline in headlines]
        titles = titles[0:[i for i, x in enumerate(titles) if x == ''][0]]
        return titles

    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def save_to_csv(titles, filename='nyt_titles.csv'):
    """Saves a list of titles to a CSV file."""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title'])
            for title in titles:
                writer.writerow([title])
            print(f"Titles saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

if __name__ == '__main__':
    titles = scrape_nyt_titles()
    if titles:
        save_to_csv(titles)
        print(titles)
    else:
        print("No titles found.")
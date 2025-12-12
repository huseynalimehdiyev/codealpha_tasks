"""
Web Scraping Project - Books to Scrape
This script scrapes book data from http://books.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin


class BooksScraper:
    def __init__(self, base_url='http://books.toscrape.com'):
        self.base_url = base_url
        self.books_data = []

    def get_page(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_rating(self, rating_class):

        ratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        for key in ratings:
            if key in rating_class:
                return ratings[key]
        return 0

    def scrape_book_details(self, book_url):
        soup = self.get_page(book_url)
        if not soup:
            return {}

        details = {}

        # Extract prod. information table
        table = soup.find('table', class_='table-striped')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                header = row.find('th').text.strip()
                value = row.find('td').text.strip()
                details[header] = value

        # Extract des.
        desc_div = soup.find('div', id='product_description')
        if desc_div:
            desc_p = desc_div.find_next_sibling('p')
            details['Description'] = desc_p.text.strip() if desc_p else 'N/A'
        else:
            details['Description'] = 'N/A'

        return details

    def scrape_books(self, num_pages=5):
        print(f"Starting to scrape {num_pages} pages...")

        for page_num in range(1, num_pages + 1):
            if page_num == 1:
                url = f"{self.base_url}/index.html"
            else:
                url = f"{self.base_url}/catalogue/page-{page_num}.html"

            print(f"Scraping page {page_num}...")
            soup = self.get_page(url)

            if not soup:
                continue

            books = soup.find_all('article', class_='product_pod')

            for book in books:
                book_data = {}

                title_tag = book.find('h3').find('a')
                book_data['Title'] = title_tag['title']

                book_url = urljoin(self.base_url, title_tag['href'])
                book_data['URL'] = book_url

                price_tag = book.find('p', class_='price_color')
                book_data['Price'] = price_tag.text.strip()

                availability = book.find('p', class_='instock availability')
                book_data['Availability'] = availability.text.strip() if availability else 'N/A'

                rating_tag = book.find('p', class_='star-rating')
                book_data['Rating'] = self.extract_rating(rating_tag['class'])

                print(f"  Fetching details for: {book_data['Title'][:50]}...")
                details = self.scrape_book_details(book_url)
                book_data.update(details)

                self.books_data.append(book_data)

                time.sleep(0.5)

            print(f"Page {page_num} completed. Total books: {len(self.books_data)}")
            time.sleep(1)

        print(f"\nScraping completed! Total books scraped: {len(self.books_data)}")

    def save_to_csv(self, filename='books_data.csv'):
        if not self.books_data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.books_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
        print(f"Dataset shape: {df.shape}")
        print(f"\nColumns: {list(df.columns)}")

    def display_summary(self):
        if not self.books_data:
            print("No data scraped yet!")
            return

        df = pd.DataFrame(self.books_data)
        print("\n" + "=" * 60)
        print("SCRAPING SUMMARY")
        print("=" * 60)
        print(f"Total Books Scraped: {len(df)}")
        print(f"\nFirst 5 books:")
        print(df[['Title', 'Price', 'Rating', 'Availability']].head())
        print(f"\nAverage Rating: {df['Rating'].mean():.2f}")
        print(f"Most Common Rating: {df['Rating'].mode()[0]}")


def main():
    scraper = BooksScraper()

    scraper.scrape_books(num_pages=5)

    scraper.display_summary()

    scraper.save_to_csv('books_data.csv')


if __name__ == "__main__":
    main()

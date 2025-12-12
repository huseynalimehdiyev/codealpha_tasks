# Books to Scrape – Web Scraping Project 🕸️📚✨

> "A Python script that quickly collects books!" 

This project scrapes book data from **[Books to Scrape](http://books.toscrape.com)**. It collects key information about each book — from price to rating and description — and saves it into a CSV file.

---

## 🛠️ Features

- 🔹 **Scrape multiple pages** – You can scrape as many pages as you like (controlled by the `num_pages` parameter, default is 5)  
- 🔹 **Extract book details**:
  - 📖 Title  
  - 💰 Price  
  - ✅ Availability  
  - ⭐ Rating  
  - 🗂️ Product info (UPC, Product Type, Tax, Number of reviews, etc.)  
  - 📝 Description  
- 🔹 **CSV export** – Saves all scraped data into `books_data.csv`  
- 🔹 **Summary display** – After scraping, the script shows:  
  - Total books scraped  
  - First 5 books  
  - Average rating  
  - Most common rating  

---

## ⚡ How It Works (Step by Step)

1. **Fetch page** 🌐  
   - Uses `requests` to download the page  
   - Parses HTML with `BeautifulSoup`  

2. **Loop through books** 📚  
   - Finds all books on the page  
   - Extracts title, price, availability, and rating  

3. **Scrape book details** 🕵️‍♂️  
   - Visits each book’s individual page  
   - Extracts product table info and description  
   - Stores data in a Python dictionary  

4. **Append data** 📝  
   - Adds each book’s data to the `books_data` list  
   - Uses `time.sleep()` to avoid overloading the site  

5. **Save to CSV** 💾  
   - Converts data to a Pandas DataFrame  
   - Writes it to `books_data.csv`  

6. **Display summary** 📊  
   - Shows total books, first 5 books, average rating, and most common rating  

---

## 📦 Requirements

- Python 3.x  
- Libraries:
  - `requests`  
  - `beautifulsoup4`  
  - `pandas`  

Install them with pip:

```bash
pip install requests beautifulsoup4 pandas

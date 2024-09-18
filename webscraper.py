import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to make a request and get the HTML content
def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# Function to parse HTML and extract books' data
def parse_books(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all book elements
    book_elements = soup.find_all('article', class_='product_pod')
    print(f"Found {len(book_elements)} book elements.")  # Debug: Check number of book elements
    
    data = []
    for book in book_elements:
        # Extract the title from the title attribute if available
        title_tag = book.find('h3')
        title = title_tag.get('title', 'N/A') if title_tag else 'N/A'
        
        # Extract the price
        price_tag = book.find('p', class_='price_color')
        price = price_tag.text.strip() if price_tag else 'N/A'
        
        # Extract the availability
        availability_tag = book.find('p', class_='availability')
        availability = availability_tag.text.strip() if availability_tag else 'N/A'
        
        # Extract the rating
        rating_tag = book.find('p', class_='star-rating')
        rating = rating_tag.get('class', ['N/A'])[1] if rating_tag else 'N/A'
        
        # Extract the book URL
        link_tag = book.find('h3').find('a')
        book_url = link_tag.get('href', 'N/A') if link_tag else 'N/A'
        
        # Construct the full URL
        full_url = f"http://books.toscrape.com/{book_url}" if book_url != 'N/A' else 'N/A'
        
        data.append({
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'URL': full_url
        })
    
    return data

# Function to store the data in a CSV file
def store_data_csv(data, filename="books_data.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to execute the scraper logic
def scrape_books(url):
    html_content = get_html_content(url)
    if html_content:
        books_data = parse_books(html_content)
        store_data_csv(books_data)

# URL of the target page
url = "http://books.toscrape.com/"
scrape_books(url)

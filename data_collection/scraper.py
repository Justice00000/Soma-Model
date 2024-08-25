import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException for URL: {url} - {e}")
        return None

def parse_scholarships(html):
    soup = BeautifulSoup(html, "html.parser")
    scholarships = []
    
    # Update parsing logic based on the specific structure of the website
    for scholarship_div in soup.select(".scholarship-div"):  # Example selector, change as needed
        title = scholarship_div.select_one(".title").get_text(strip=True) if scholarship_div.select_one(".title") else "N/A"
        amount = scholarship_div.select_one(".amount").get_text(strip=True) if scholarship_div.select_one(".amount") else "N/A"
        deadline = scholarship_div.select_one(".deadline").get_text(strip=True) if scholarship_div.select_one(".deadline") else "N/A"
        
        scholarships.append({
            "title": title,
            "amount": amount,
            "deadline": deadline,
        })
    
    return scholarships

def scrape_scholarships(url):
    logging.info(f"Scraping URL: {url}")
    html = fetch_url(url)
    if html:
        return parse_scholarships(html)
    return []

def scrape_from_multiple_urls(urls):
    all_scholarships = []
    for url in urls:
        scholarships = scrape_scholarships(url)
        all_scholarships.extend(scholarships)
    return all_scholarships

def save_to_csv(scholarships, filename="scholarships.csv"):
    df = pd.DataFrame(scholarships)
    df.to_csv(filename, index=False)
    logging.info(f"Saved data to {filename}")

if __name__ == "__main__":
    urls = [
        "https://www.google.com/",  # Replace with actual URLs
        # Add more URLs if needed
    ]
    
    all_scholarship_data = scrape_from_multiple_urls(urls)
    
    for scholarship in all_scholarship_data:
        print(scholarship)
    
    save_to_csv(all_scholarship_data)
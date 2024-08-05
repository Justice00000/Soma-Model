import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time

# Function to save scholarship data to CSV
def save_to_csv(data):
    with open('scholarships.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Degree', 'Location', 'Funds Needed'])  # Adjust columns as needed
        for row in data:
            writer.writerow(row)

def get_scholarship_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'lxml')
    
    # Placeholder for scraping details - adjust selectors as needed
    degree = soup.find('div', class_='degree').text.strip() if soup.find('div', class_='degree') else 'N/A'
    location = soup.find('div', class_='location').text.strip() if soup.find('div', class_='location') else 'N/A'
    funds = soup.find('div', class_='funds').text.strip() if soup.find('div', class_='funds') else 'N/A'

    return degree, location, funds

def scrape_scholarships(urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    all_scholarship_data = []

    for url in urls:
        try:
            result = requests.get(url, headers=headers)
            result.raise_for_status()  # Raises HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}")
            continue

        print(f"Status Code: {result.status_code}")

        if result.status_code == 200:
            soup = BeautifulSoup(result.content, 'lxml')
            links = soup.find_all("a")

            for link in links:
                href = link.attrs.get('href', '')
                full_url = urljoin(url, href)
                if "Scholarship" in link.text:  # Adjust criteria based on actual content
                    print(f"Title: {link.text}, URL: {full_url}")
                    details = get_scholarship_details(full_url)
                    if details:
                        degree, location, funds = details
                        all_scholarship_data.append([link.text.strip(), full_url, degree, location, funds])
        
        time.sleep(2)  # Delay to avoid being blocked

    save_to_csv(all_scholarship_data)

# Ensure this script can be run independently
if __name__ == "__main__":
    urls = [
        "https://www.scholarshipregion.com/category/scholarships/",
        "https://www.fastweb.com/"
    ]
    scrape_scholarships(urls)
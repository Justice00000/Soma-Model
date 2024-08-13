import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import time

# Function to save scholarship data to CSV
def save_to_csv(data):
    file_exists = False
    try:
        with open('scholarships.csv', 'r', encoding='utf-8') as file:
            file_exists = True
    except FileNotFoundError:
        pass

    with open('scholarships.csv', 'a', newline='', encoding='utf-8') as file:  # 'a' mode for appending
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Title', 'Link', 'Degree', 'Location', 'Funds Needed', 'Eligibility', 'Description'])  # Write header only if file doesn't exist
        for row in data:
            writer.writerow(row)

# Function to get details from individual scholarship pages
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
    
    # Scraping details
    degree = soup.find('div', class_='degree').text.strip() if soup.find('div', class_='degree') else 'N/A'
    location = soup.find('div', class_='location').text.strip() if soup.find('div', class_='location') else 'N/A'
    funds = soup.find('div', class_='funds').text.strip() if soup.find('div', class_='funds') else 'N/A'
    eligibility = soup.find('div', class_='eligibility').text.strip() if soup.find('div', class_='eligibility') else 'N/A'
    description = soup.find('div', class_='description').text.strip() if soup.find('div', class_='description') else 'N/A'

    return degree, location, funds, eligibility, description

# Function to scrape scholarships
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
            links = soup.find_all("a", href=True)

            for link in links:
                href = link.attrs.get('href', '')
                full_url = urljoin(url, href)
                if "Scholarship" in link.text:  # Adjust criteria based on actual content
                    print(f"Title: {link.text.strip()}, URL: {full_url}")
                    details = get_scholarship_details(full_url)
                    if details:
                        degree, location, funds, eligibility, description = details
                        all_scholarship_data.append([link.text.strip(), full_url, degree, location, funds, eligibility, description])
        
        time.sleep(2)  # Delay to avoid being blocked

    save_to_csv(all_scholarship_data)

# Ensure this script can be run independently
if __name__ == "__main__":
    urls = [
        "https://www.scholarshipregion.com/category/scholarships/scholarships-in-usa/",
        "https://www.fastweb.com/"
    ]
    scrape_scholarships(urls)
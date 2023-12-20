import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    """Get the soup object from a given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.content, 'html.parser')

# Directly list faculty URLs
faculty_links = {
    "كلية الصيدلة": [""],
    "كلية العلوم": [""],
    "كلية طب الاسنان": [""],
    "كلية الطب": [""],
    # ... add other faculties here
}

def scrape_departments(department_url):
    """Scrape department names from a department page."""
    soup = get_soup(department_url)
    departments = soup.find_all('li')  # Adjust the tag and attribute as needed
    return [dept.get_text().strip() for dept in departments]

def save_to_csv(filename, data):
    """Save the scraped data to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Process each faculty
for faculty_name, urls in faculty_links.items():
    for url in urls:
        try:
            departments = scrape_departments(url)
            save_to_csv(f'data_{faculty_name}.csv', [(dept,) for dept in departments])
            print(f"Data saved for {faculty_name} in {url}")
        except Exception as e:
            print(f"Error scraping departments from {url}: {e}")

print("Scraping process completed.")

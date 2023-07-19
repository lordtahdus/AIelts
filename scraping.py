import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Set up Scraper API request
api_key = '63344ec8f7f532e761bd07a60531c2f0'
url = 'https://writing9.com/ielts-writing-samples'
params = {
    'api_key': api_key,
    'url': url,
}

# Make the request to Scraper API
response = requests.get('http://api.scraperapi.com', params=params)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <a> tags containing URLs
    links = soup.find_all('a', class_ = 'root__link')

    # Loop through each URL and make requests to scrape data
    for link in links:
        href = link.get('href')
        absolute_url = urljoin(url, href)  # Convert relative URLs to absolute URLs

        # Set up Scraper API request for each URL
        params['url'] = absolute_url

        # Make the request to Scraper API for the specific URL
        response = requests.get('http://api.scraperapi.com', params=params)

        if response.status_code == 200:
            # Parse the HTML content of the specific URL
            sub_soup = BeautifulSoup(response.content, 'html.parser')

            sub_title = sub_soup.find_all('h1', class_ = 'h4')[0].text
            print('Subpage URL:', absolute_url)
            print('Subpage Title:', sub_title)

            sub_content = sub_soup.find('div', class_ = 'content-editable')

            remove_content = sub_content.find_all('div', 'hover')
            for content in remove_content:
                content.extract()
            
            print(sub_content.text)
        else:
            print('Error:', response.status_code)
else:
    print('Error:', response.status_code)

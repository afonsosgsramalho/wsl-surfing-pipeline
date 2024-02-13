from bs4 import BeautifulSoup
import requests

# URL of the page (if fetching from the web)
url = 'https://www.worldsurfleague.com/events/2022/ct?all=1'

# Fetch the HTML content (if fetching from the web)
response = requests.get(url)
html_content = response.text

# Or, directly use your HTML content here if not fetching from the web
# html_content = """YOUR_HTML_CONTENT_HERE"""

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the first <table> element
# If there are multiple tables and you need a specific one, adjust this accordingly
table = soup.find('table')

# Find all <a> elements within this <table> and extract their 'href' attributes
links = [a['href'] for a in table.find_all('a', href=True)]

print(links)

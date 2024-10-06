from bs4 import BeautifulSoup

# Sample HTML
html = '''
<span title="Saturday, June 11, 2022" class="e-day">11</span>
'''

# Create a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# Find the span element by class name 'e-day'
span_element = soup.find('span', class_='e-day')

# Extract the text from the found element
text_value = span_element.get_text()

print(text_value)


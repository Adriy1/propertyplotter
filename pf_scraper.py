from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

base_url = "https://www.propertyfinder.ae/en/transactions/buy/dubai/downtown-dubai-downtown-views-ii"
params = {
    'bdr[]': '1',
    'fu': '0',
    'ob': 'mr',
    'period': '3y',
    'page': 1
}

data = []

while True:
    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the transaction table
    table = soup.find('table', {'class': 'styles_desktop_transaction-list__table__Mc9wB'})
    if not table:
        break

    # Extract table rows
    rows = table.select('tbody[data-testid="table-body"] tr')
    if not rows:
        break

    for row in rows:
        # Extract all columns
        cols = row.find_all('td')

        # Location details
        location_div = cols[0].find('div', class_='styles_desktop_transaction-list__table-location__ywX2B')
        location = location_div.get_text(strip=True) if location_div else None
        unit_details = cols[0].find('span', class_='styles_desktop_transaction-list__table-unit-details__oYIr1').get_text(strip=True)

        # Extract numerical values
        price = float(cols[1].find('span', {'data-testid': 'price'}).get_text(strip=True).replace(',', ''))
        price_per_sqft = float(cols[2].find('span', {'data-testid': 'price-per-sqft'}).get_text(strip=True))
        date_str = cols[3].find('span', {'data-testid': 'date'}).get_text(strip=True)
        contract_status = cols[4].find('div', {'data-testid': 'tag-new-listing'}).get_text(strip=True)
        property_type = cols[5].find('span', {'data-testid': 'property-type'}).get_text(strip=True)
        bedrooms = int(cols[6].find('span', {'data-testid': 'bedroom'}).get_text(strip=True).split()[0])
        size = float(cols[7].find('span', {'data-testid': 'size'}).get_text(strip=True))

        data.append({
            'Location': f"{location} - {unit_details}",
            'Price (AED)': price,
            'Price per sqft': price_per_sqft,
            'Date': datetime.strptime(date_str, '%d %b %Y'),
            'Contract Status': contract_status,
            'Property Type': property_type,
            'Bedrooms': bedrooms,
            'Size (sqft)': size
        })

    # Check for next page
    params['page'] += 1
    time.sleep(0.2)

df = pd.DataFrame(data)
df.to_csv("df.csv", index=False)


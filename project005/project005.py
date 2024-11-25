import requests
from bs4 import BeautifulSoup
import json

url = 'https://polarniczki.pl/uczestniczki-wypraw/hornsund/'
res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

table = soup.find('table', class_='has-fixed-layout')

expeditions = []
if table:
    rows = table.find_all('tr')
    headers = [header.get_text(strip=True) for header in rows[0].find_all('td')]

    for row in rows[1:]:
        columns = row.find_all('td')
        print(len(columns))
        expedition_data = {
            "Wyprawa": columns[0].get_text(strip=True),
            "Daty": columns[1].get_text(strip=True),
            "Wyprawa zimująca": columns[2].get_text(strip=True),
            "Wyprawa letnia": columns[3].get_text(strip=True),
            "Wyprawa wiosenna": columns[4].get_text(strip=True),
        }
        expeditions.append(expedition_data)

# print(json.dumps(expeditions, ensure_ascii=False, indent=4))

with open('expeditions.json', 'w') as file:
    json.dump(expeditions, file, indent=4)

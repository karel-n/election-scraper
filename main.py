"""
main.py - třetí projekt do Engeto Online Python Akademie
Autor: Karel Nodes
Email: k.nodes00@gmail.com
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
from urllib.parse import urljoin

def get_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_obce_links(url):
    soup = get_soup(url)
    obce = []
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                code = cells[0].get_text(strip=True)
                name = cells[1].get_text(strip=True)
                link_tag = cells[0].find('a')
                if link_tag:
                    href = link_tag.get("href")
                    full_url = urljoin(url, href)
                    obce.append((code, name, full_url))
    return obce

def parse_obec(url):
    soup = get_soup(url)
    tables = soup.find_all("table")
    stat_cells = tables[0].find_all("td")
    voters = stat_cells[3].get_text(strip=True)
    envelopes = stat_cells[4].get_text(strip=True)
    valid = stat_cells[7].get_text(strip=True)
    party_data = {}
    for table in tables[1:]:
        rows = table.find_all("tr")[2:]
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 3:
                party = tds[1].get_text(strip=True)
                votes = tds[2].get_text(strip=True)
                party_data[party] = votes

    return voters, envelopes, valid, party_data

def save_to_csv(filename, results, parties):
    fieldnames = ["code", "name", "voters", "envelopes", "valid"] + parties
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def main():
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL> <vystup.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_file = sys.argv[2]

    obce = get_obce_links(input_url)
    print(f"Nalezeno obcí: {len(obce)}")

    results = []
    all_parties = set()

    for code, name, link in obce:
        print(f"Zpracovávám {name} ({code})")
        voters, envelopes, valid, parties = parse_obec(link)
        all_parties.update(parties.keys())
        row = {
            "code": code,
            "name": name,
            "voters": voters,
            "envelopes": envelopes,
            "valid": valid,
            **parties
        }
        results.append(row)

    sorted_parties = sorted(all_parties)
    save_to_csv(output_file, results, sorted_parties)
    print(f"Výsledky uloženy do {output_file}")

if __name__ == "__main__":
    main()

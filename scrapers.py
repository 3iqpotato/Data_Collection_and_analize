import json
import os
import time

import requests
from bs4 import BeautifulSoup
from models.countries import Country
from static_variables import gdp_url, continent_urls, CACHE_DURATION

def is_cache_valid(filepath="countries.json"):
    if not os.path.exists(filepath):
        return False
    file_age = time.time() - os.path.getmtime(filepath)
    return file_age < CACHE_DURATION


def load_data():
    if is_cache_valid():
        print("Loading from cache...")
        return read_from_the_file()
    else:
        print("Cache expired or missing, scraping fresh data...")
        all_countries = scrape_the_data()
        write_in_the_file(all_countries)
        return all_countries

def parse_values_to_int(g):
    g = g.strip().replace(",", "").replace("$", "")
    try:
        return int(g)
    except ValueError as e:
        print(f"Error parsing GDP: {e}")
        return 0

def scrape_the_gdp():
    dict_name_gdp = {}
    gdp_response = requests.get(gdp_url)
    html_response = BeautifulSoup(gdp_response.text, 'html.parser')
    table = html_response.find("table")
    rows = table.find_all("tr")

    for row in rows[1::]:
        cells = row.find_all("td")
        country_name = cells[1].text.strip()
        gdp = cells[3].text.strip()
        dict_name_gdp[country_name] = parse_values_to_int(gdp)

    return dict_name_gdp

def scrape_the_data():
    dict_name_gdp = scrape_the_gdp()
    res = []

    for continent, url in continent_urls.items():
        response = requests.get(url)
        html_response = BeautifulSoup(response.text, 'html.parser')
        table = html_response.find("table")
        rows = table.find_all("tr")

        for row in rows[1::]:  # vzimam sled 1viq element 1viq sa gore imenata na kolonite
            cells = row.find_all("td")
            country_name = cells[1].text.strip()
            c_population = parse_values_to_int(cells[2].text)

            res.append(Country(country_name, c_population, continent,dict_name_gdp.get(country_name, 0)))  # taka dostypvame directno bez mnogo iteracii

    return res

def write_in_the_file(countries):
    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in countries], f, ensure_ascii=False, indent=2)


def read_from_the_file():
    with open("countries.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Country(**d) for d in data]
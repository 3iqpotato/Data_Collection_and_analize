from logging import exception
import json
import requests
import pandas
from bs4 import BeautifulSoup

continent_urls = {
    "Asia": "https://www.worldometers.info/population/countries-in-asia-by-population/",
    # "Africa": "https://www.worldometers.info/population/countries-in-africa-by-population/",
    # "Europe": "https://www.worldometers.info/population/countries-in-europe-by-population/",
    # "Latin America": "https://www.worldometers.info/population/countries-in-latin-america-and-the-caribbean-by-population/",
    # "Northern America": "https://www.worldometers.info/population/countries-in-northern-america-by-population/",
    # "Oceania": "https://www.worldometers.info/population/countries-in-oceania-by-population/",
}
gdp_url = "https://www.worldometers.info/gdp/gdp-by-country/"

counties_container = []


class Country:
    def __init__(self, name, population, region, gdp=0):
        self.name = name
        self.population = population
        self.region = region
        self.gdp = gdp

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()

    def to_dict(self):
        return {
            "name": self.name,
            "population": self.population,
            "region": self.region,
            "gdp": self.gdp
        }

    def __str__(self):
        return f"{self.name} : {self.population} : {self.region} : {self.gdp}"

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

    for continent, url in continent_urls.items():
        response = requests.get(url)
        html_response = BeautifulSoup(response.text, 'html.parser')
        table = html_response.find("table")
        rows = table.find_all("tr")

        for row in rows[1::]:  # vzimam sled 1viq element 1viq sa gore imenata na kolonite
            cells = row.find_all("td")
            country_name = cells[1].text.strip()
            c_population = parse_values_to_int(cells[2].text)

            counties_container.append(Country(country_name, c_population, continent,dict_name_gdp.get(country_name, 0)))  # taka dostypvame directno bez mnogo iteracii

scrape_the_data()
def write_in_the_file(countries):
    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in counties_container], f, ensure_ascii=False, indent=2)


def read_from_the_file():
    with open("countries.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Country(**d) for d in data]




for c in read_from_the_file():
    print(c)

#at this point claud refused to answer me :(
print("All data get what do u want:")
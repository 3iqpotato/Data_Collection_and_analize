from logging import exception
import json
import requests
import pandas
from bs4 import BeautifulSoup

continent_urls = {
    "Asia": "https://www.worldometers.info/population/countries-in-asia-by-population/",
    "Africa": "https://www.worldometers.info/population/countries-in-africa-by-population/",
    "Europe": "https://www.worldometers.info/population/countries-in-europe-by-population/",
    "Latin America": "https://www.worldometers.info/population/countries-in-latin-america-and-the-caribbean-by-population/",
    "Northern America": "https://www.worldometers.info/population/countries-in-northern-america-by-population/",
    "Oceania": "https://www.worldometers.info/population/countries-in-oceania-by-population/",
}
gdp_url = "https://www.worldometers.info/gdp/gdp-by-country/"

# counties_container = []


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

def get_gdp_population(country_name, all_data):
    country_l = list(filter(lambda x: x.name.lower() == country_name.lower(), all_data))
    if len(country_l) > 0:
        country = country_l[0]
        return country
    return 0

def list_countries_in_continent(continent, all_data):
    countries_l = list(filter(lambda x: x.region.lower() == continent.lower(), all_data))
    if len(countries_l) > 0:
        return countries_l
    return 0

def get_total_population_gdp_per_continent(all_data):
    result = {}

    for country in all_data:
        continent = country.region
        population = country.population
        gdp = country.gdp

        if continent not in result:
            result[continent] = [population, gdp]
        else:
            result[continent][0] += population
            result[continent][1] += gdp

    result = {continent: (total_pop, total_gdp) for continent, (total_pop, total_gdp) in result.items()}

    return result

def get_avg_population_gdp_per_continent(all_data):
    totals = get_total_population_gdp_per_continent(all_data)

    counts = {}

    for country in all_data:
        continent = country.region

        if continent not in counts:
            counts[continent] = 1
        else:
            counts[continent] += 1

    averages = {}

    for continent in totals:
        total_pop, total_gdp = totals[continent]
        count = counts[continent]

        averages[continent] = (
            total_pop / count,
            total_gdp / count
        )

    return averages


def top_5_countries(all_data, key, continent=None):
    if continent:
        filtered_data = [c for c in all_data if c.region.lower() == continent.lower()]
    else:
        filtered_data = all_data

    # Сортиране и връщане на топ 5
    sorted_data = sorted(filtered_data, key=lambda c: getattr(c, key), reverse=True)
    return sorted_data[:5]

def filter_countries_by_population(all_data, option, min_pop=0, max_pop=0):
    if option == "1":
        return [c for c in all_data if c.population > min_pop]
    elif option == "2":
        return [c for c in all_data if c.population < max_pop]
    elif option == "3":
        return [c for c in all_data if min_pop < c.population < max_pop]
    else:
        return []

def print_menu():
    print("\n" + "=" * 50)
    print("        DATA ANALYSIS MENU")
    print("=" * 50)
    print("1. GDP/Population for a specific country")
    print("2. List all countries in a continent")
    print("3. Total population and GDP per continent")
    print("4. Average population and GDP per continent")
    print("5. Top 5 countries by population worldwide")
    print("6. Top 5 countries by GDP worldwide")
    print("7. Top 5 countries in a continent (by population or GDP)")
    print("8. Filter countries by population range")
    print("0. Exit")
    print("=" * 50)

#at this point claud refused to answer me :(

def main():
    # all_counties = scrape_the_data()   # закоментирам защото вече ги имам локално и ще си ползвам тях иначе работи тествано! :)
    # write_in_the_file(all_counties)
    readed_countries = read_from_the_file()
    while True:
        print_menu()

        choice = input("Enter your choice (0-8): ").strip()

        if choice == "0":
            print("Exiting program. Goodbye!")
            break

        elif choice == "1":
            country = input("Enter country name: ").strip()
            searched_country = get_gdp_population(country, readed_countries)  # твоята функция
            if searched_country == 0:
                print("Error: Country not found!")
            else:
                print(f"\n {searched_country.name}")
                print(f"   Population: {searched_country.population:,}")
                print(f"   GDP: ${searched_country.gdp:,}")

        elif choice == "2":
            continent = input("Enter continent name: ").strip()
            result = list_countries_in_continent(continent, readed_countries)
            if result == 0:
                print("Error: Continent not found!")
            else:
                print(f"\n Countries in {continent}:")
                for c in result:
                    print(f"   • {c.name}")

        elif choice == "3":
            result = get_total_population_gdp_per_continent(readed_countries)
            print("\n Total Population & GDP per Continent:")
            for continent, (total_pop, total_gdp) in result.items():
                print(f"\n {continent}:")
                print(f"   Population: {total_pop:,}")
                print(f"   GDP: ${total_gdp:,}")


        elif choice == "4":
            result = get_avg_population_gdp_per_continent(readed_countries)
            print("\n Average Population & GDP per Continent:")
            for continent, (avg_pop, avg_gdp) in result.items():
                print(f"\n {continent}:")
                print(f"   Average Population: {avg_pop:,.0f}")
                print(f"   Average GDP: ${avg_gdp:,.0f}")

        elif choice == "5":
            result = top_5_countries(readed_countries, key="population")
            print("\n TOP 5 COUNTRIES BY POPULATION:")
            for i, country in enumerate(result, 1):
                print(f"   {i}. {country.name} - {country.population}")

        elif choice == "6":
            result = top_5_countries(readed_countries, key="gdp")
            print("\n TOP 5 COUNTRIES BY GDP:")
            for i, country in enumerate(result, 1):
                print(f"   {i}. {country.name} - ${country.gdp:,}")

        elif choice == "7":
            continent = input("Enter continent name: ").strip()
            print("\n Sort by:")
            print("   1. Population")
            print("   2. GDP")
            sort_by = input("Choose (1 or 2): ").strip()

            if sort_by == "1":
                result = top_5_countries(readed_countries,"population", continent)
                if not result:
                    print("Error: Continent not found!")
                else:
                    print(f"\nTOP 5 COUNTRIES IN {continent.upper()} BY POPULATION:")
                    for i, country in enumerate(result, 1):
                        print(f"   {i}. {country.name} - {country.population:,}")

            elif sort_by == "2":
                result = top_5_countries(readed_countries,"gdp", continent)
                if not result:
                    print("Error: Continent not found!")
                else:
                    print(f"\nTOP 5 COUNTRIES IN {continent.upper()} BY GDP:")
                    for i, country in enumerate(result, 1):
                        print(f"   {i}. {country.name} - ${country.gdp:,}")
            else:
                print("Invalid choice!")

        elif choice == "8":
            print("\n Filter countries by population range:")
            print("   1. Greater than (min)")
            print("   2. Less than (max)")
            print("   3. Between (min - max)")
            filter_type = input("Choose (1, 2 or 3): ").strip()

            if filter_type == "1":
                min_pop = int(input("Enter minimum population: ").strip())
                result = result = filter_countries_by_population(readed_countries, filter_type, min_pop=min_pop)
                print(f"\nCountries with population > {min_pop:,}:")
                for country in result:
                    print(f"   • {country.name} - {country.population:,}")

            elif filter_type == "2":
                max_pop = int(input("Enter maximum population: ").strip())
                result = result = filter_countries_by_population(readed_countries, filter_type, max_pop=max_pop)
                print(f"\nCountries with population < {max_pop:,}:")
                for country in result:
                    print(f"   • {country.name} - {country.population:,}")

            elif filter_type == "3":
                min_pop = int(input("Enter minimum population: ").strip())
                max_pop = int(input("Enter maximum population: ").strip())
                result = result = filter_countries_by_population(readed_countries, filter_type, min_pop, max_pop)
                print(f"\nCountries with population between {min_pop:,} and {max_pop:,}:")
                for country in result:
                    print(f"   • {country.name} - {country.population:,}")
            else:
                print("Invalid choice!")

        else:
            print("Invalid choice. Please enter a number between 0 and 4.")
            continue

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
from logging import exception
import json
import requests
import pandas
from bs4 import BeautifulSoup
from functionalities import *
from scrapers import *
from static_variables import *
from models import countries

def main():
    loaded_countries = load_data()
    while True:
        print_menu()

        choice = input("Enter your choice (0-8): ").strip()

        if choice == "0":
            print("Exiting program. Goodbye!")
            break

        elif choice == "1":
            country = input("Enter country name: ").strip()
            searched_country = get_gdp_population(country, loaded_countries)  # твоята функция
            if not searched_country:
                print("Error: Country not found!")
            else:
                print(f"\n {searched_country.name}")
                print(f"   Population: {searched_country.population:,}")
                print(f"   GDP: ${searched_country.gdp:,}")

        elif choice == "2":
            continent = input("Enter continent name: ").strip()
            result = list_countries_in_continent(continent, loaded_countries)
            if not result:
                print("Error: Continent not found!")
            else:
                print(f"\n Countries in {continent}:")
                for c in result:
                    print(f"   • {c.name}")

        elif choice == "3":
            result = get_total_population_gdp_per_continent(loaded_countries)
            print("\n Total Population & GDP per Continent:")
            for continent, (total_pop, total_gdp) in result.items():
                print(f"\n {continent}:")
                print(f"   Population: {total_pop:,}")
                print(f"   GDP: ${total_gdp:,}")


        elif choice == "4":
            result = get_avg_population_gdp_per_continent(loaded_countries)
            print("\n Average Population & GDP per Continent:")
            for continent, (avg_pop, avg_gdp) in result.items():
                print(f"\n {continent}:")
                print(f"   Average Population: {avg_pop:,.0f}")
                print(f"   Average GDP: ${avg_gdp:,.0f}")

        elif choice == "5":
            result = top_5_countries(loaded_countries, key="population")
            print("\n TOP 5 COUNTRIES BY POPULATION:")
            for i, country in enumerate(result, 1):
                print(f"   {i}. {country.name} - {country.population:,}")

        elif choice == "6":
            result = top_5_countries(loaded_countries, key="gdp")
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
                result = top_5_countries(loaded_countries,"population", continent)
                if not result:
                    print("Error: Continent not found!")
                else:
                    print(f"\nTOP 5 COUNTRIES IN {continent.upper()} BY POPULATION:")
                    for i, country in enumerate(result, 1):
                        print(f"   {i}. {country.name} - {country.population:,}")

            elif sort_by == "2":
                result = top_5_countries(loaded_countries,"gdp", continent)
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
                result = result = filter_countries_by_population(loaded_countries, filter_type, min_pop=min_pop)
                print(f"\nCountries with population > {min_pop:,}:")
                for country in result:
                    print(f"   • {country.name} - {country.population:,}")

            elif filter_type == "2":
                max_pop = int(input("Enter maximum population: ").strip())
                result = result = filter_countries_by_population(loaded_countries, filter_type, max_pop=max_pop)
                print(f"\nCountries with population < {max_pop:,}:")
                for country in result:
                    print(f"   • {country.name} - {country.population:,}")

            elif filter_type == "3":
                min_pop = int(input("Enter minimum population: ").strip())
                max_pop = int(input("Enter maximum population: ").strip())
                result = result = filter_countries_by_population(loaded_countries, filter_type, min_pop, max_pop)
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
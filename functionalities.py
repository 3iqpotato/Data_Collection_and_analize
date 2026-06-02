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
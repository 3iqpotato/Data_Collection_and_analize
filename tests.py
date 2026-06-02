# tests.py
from models.countries import Country
from functionalities import (
    get_gdp_population,
    list_countries_in_continent,
    get_total_population_gdp_per_continent,
    get_avg_population_gdp_per_continent,
    top_5_countries,
    filter_countries_by_population,
)

mock_data = [
    Country("China", 1_400_000_000, "Asia", 14_000_000_000_000),
    Country("India", 1_380_000_000, "Asia", 3_000_000_000_000),
    Country("Germany", 83_000_000, "Europe", 4_000_000_000_000),
    Country("France", 67_000_000, "Europe", 2_800_000_000_000),
    Country("Nigeria", 220_000_000, "Africa", 440_000_000_000),
    Country("Brazil", 215_000_000, "Latin America", 1_600_000_000_000),
    Country("Canada", 38_000_000, "Northern America", 1_990_000_000_000),
]

def test_get_gdp_population():
    result = get_gdp_population("China", mock_data)
    assert result.name == "China"
    assert result.population == 1_400_000_000
    result_missing = get_gdp_population("Narnia", mock_data)
    assert result_missing is None
    print("✓ get_gdp_population")

def test_list_countries_in_continent():
    result = list_countries_in_continent("Asia", mock_data)
    assert len(result) == 2
    assert all(c.region == "Asia" for c in result)
    result_missing = list_countries_in_continent("Antarctica", mock_data)
    assert result_missing is None
    print("✓ list_countries_in_continent")

def test_get_total_population_gdp_per_continent():
    result = get_total_population_gdp_per_continent(mock_data)
    assert result["Asia"][0] == 1_400_000_000 + 1_380_000_000
    assert result["Europe"][1] == 4_000_000_000_000 + 2_800_000_000_000
    print("✓ get_total_population_gdp_per_continent")

def test_get_avg_population_gdp_per_continent():
    result = get_avg_population_gdp_per_continent(mock_data)
    expected_avg_pop_asia = (1_400_000_000 + 1_380_000_000) / 2
    assert result["Asia"][0] == expected_avg_pop_asia
    print("✓ get_avg_population_gdp_per_continent")

def test_top_5_countries():
    result = top_5_countries(mock_data, key="population")
    assert result[0].name == "China"
    assert len(result) <= 5
    result_continent = top_5_countries(mock_data, key="gdp", continent="Europe")
    assert result_continent[0].name == "Germany"
    print("✓ top_5_countries")

def test_filter_countries_by_population():
    result = filter_countries_by_population(mock_data, "1", min_pop=200_000_000)
    assert all(c.population > 200_000_000 for c in result)
    result = filter_countries_by_population(mock_data, "2", max_pop=100_000_000)
    assert all(c.population < 100_000_000 for c in result)
    result = filter_countries_by_population(mock_data, "3", min_pop=50_000_000, max_pop=300_000_000)
    assert all(50_000_000 < c.population < 300_000_000 for c in result)
    print("✓ filter_countries_by_population")

if __name__ == "__main__":
    test_get_gdp_population()
    test_list_countries_in_continent()
    test_get_total_population_gdp_per_continent()
    test_get_avg_population_gdp_per_continent()
    test_top_5_countries()
    test_filter_countries_by_population()
    print("\nAll tests passed! ✓")

#the test are ai generated but at least i checked what they do)
class Country:
    def __init__(self, name, population, region, gdp=0):
        self.name = name
        self.population = population
        self.region = region
        self.gdp = gdp
    
    @property
    def population(self):
        return self._population
    
    @population.setter
    def population(self, value):
        cleaned = str(value).strip().replace(",", "")
        try:
            self._population = int(cleaned)
        except ValueError:
            print(f"Invalid population for {self.name}: {value}")
            self._population = 0


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
"""Download data from GapMinder

countries.csv - last available info for most features
cze.csv - Czechia features evolution 1993-2013
"""
import pandas as pd
import gapminderdata as gmd


def run():
    # Get country metadata
    countries = gmd.read_countries()
    countries = countries[country_columns].copy()
    countries["is_eu"] = countries["name"].isin(eu.keys())
    assert countries["is_eu"].sum() == 28, f"Only {countries['is_eu'].sum()} countries in EU."
    
    countries["is_oecd"] = countries["name"].isin(oecd)
    assert countries["is_oecd"].sum() == 36, f"Only {countries['is_oecd'].sum()} countries in OECD: {list(countries.query('is_oecd').index)}"

    countries["eu_accession"] = pd.to_datetime(countries["name"].apply(lambda n: eu.get(n, None)))

    # Get data points
    data = gmd.read_columns(data_columns)
    data = (
        countries.merge(data.reset_index(), right_on="geo", left_index=True)
        .reset_index(drop=True)
        .sort_values(["name", "time"])
    )

    # Rename
    data = data.rename(rename_columns, axis=1)

    gap_data = (
        data.dropna(thresh=len(data.columns) - 5)
        .sort_values("year", ascending=False)
        .groupby("name")
        .first()
        .drop(["geo"], axis=1)
        # .drop(["iso3166_1_alpha3", "geo"], axis=1)
        .reset_index()
    )
    gap_data.to_csv("data/countries.csv", index=False)

    cze_data = (
        data[data["name"] == "Czech Republic"]
        .sort_values("year", ascending=True)
        .drop(
            [
                "area",
                "eu_accession",
                "iso_alpha",
                "geo",
                "name",
                "world_6region",
                "world_4region",
                "income_groups",
                "is_eu",
                "is_oecd",
            ],
            axis=1,
        )
        .reset_index(drop=True)
    )
    cze_data = cze_data.dropna(thresh=len(cze_data.columns) - 4)
    cze_data.to_csv("data/cze.csv", index=False)


# https://en.wikipedia.org/wiki/Enlargement_of_the_European_Union
eu = {
    "Austria": "1995-01-01",
    "Belgium": "1952-07-23",
    "Bulgaria": "2007-01-01",
    "Croatia": "2013-01-01",
    "Cyprus": "2004-05-01",
    "Czech Republic": "2004-05-01",
    "Denmark": "1973-01-01",
    "Estonia": "2004-05-01",
    "Finland": "1995-01-01",
    "France": "1952-07-23",
    "Germany": "1952-07-23",
    "Greece": "1981-01-01",
    "Hungary": "2004-05-01",
    "Ireland": "1973-01-01",
    "Italy": "1952-07-23",
    "Latvia": "2004-05-01",
    "Lithuania": "2004-05-01",
    "Luxembourg": "1952-07-23",
    "Malta": "2004-05-01",
    "Netherlands": "1952-07-23",
    "Poland": "2004-05-01",
    "Portugal": "1986-01-01",
    "Romania": "2007-01-01",
    "Slovak Republic": "2004-05-01",
    "Slovenia": "2004-05-01",
    "Spain": "1986-01-01",
    "Sweden": "1995-01-01",
    "United Kingdom": "1973-01-01",
}

# https://en.wikipedia.org/wiki/OECD
oecd = [
    "Australia",
    "Austria",
    "Belgium",
    "Canada",
    "Chile",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Mexico",
    "Netherlands",
    "New Zealand",
    "Norway",
    "Poland",
    "Portugal",
    "Slovak Republic",
    "Slovenia",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "United Kingdom",
    "United States"
]

country_columns = [
    "name",
    "iso3166_1_alpha3",
    "world_6region",
    "world_4region",
    "income_groups",
]

data_columns = [
    "surface_area_sq_km",
    "total_population_with_projections",
    "alcohol_consumption_per_adult_15plus_litres",
    "body_mass_index_bmi_men_kgperm2",
    "body_mass_index_bmi_women_kgperm2",
    "car_deaths_per_100000_people",
    "co2_emissions_tonnes_per_person",
    "food_supply_kilocalories_per_person_and_day",
    "income_share_of_poorest_10percent",
    "income_share_of_richest_10percent",
    "life_expectancy_years",
    "all_causes_deaths_in_newborn_per_1000_births",
]

rename_columns = {
    "all_causes_deaths_in_newborn_per_1000_births": "newborn_mortality",
    "surface_area_sq_km": "area",
    "food_supply_kilocalories_per_person_and_day": "calories_per_day",
    "total_population_with_projections": "population",
    "body_mass_index_bmi_men_kgperm2": "bmi_men",
    "body_mass_index_bmi_women_kgperm2": "bmi_women",
    "alcohol_consumption_per_adult_15plus_litres": "alcohol_adults",
    "iso3166_1_alpha3": "iso_alpha",
    "time": "year",
}


if __name__ == "__main__":
    run()

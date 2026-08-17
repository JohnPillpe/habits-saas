# app/services/location_service.py

# ============================================================
# REGIONS
# ============================================================

REGIONS = {
    "Americas",
    "Europe",
    "Asia",
    "Africa",
    "Oceania",
    "EMEA",
    "UK",
    "Northern America",
}


# ============================================================
# COUNTRY ALIASES
# ============================================================

COUNTRY_ALIASES = {
    "UK": "United Kingdom",
    "U.K.": "United Kingdom",
    "US": "United States",
    "U.S.": "United States",
    "USA": "United States",
}


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Costa Rica",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "Estonia",
    "Ethiopia",
    "Finland",
    "France",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Guatemala",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "Jordan",
    "Kenya",
    "Latvia",
    "Lebanon",
    "Lithuania",
    "Luxembourg",
    "Malaysia",
    "Malta",
    "Mauritius",
    "Mexico",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nigeria",
    "Norway",
    "Pakistan",
    "Panama",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Rwanda",
    "Saudi Arabia",
    "Serbia",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sri Lanka",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Thailand",
    "Tunisia",
    "Turkey",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Zambia",
    "Zimbabwe",
]


# ============================================================
# REGION -> COUNTRIES
# ============================================================

REGION_COUNTRIES = {

    "Europe": {
        "Austria",
        "Belgium",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Georgia",
        "Germany",
        "Greece",
        "Hungary",
        "Iceland",
        "Ireland",
        "Italy",
        "Latvia",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Moldova",
        "Monaco",
        "Montenegro",
        "Netherlands",
        "Norway",
        "Poland",
        "Portugal",
        "Romania",
        "Serbia",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Switzerland",
        "Ukraine",
        "United Kingdom",
    },

    "Northern America": {
        "Canada",
        "United States",
    },

    "UK": {
        "United Kingdom",
    },

    "Americas": {
        "Argentina",
        "Bahamas",
        "Barbados",
        "Belize",
        "Bolivia",
        "Brazil",
        "Canada",
        "Chile",
        "Colombia",
        "Costa Rica",
        "Dominican Republic",
        "Ecuador",
        "Guatemala",
        "Mexico",
        "Panama",
        "Peru",
        "United States",
        "Uruguay",
        "Venezuela",
    },

    "Asia": {
        "Afghanistan",
        "Bahrain",
        "Bangladesh",
        "Brunei",
        "China",
        "India",
        "Indonesia",
        "Israel",
        "Japan",
        "Jordan",
        "Malaysia",
        "Mongolia",
        "Nepal",
        "Pakistan",
        "Philippines",
        "Qatar",
        "Saudi Arabia",
        "Singapore",
        "South Korea",
        "Sri Lanka",
        "Taiwan",
        "Thailand",
        "Turkey",
        "United Arab Emirates",
        "Vietnam",
    },

    "Africa": {
        "Algeria",
        "Angola",
        "Benin",
        "Botswana",
        "Cameroon",
        "Egypt",
        "Ethiopia",
        "Ghana",
        "Kenya",
        "Mauritius",
        "Morocco",
        "Nigeria",
        "Rwanda",
        "South Africa",
        "Tunisia",
        "Zambia",
        "Zimbabwe",
    },

    "Oceania": {
        "Australia",
        "New Zealand",
    },
}


# ============================================================
# EMEA
# Europe + Middle East + Africa
# ============================================================

REGION_COUNTRIES["EMEA"] = (
    REGION_COUNTRIES["Europe"]
    | REGION_COUNTRIES["Africa"]
    | {
        "Bahrain",
        "Israel",
        "Jordan",
        "Qatar",
        "Saudi Arabia",
        "United Arab Emirates",
    }
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_country(
    value: str | None,
) -> str | None:

    if not value:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Exact alias
    alias = COUNTRY_ALIASES.get(value)

    if alias:
        return alias

    # Case-insensitive alias
    value_lower = value.lower()

    for alias_key, canonical_country in COUNTRY_ALIASES.items():

        if value_lower == alias_key.lower():
            return canonical_country

    return value


# ============================================================
# REGION NORMALIZATION
# ============================================================

def normalize_region(
    value: str | None,
) -> str | None:

    if not value:
        return None

    value = str(value).strip()

    if not value:
        return None

    for region in REGIONS:

        if value.lower() == region.lower():
            return region

    return value


# ============================================================
# GET COUNTRIES FOR REGION
# ============================================================

def get_countries_for_region(
    region: str | None,
) -> list[str]:

    if not region:
        return sorted(
            COUNTRIES,
            key=str.lower,
        )

    normalized_region = normalize_region(region)

    if not normalized_region:
        return sorted(
            COUNTRIES,
            key=str.lower,
        )

    countries = REGION_COUNTRIES.get(
        normalized_region,
        set(),
    )

    return sorted(
        countries,
        key=str.lower,
    )

def get_cities(
    country: str | None = None,
    query: str | None = None,
) -> list[str]:
    """
    Returns cities from the location catalog.

    country:
        Optional country filter.

    query:
        Optional city search string.
    """

    # --------------------------------------------------
    # CITY CATALOG
    # --------------------------------------------------

    cities_by_country = {
        "France": [
            "Paris",
            "Lyon",
            "Marseille",
            "Toulouse",
            "Bordeaux",
            "Lille",
            "Nantes",
            "Nice",
            "Montpellier",
            "Strasbourg",
        ],

        "United Kingdom": [
            "London",
            "Manchester",
            "Birmingham",
            "Liverpool",
            "Leeds",
            "Bristol",
            "Edinburgh",
            "Glasgow",
            "Cambridge",
            "Oxford",
        ],

        "Germany": [
            "Berlin",
            "Munich",
            "Hamburg",
            "Frankfurt",
            "Cologne",
            "Düsseldorf",
            "Stuttgart",
            "Leipzig",
            "Dresden",
            "Hannover",
        ],

        "Spain": [
            "Madrid",
            "Barcelona",
            "Valencia",
            "Seville",
            "Bilbao",
            "Málaga",
            "Alicante",
            "Zaragoza",
            "Palma",
            "Murcia",
        ],

        "Italy": [
            "Rome",
            "Milan",
            "Naples",
            "Turin",
            "Florence",
            "Bologna",
            "Venice",
            "Genoa",
            "Palermo",
            "Pisa",
        ],

        "Netherlands": [
            "Amsterdam",
            "Rotterdam",
            "The Hague",
            "Utrecht",
            "Eindhoven",
            "Groningen",
        ],

        "Belgium": [
            "Brussels",
            "Antwerp",
            "Ghent",
            "Bruges",
        ],

        "Portugal": [
            "Lisbon",
            "Porto",
            "Braga",
            "Coimbra",
        ],

        "Ireland": [
            "Dublin",
            "Cork",
            "Galway",
            "Limerick",
        ],

        "United States": [
            "New York",
            "San Francisco",
            "Los Angeles",
            "Chicago",
            "Boston",
            "Seattle",
            "Austin",
            "Washington",
            "Miami",
            "Denver",
        ],

        "Canada": [
            "Toronto",
            "Vancouver",
            "Montreal",
            "Calgary",
            "Ottawa",
            "Edmonton",
        ],

        "Australia": [
            "Sydney",
            "Melbourne",
            "Brisbane",
            "Perth",
            "Adelaide",
            "Canberra",
        ],

        "India": [
            "Bangalore",
            "Mumbai",
            "Delhi",
            "Hyderabad",
            "Pune",
            "Chennai",
            "Gurgaon",
        ],

        "Singapore": [
            "Singapore",
        ],

        "Japan": [
            "Tokyo",
            "Osaka",
            "Kyoto",
            "Yokohama",
        ],

        "China": [
            "Beijing",
            "Shanghai",
            "Shenzhen",
            "Guangzhou",
        ],
    }

    # --------------------------------------------------
    # COUNTRY NORMALIZATION
    # --------------------------------------------------

    normalized_country = normalize_country(country)

    # --------------------------------------------------
    # SELECT CITIES
    # --------------------------------------------------

    if normalized_country:

        cities = cities_by_country.get(
            normalized_country,
            [],
        )

    else:

        cities = [
            city
            for country_cities in cities_by_country.values()
            for city in country_cities
        ]

    # --------------------------------------------------
    # CITY SEARCH
    # --------------------------------------------------

    normalized_query = (
        (query or "")
        .strip()
        .lower()
    )

    if normalized_query:

        cities = [
            city
            for city in cities
            if normalized_query in city.lower()
        ]

    # --------------------------------------------------
    # DEDUPLICATE + SORT
    # --------------------------------------------------

    return sorted(
        set(cities),
        key=str.lower,
    )
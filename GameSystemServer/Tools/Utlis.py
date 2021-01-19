from datetime import date
import datetime
from typing import List

class Countries:
    __countries: List[str] = [
        "Afghanistan",
        "Bahrain",
        "Bangladesh",
        "Bhutan",
        "Brunei_Darussalam",
        "Cambodia",
        "China",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Israel",
        "Japan",
        "Jordan",
        "Kazakhstan",
        "Kuwait",
        "Kyrgyzstan",
        "Laos",
        "Lebanon",
        "Malaysia",
        "Maldives",
        "Mongolia",
        "Myanmar",
        "Nepal",
        "Oman",
        "Pakistan",
        "Palestine",
        "Philippines",
        "Qatar",
        "Saudi_Arabia",
        "Singapore",
        "South_Korea",
        "Sri_Lanka",
        "Syria",
        "Taiwan",
        "Tajikistan",
        "Thailand",
        "Timor_Leste",
        "Turkey",
        "United_Arab_Emirates",
        "Uzbekistan",
        "Vietnam",
        "Yemen",
        "Albania",
        "Andorra",
        "Armenia",
        "Austria",
        "Azerbaijan",
        "Belarus",
        "Belgium",
        "Bosnia_and_Herzegovina",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czechia",
        "Denmark",
        "Estonia",
        "Faroe_Islands",
        "Finland",
        "France",
        "Georgia",
        "Germany",
        "Gibraltar",
        "Greece",
        "Guernsey",
        "Holy_See",
        "Hungary",
        "Iceland",
        "Ireland",
        "Isle_of_Man",
        "Italy",
        "Jersey",
        "Kosovo",
        "Latvia",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Moldova",
        "Monaco",
        "Montenegro",
        "Netherlands",
        "North_Macedonia",
        "Norway",
        "Poland",
        "Portugal",
        "Romania",
        "Russia",
        "San_Marino",
        "Serbia",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Switzerland",
        "Ukraine",
        "United_Kingdom",
        "Algeria",
        "Angola",
        "Benin",
        "Botswana",
        "Burkina_Faso",
        "Burundi",
        "Cameroon",
        "Cape_Verde",
        "Central_African_Republic",
        "Chad",
        "Comoros",
        "Congo",
        "Cote_dIvoire",
        "Democratic_Republic_of_the_Congo",
        "Djibouti",
        "Egypt",
        "Equatorial_Guinea",
        "Eritrea",
        "Eswatini",
        "Ethiopia",
        "Gabon",
        "Gambia",
        "Ghana",
        "Guinea",
        "Guinea_Bissau",
        "Kenya",
        "Lesotho",
        "Liberia",
        "Libya",
        "Madagascar",
        "Malawi",
        "Mali",
        "Mauritania",
        "Mauritius",
        "Morocco",
        "Mozambique",
        "Namibia",
        "Niger",
        "Nigeria",
        "Rwanda",
        "Sao_Tome_and_Principe",
        "Senegal",
        "Seychelles",
        "Sierra_Leone",
        "Somalia",
        "South_Africa",
        "South_Sudan",
        "Sudan",
        "Togo",
        "Tunisia",
        "Uganda",
        "United_Republic_of_Tanzania",
        "Western_Sahara",
        "Zambia",
        "Zimbabwe",
        "Anguilla",
        "Antigua_and_Barbuda",
        "Argentina",
        "Aruba",
        "Bahamas",
        "Barbados",
        "Belize",
        "Bermuda",
        "Bolivia",
        "Bonaire, Saint Eustatius and Saba",
        "Brazil",
        "British_Virgin_Islands",
        "Canada",
        "Cayman_Islands",
        "Chile",
        "Colombia",
        "Costa_Rica",
        "Cuba",
        "CuraÃ§ao",
        "Dominica",
        "Dominican_Republic",
        "Ecuador",
        "El_Salvador",
        "Falkland_Islands_(Malvinas)",
        "Greenland",
        "Grenada",
        "Guatemala",
        "Guyana",
        "Haiti",
        "Honduras",
        "Jamaica",
        "Mexico",
        "Montserrat",
        "Nicaragua",
        "Panama",
        "Paraguay",
        "Peru",
        "Puerto_Rico",
        "Saint_Kitts_and_Nevis",
        "Saint_Lucia",
        "Saint_Vincent_and_the_Grenadines",
        "Sint_Maarten",
        "Suriname",
        "Trinidad_and_Tobago",
        "Turks_and_Caicos_islands",
        "United_States_of_America",
        "United_States_Virgin_Islands",
        "Uruguay",
        "Venezuela",
        "Australia",
        "Fiji",
        "French_Polynesia",
        "Guam",
        "New_Caledonia",
        "New_Zealand",
        "Northern_Mariana_Islands",
        "Papua_New_Guinea"
    ]

    @staticmethod
    def get_list() -> List[str]:
        return Countries.__countries

def str_to_date(value: str) -> date:
    try:
        dt = datetime.datetime.strptime(value, "%d.%m.%Y")
        return date(dt.year, dt.month, dt.day)
    except:
        return None
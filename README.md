# IPL Match Data Extractor

## Project Overview
This project is designed to extract Indian Premier League (IPL) match data from the source ESPN Cricinfo ("https://www.espncricinfo.com/"). The data extraction is facilitated through Python, utilizing various libraries such as Scrapy, BeautifulSoup, and Pandas.
The main aim is to create a json file containing raw data about all the matches that have happened in the Cricket tournament IPL from its inception in 2008 to 2023.
This data can further be utilised for ML modelling and other such purposes.

## Files in the Repository

### File 1: - 'BS4 Ideation.ipynb'
This file is the basic ideation playground upon which the rest of the files are built. It is hihgly suggested to go through the file, copy it, try playing around and then maybe look at the other files.

### File 1: match_extractor
This file contains three main methods for extracting specific data from IPL matches.

#### Method 1: Batting Data Extractor
This method is responsible for extracting batting data from an IPL match and saving it in a JSON file.

#### Method 2: Bowling Data Extractor
Similar to the batting data extractor, this method focuses on extracting bowling data from an IPL match and saving it in a JSON file.

#### Method 3: Match All Data Extractor
This method takes an IPL match URL as input and extracts comprehensive data including batting, bowling, and other match details. The output is stored in a JSON file.

### File 2: all_match_data_extractor
This file acts as a central coordinator, utilizing the main methods from `match_extractor` to extract data for multiple matches. By providing a list of match URLs, this file extracts all relevant data for each match and compiles it into a single JSON file.

## How to Use
1. Clone the repository to your local machine.
2. Go through 'BS4 Ideation.ipynb' to understand the basic idea of extracting data of IPL matches.
3. Run the desired method from `match_extractor` to extract specific data for an IPL match.
4. Alternatively, use `all_match_data_extractor` by providing a list of match URLs to extract data for multiple matches into a consolidated JSON file.

## Dependencies
- Python
- Scrapy
- BeautifulSoup
- Pandas

## Source
The IPL match data is extracted from ESPN Cricinfo ("https://www.espncricinfo.com/").

Feel free to contribute or raise issues if you encounter any problems. Happy coding!

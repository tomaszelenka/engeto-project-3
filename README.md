### Engeto Project 3 - Election Scraper
## About the Project
This project is the third assignment for the Engeto Python Academy. It scrapes election data from a specified URL (pertaining to the 2017 elections in the Czech Republic; the link is [here](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)) and processes various election statistics, such as locations, counts of registered voters, envelopes, valid votes, and election results. Finally, it compiles the data and saves it to a CSV file.

# Built With
- Python 3
- BeautifulSoup4
- Requests

## Getting Started
To get a local copy up and running follow these simple steps.

# Prerequisites
- Python 3.6 or higher
- pip
- BeautifulSoup4
- Requests

You can install the necessary libraries using pip:
```pip install beautifulsoup4 requests```

# Installation
- Clone the repo:
```git clone https://github.com/tomaszelenka/engeto-project-3.git```
- Install Python packages:
```pip install -r requirements.txt```

## Usage
This script requires two command-line arguments:

1. A valid URL where the election data is located.
2. The file name for the output CSV.
# Running the Script
To run the script, use the following command:
```python projekt_3.py [URL] [output_file.csv]```

# Example
Here's an example command using a URL:

This command will scrape data from the provided URL and save the processed election results to election_data.csv:
```python projekt_3.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'vysledky-prostejov.csv'```
> Donwloading data from URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
> Saving to file: vysledky-prostejov.csv
> Exiting: Election-scraper




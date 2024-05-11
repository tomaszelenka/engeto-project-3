### Engeto Project 3 - Election Scraper
## About the Project
This project is the third assignment for the Engeto Online Python Academy. It scrapes election data from a specified URL and processes various election statistics such as codes, locations, registered voters, envelopes, and valid votes. Finally, it saves the compiled data to a CSV file.

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
Clone the repo:
```git clone https://github.com/your_username_/Project-Name.git```
Install Python packages:
```pip install -r requirements.txt```

## Usage
This script requires two command-line arguments:

- A valid URL where the election data is located.
- The file name for the output CSV.
# Running the Script
To run the script, use the following command:
python projekt_3.py [URL] [output_file.csv]

# Example
Here's an example command using a URL:

python projekt_3.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'election_data.csv'
This command will scrape data from the provided URL and save the processed election results to election_data.csv.

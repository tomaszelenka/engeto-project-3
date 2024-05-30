'''
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Zelenka
email: me@tomaszelenka.cz
discord: .toze.
'''

import sys
import requests_cache as rq
import csv
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

session = rq.CachedSession('http_cache', expire_after=300)
cache_http = {}

def get_soup(url):
    if url not in cache_http:
        response = session.get(url)
        response.encoding = 'utf-8'
        cache_http[url] = bs(response.text, 'html.parser')

    return cache_http[url]


def get_urls_with_x(soup):
    base_url = "https://volby.cz/pls/ps2017nss/"
    x_links = soup.find_all('a', string='X', href=True)
    x_urls = [urljoin(base_url, link['href']) for link in x_links]
    
    return x_urls



def get_data(soup, class_name, dict_key):
    rows = soup.find_all('tr')
    data_dict = {dict_key: []}
    for row in rows:
        element = row.find("td", {"class": class_name})
        if element:
            cleardata = element.text.strip()
            data_dict[dict_key].append(cleardata)
    return data_dict

def get_code(link) -> dict:
    return get_data(get_soup(link), "cislo", "code")

def get_location(link) -> dict:
    return get_data(get_soup(link), "overflow_name", "location")


def get_data_voters(urls):
    data = {
        'registered': [],
        'envelopes': [],
        'valid': []
    }
    
    for url in urls:
        soup = get_soup(url)

        if 'vyber' not in url:  # multichoice
            total_registered = 0
            total_envelopes = 0
            total_valid = 0
            sub_urls = get_sub_urls(url, 'cislo', 's1')  # URLs
            
            for sub_url in sub_urls:
                sub_soup = get_soup(sub_url)
                
                # Registered data
                value_elements_registered = sub_soup.find_all('td', class_='cislo', headers='sa2')
                for element in value_elements_registered:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_registered += int(cleardata)
                
                # Envelopes data
                value_elements_envelopes = sub_soup.find_all('td', class_='cislo', headers='sa3')
                for element in value_elements_envelopes:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_envelopes += int(cleardata)
                
                # Valid data
                value_elements_valid = sub_soup.find_all('td', class_='cislo', headers='sa6')
                for element in value_elements_valid:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_valid += int(cleardata)
                
            data['registered'].append(total_registered)
            data['envelopes'].append(total_envelopes)
            data['valid'].append(total_valid)
        else:
            # Registered data
            value_registered = soup.find("td", class_="cislo", headers="sa2")
            cleardata_registered = value_registered.text.strip().replace('\xa0', '').replace(' ', '') if value_registered else '0'
            data['registered'].append(int(cleardata_registered))
            
            # Envelopes data
            value_envelopes = soup.find("td", class_="cislo", headers="sa3")
            cleardata_envelopes = value_envelopes.text.strip().replace('\xa0', '').replace(' ', '') if value_envelopes else '0'
            data['envelopes'].append(int(cleardata_envelopes))
            
            # Valid data
            value_valid = soup.find("td", class_="cislo", headers="sa6")
            cleardata_valid = value_valid.text.strip().replace('\xa0', '').replace(' ', '') if value_valid else '0'
            data['valid'].append(int(cleardata_valid))

    return data


def get_results(urls):
    data = {}
    for url in urls:
        soup = get_soup(url)
        all_headers = [("t1sa1 t1sb2", "t1sa2 t1sb3"), ("t2sa1 t2sb2", "t2sa2 t2sb3")]   
        
        if 'vyber' not in url: # multichoice
                total_sum = {}
                sub_urls = get_sub_urls(url, 'cislo', 's1') # URLs
                
                for url in sub_urls:
                    sub_soup = get_soup(url)
                    for name_header, value_header in all_headers:
                        names = sub_soup.find_all('td', class_='overflow_name', headers=name_header) #DATA
                        values = sub_soup.find_all('td', class_='cislo', headers=value_header) #DATA
                        for name, value in zip(names, values):
                            name_text = name.text.strip()
                            value_text = value.text.strip().replace('\xa0', '').replace(' ', '')

                            if name_text in total_sum:
                                total_sum[name_text] = int(total_sum[name_text]) + int(value_text)
                            else:
                                total_sum[name_text] = int(value_text)

                for name_text, sum_value in total_sum.items():
                    if name_text in data:
                        data[name_text].append(sum_value)
                    else:
                        data[name_text] = [sum_value]       
        else:
            for name_header, value_header in all_headers:
                names = soup.find_all('td', class_='overflow_name', headers=name_header)
                values = soup.find_all('td', class_='cislo', headers=value_header)

                for name, value in zip(names, values):
                    name_text = name.text.strip()
                    value_text = value.text.strip()
                    if name_text in data:
                        data[name_text].append(value_text)
                    else:
                        data[name_text] = [value_text]

    return data


def get_sub_urls(url, class_name, headers_value):
    sub_soup = get_soup(url)

    td_elements = sub_soup.find_all('td', {'class': class_name, 'headers': headers_value})
    
    list_urls = []
    for td in td_elements:
        links = td.find_all('a')
        for link in links:
            if link.get('href'):
                list_urls.append(link.get('href')) 
    
    base_url = "https://volby.cz/pls/ps2017nss/"
    sub_x_urls = [urljoin(base_url, link) for link in list_urls]
    return sub_x_urls


def save_csv(data_code, data_location, data_multi, data_results, name_file):
    combined_dict = {**data_code, **data_location, **data_multi, **data_results}
    with open(name_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        headers = list(combined_dict.keys())
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';')
        writer.writeheader()
        
        max_length = max(len(values) for values in data_code.values())
        
        for i in range(max_length):
            row_data = {key: combined_dict[key][i] if i < len(combined_dict[key]) else '' for key in headers}
            writer.writerow(row_data)



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Error: Two arguments expected")
        sys.exit(1)

    link = sys.argv[1]
    name_file = sys.argv[2]

    if not (link.startswith('http://') or link.startswith('https://')):
        print("The first argument must be a valid URL starting with 'http://' or 'https://")
        sys.exit(1)

    expected_url_part = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj="
    if expected_url_part not in link:
        print(f"URL must contain '{expected_url_part}'.")
        sys.exit(1)

    if not name_file.endswith('.csv'):
        print("The file name must end with '.csv'")
        sys.exit(1)

    print(f"Downloading data from URL: {link}")
    get_html = get_soup(link)
    get_urlsx = get_urls_with_x(get_html)
    get_code_dict = get_code(link)
    get_location_dict = get_location(link)

    get_multidata_dict = get_data_voters(get_urlsx)

    get_results_dict = get_results(get_urlsx)

    print(f"Saving to file: {name_file}")
    save_csv(get_code_dict, get_location_dict, get_multidata_dict, get_results_dict, name_file)
    print(f"Exiting: Election-scraper")
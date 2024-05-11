'''
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Zelenka
email: me@tomaszelenka.cz
discord: .toze.
'''

import sys
import requests as rq
import csv
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def get_soup(url):
    response = rq.get(url)
    response.encoding = 'utf-8'
    return bs(response.text, 'html.parser')


def get_urls_with_x(soup):
    base_url = "https://volby.cz/pls/ps2017nss/"
    x_links = soup.find_all('a', string='X', href=True)
    x_urls = [urljoin(base_url, link['href']) for link in x_links]
    return x_urls

def get_code(link) -> dict:
    soup = get_soup(link)
    rows = soup.find_all('tr')
    dict_code = {'code': []}
    for row in rows:
        element = row.find("td", {"class": "cislo"})
        if element:
            cleardata = element.text.strip()
            dict_code['code'].append(cleardata)
        else:
            continue
    #print(dict_code)
    return dict_code

def get_location(link) -> dict:
    soup = get_soup(link)
    rows = soup.find_all('tr')
    dict_location = {'location': []}
    for row in rows:
        element = row.find("td", {"class": "overflow_name"})
        if element:
            cleardata = element.text.strip()
            dict_location['location'].append(cleardata)
        else:
            continue
    #print(dict_location)
    return dict_location

def get_registered(urls):
    dict_registered = {'registered': []}
    for url in urls:
        soup = get_soup(url)

        if 'vyber' not in url: # multichoice
            total_sum = 0
            sub_urls = get_sub_urls(url, 'cislo', 's1') # URLs
            
            for url in sub_urls:
                sub_soup = get_soup(url)
                value_elements = sub_soup.find_all('td', class_='cislo', headers='sa2') # DATA
                        
                for element in value_elements:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_sum += int(cleardata)
            
            dict_registered['registered'].append(total_sum)
        else:
            value = soup.find("td", class_="cislo", headers="sa2")
            cleardata = value.text.strip().replace('\xa0', '').replace(' ', '') if value else '0'
            dict_registered['registered'].append(int(cleardata))
    #print(dict_location)
    return dict_registered

def get_envelopes(urls):
    dict_envelopes = {'envelopes': []}
    for url in urls:
        soup = get_soup(url)

        if 'vyber' not in url: # multichoice
            total_sum = 0
            sub_urls = get_sub_urls(url, 'cislo', 's1') # URLs
            
            for url in sub_urls:
                sub_soup = get_soup(url)
                value_elements = sub_soup.find_all('td', class_='cislo', headers='sa3') # DATA
                        
                for element in value_elements:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_sum += int(cleardata)
            
            dict_envelopes['envelopes'].append(total_sum)
        else:
            value = soup.find("td", class_="cislo", headers="sa2")
            cleardata = value.text.strip().replace('\xa0', '').replace(' ', '') if value else '0'
            dict_envelopes['envelopes'].append(int(cleardata))
    #print(dict_location)
    return dict_envelopes

def get_valid(urls):
    dict_valid = {'valid': []}
    for url in urls:
        soup = get_soup(url)

        if 'vyber' not in url: # multichoice
            total_sum = 0
            sub_urls = get_sub_urls(url, 'cislo', 's1') # URLs
            
            for url in sub_urls:
                sub_soup = get_soup(url)
                value_elements = sub_soup.find_all('td', class_='cislo', headers='sa6') # DATA
                        
                for element in value_elements:
                    cleardata = element.text.strip().replace('\xa0', '').replace(' ', '')
                    total_sum += int(cleardata)
            
            dict_valid['valid'].append(total_sum)
        else:
            value = soup.find("td", class_="cislo", headers="sa2")
            cleardata = value.text.strip().replace('\xa0', '').replace(' ', '') if value else '0'
            dict_valid['valid'].append(int(cleardata))
    #print(dict_location)
    return dict_valid

def ger_results(urls):
    pass
    #IN PROGRESS :( :( :(


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


def save_csv(data_code, data_location, data_registered, data_envelopes, data_valid, name_file):
    combined_dict = {**data_code, **data_location, **data_registered, **data_envelopes, **data_valid}
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


    # Kontrola, zda je první argument validní URL začínající na http nebo https
    if not (link.startswith('http://') or link.startswith('https://')):
        print("The first argument must be a valid URL starting with 'http://' or 'https://")
        sys.exit(1)

    # Kontrola specifického řetězce v URL
    expected_url_part = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj="
    if expected_url_part not in link:
        print(f"URL must contain '{expected_url_part}'.")
        sys.exit(1)

    # Kontrola, zda jméno souboru končí na .csv
    if not name_file.endswith('.csv'):
        print("The file name must end with '.csv'")
        sys.exit(1)


    get_html = get_soup(link)
    get_urlsx = get_urls_with_x(get_html)
    get_code_dict = get_code(link)
    get_location_dict = get_location(link)
    get_registered_dict = get_registered(get_urlsx)
    get_envelopes_dict = get_envelopes(get_urlsx)
    get_valid_dict = get_valid(get_urlsx)



    save_csv(get_code_dict, get_location_dict, get_registered_dict, get_envelopes_dict, get_valid_dict, name_file)


   


   

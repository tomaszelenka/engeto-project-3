'''
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Zelenka
email: me@tomaszelenka.cz
discord: .toze.
'''

import sys
import requests
import csv
from bs4 import BeautifulSoup

def get_code(odkaz) -> list:
    response = requests.get(odkaz)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
       
    radky = soup.find_all('tr')

    data_code=[]
    for radek in radky:

        cislo_element = radek.find("td", {"class": "cislo"})

        if cislo_element:
                cislo = cislo_element.text.strip()
                data_code.append(cislo)
        else:
            continue 

    return data_code

def get_location(odkaz) -> list:
    response = requests.get(odkaz)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
       
    radky = soup.find_all('tr')

    data_location=[] 
    for radek in radky:
            
        nazev_element = radek.find("td", {"class": "overflow_name"})
        if nazev_element:
            nazev = nazev_element.text.strip()
            data_location.append(nazev)
        else:
            continue
            
    return data_location

def get_url_x(odkaz) -> list:
    response = requests.get(odkaz)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    odkazy = soup.find_all('a', string='X') 
    data_url_x = []
    for odkaz in odkazy:
        url = odkaz.get('href')
        url_with_http = "https://volby.cz/pls/ps2017nss/" + url
        data_url_x.append(url_with_http)    

    return data_url_x


def get_registered(user_link):
    registered_data = []
    for url in user_link:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'vyber' not in url:
            td_elements = soup.find_all('td', class_='cislo')
            total_sum = 0
            for td in td_elements:
                a_tag = td.find('a')                 
                if a_tag and a_tag.has_attr('href'):
                        full_url = "https://volby.cz/pls/ps2017nss/" + a_tag['href']

                        sub_response = requests.get(full_url)
                        sub_response.encoding = 'utf-8'
                        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                        value_elements = sub_soup.find_all('td', class_='cislo', headers='sa2')
                        
                        for element in value_elements:
                                cleaned_value = element.text.strip().replace('\xa0', '').replace(' ', '')
                                try:
                                    value = int(cleaned_value)
                                    total_sum += value
                                except ValueError:
                                    print(f"Chyba při konverzi hodnoty: {cleaned_value}")

            registered_data.append(total_sum)
            continue
        
        radky = soup.find_all('tr')
        for radek in radky:
           
            cislo_element = radek.find("td", class_="cislo", headers="sa2")
            if cislo_element:
                cislo = cislo_element.text.strip()
                registered_data.append(cislo)

    return registered_data

def get_envelopes(user_link):
    envelopes_data = []
    for url in user_link:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'vyber' not in url:
            td_elements = soup.find_all('td', class_='cislo')
            total_sum = 0
            for td in td_elements:
                a_tag = td.find('a')                 
                if a_tag and a_tag.has_attr('href'):
                        full_url = "https://volby.cz/pls/ps2017nss/" + a_tag['href']

                        sub_response = requests.get(full_url)
                        sub_response.encoding = 'utf-8'
                        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                        value_elements = sub_soup.find_all('td', class_='cislo', headers='sa3')
                        
                        for element in value_elements:
  
                                cleaned_value = element.text.strip().replace('\xa0', '').replace(' ', '')
                                try:
                                    value = int(cleaned_value)
                                    total_sum += value
                                except ValueError:
                                    print(f"Chyba při konverzi hodnoty: {cleaned_value}")

            envelopes_data.append(total_sum)
            continue
        
        radky = soup.find_all('tr')
        for radek in radky:
           
            cislo_element = radek.find("td", class_="cislo", headers="sa3")
            if cislo_element:
                cislo = cislo_element.text.strip()
                envelopes_data.append(cislo) 
    return envelopes_data

def get_valid(user_link):
    valid_data = []
    for url in user_link:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'vyber' not in url:
            td_elements = soup.find_all('td', class_='cislo')
            total_sum = 0
            for td in td_elements:
                a_tag = td.find('a')                 
                if a_tag and a_tag.has_attr('href'):
                        full_url = "https://volby.cz/pls/ps2017nss/" + a_tag['href']

                        sub_response = requests.get(full_url)
                        sub_response.encoding = 'utf-8'
                        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                        value_elements = sub_soup.find_all('td', class_='cislo', headers='sa6')
                        
                        for element in value_elements:

                                cleaned_value = element.text.strip().replace('\xa0', '').replace(' ', '')
                                try:
                                    value = int(cleaned_value)
                                    total_sum += value
                                except ValueError:
                                    print(f"Chyba při konverzi hodnoty: {cleaned_value}")

            valid_data.append(total_sum)
            continue

        
        radky = soup.find_all('tr')
        for radek in radky:
           
          
            cislo_element = radek.find("td", class_="cislo", headers="sa6")
            if cislo_element:
                cislo = cislo_element.text.strip()
                valid_data.append(cislo)  

    return valid_data


def get_results(urls):
    #IN PROGRESS :( :( :(
    results = {}  

    for url in urls:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        if 'vyber' not in url:
            td_elements = soup.find_all('td', class_='cislo')
            for td in td_elements:
                a_tag = td.find('a')                 
                if a_tag and a_tag.has_attr('href'):
                        full_url = "https://volby.cz/pls/ps2017nss/" + a_tag['href']

                        sub_response = requests.get(full_url)
                        sub_response.encoding = 'utf-8'
                        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')
                        rows = sub_soup.find_all('tr')
                        for row in rows:
                            name_cell = row.find('td', class_='overflow_name')
                            value_cell = row.find('td', class_='cislo', headers='t1sa2 t1sb3')

                            if name_cell and value_cell:
                                name = name_cell.text.strip()
                                cleaned_value = value_cell.text.strip().replace('\xa0', '').replace(' ', '')
                                try:
                                    value = int(cleaned_value)
                                    if name in results:
                                        results[name] += value
                                    else:
                                        results[name] = value
                                except ValueError:
                                    print(f"Chyba při konverzi hodnoty: {cleaned_value} pro {name}")
            continue
    
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.find_all('tr')
        for row in rows:
            name_cell = row.find('td', class_='overflow_name')
            value_cell = row.find('td', class_='cislo', headers='t1sa2 t1sb3')

            if name_cell and value_cell:
                name = name_cell.text.strip()
                cleaned_value = value_cell.text.strip().replace('\xa0', '').replace(' ', '')
                try:
                    value = int(cleaned_value)
                    if name in results:
                        results[name] += value
                    else:
                        results[name] = value
                except ValueError:
                    print(f"Chyba při konverzi hodnoty: {cleaned_value} pro {name}")
    
    return results




def save_csv(data_code, data_location, data_voters, data_envelopes, data_valid, data_results, name_file):
    with open(name_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Číslo', 'Název', 'registered', 'envelopes', 'valid', data_results.keys()])
        for code, location, voters, envelopes, valid, data_res in zip(data_code, data_location, data_voters, data_envelopes, data_valid, data_results):
            writer.writerow([code, location, voters, envelopes, valid, data_res])

        # writer.writerow(data_results.keys())
        # for total in data_results.items():
        #     writer.writerow([total])


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Chyba: očekávají se dva argumenty.")
        print("Použití: python skript.py 'odkaz' 'jmeno_souboru.csv'")
        sys.exit(1)

    link = sys.argv[1]


    name_file = sys.argv[2]


    list_registered = get_registered(get_url_x(link))
    list_envelopes = get_envelopes(get_url_x(link))
    list_valid = get_valid(get_url_x(link))
    results = get_results(get_url_x(link))

    save_csv(get_code(link),get_location(link), list_registered, list_envelopes, list_valid, results, name_file)

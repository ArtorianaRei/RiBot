from bs4 import BeautifulSoup
import requests
import re
import gspread
import pandas as pd

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open('ZeakTheBot')

# Function to change the case of perk to capitalize the first letter
# except for certain words
def case_except(s):
    exceptions = ['a', 'an', 'of', 'the', 'is', 'for', 'de', 'from', 'with']
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

# Function to grab the current perks in the Shrine of Secrets and when it will refresh
def shrine_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    sos = soup.find_all('div', class_='sosPerkDescName')
    sos_list = []

    for i in range(len(sos)):
        sos_list.append(sos[i].get_text(separator=' ', strip=True))

    sos_s = ', '.join(sos_list)
    sos_time = soup.find('span', class_='luaClr clr clr4').get_text()
    
    return sos_s, sos_time

# Function to grab all the current killers from dbd fandom wiki
def killer_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    killers = soup.find_all('div', id='fpkiller')[0].get_text(', ', strip=True)[14:]
    
    return killers

# Function to grab all the current survivor names from dbd fandom wiki
def survivor_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    survivors = soup.find_all('div', id='fpsurvivors')[0].get_text(', ', strip=True)[16:]
    
    return survivors

# Function to scrape the perk from the dbd fandom wiki
def perk_scrape(perk):
    wks = sh.worksheet('Perks')
    perks_df = pd.DataFrame(wks.get_all_records())

    if perks_df['perk_name'].eq(perk).any():
        perkurl = perks_df.loc[perks_df['perk_name'] == perk, 'perk_url'].values[0]
    else:
        perkurl = case_except(perk).strip().replace(" ", "_")

    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=perkurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    perk_name = soup.find('h1').get_text(strip=True)
    perk_desc = soup.find('div', class_='formattedPerkDesc').get_text(separator=' ', strip=True).replace('\n', '')

    return perk_name, perk_desc

def status_scrape(status):
    status = status.capitalize()

    url = "https://deadbydaylight.fandom.com/wiki/Status_HUD"
    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, "html.parser")

    status_all = soup.find_all('td')

    status_list = []
    status_name = []

    for i in range(len(status_all)):
        status_list.append(status_all[i].get_text(separator=' ', strip=True))
        try:
            status_name.append(re.search('The (.*?) Status', status_list[i]).group(1))
        except:
            status_name.append(status_list[i])

    status_df = pd.DataFrame({'status_name': status_name, 'status_desc': status_list})
    
    status_desc = status_df.loc[status_df['status_name'] == status, 'status_desc'].values[0]

    return status, status_desc

perkhelp = 'Try typing !perk <perk name> to get a description of the perk. ie "!perk spine chill"'
statushelp = 'Try typing !status <status name> to get a description of the status. ie "!status exhausted"'
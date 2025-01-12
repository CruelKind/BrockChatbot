import sched
import requests,sys
from bs4 import BeautifulSoup
import pathlib

WORKING_DIRECTORY = str(pathlib.Path().resolve())



## Returns the soup of a url
def url2Soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')

## Returns the soup of an html file
def file2Soup(fileLocation):
    with open(fileLocation, 'r') as f:
        page = f.read()
    return BeautifulSoup(page, 'html.parser')

## Returns the soup of an html file with utf8 encoding
def file2Soup_utf(filelocation):
    with open(filelocation, encoding='utf8') as f:
        page = f.read()
    return BeautifulSoup(page, 'html.parser')

## Remove all trailing spaces from list items and space unicodes
def removeUnicodeSpace(list):
    return [i.replace(u"\xa0",u"").strip() for i in list]

## Returns scraped player+sport data from gemspro 2019 html for testing pruposes
def scrapeAthleteData_gemspro(filename="allAthletes.htm"):
    soup = file2Soup(WORKING_DIRECTORY+"\\backend\\allAthletes.htm")
    table = soup.find('table',id="ctl00_ContentPlaceHolder1_tblParticipant") 
    athletes_sports = [i.get_text() for i in table.find_all("td")]
    athletes_sports = removeUnicodeSpace(athletes_sports)
    athletes_sports = grabEveryN_fromList(athletes_sports,2)
    return athletes_sports


def scrapeCompetitors_nigaragames():
    soup = url2Soup("https://niagara2022games.ca/sports/#Athletics")
    table = soup.find("div",{'class':"col-sm-12 col-lg-9"}) 
    Athletes = [i.get_text() for i in table.find_all("li")]
    Athletes = removeUnicodeSpace(Athletes)
    return Athletes

def grabEveryN_fromList(list,n):
    return [list[i*n:i*n+n] for i in range(int(len(list)/n))]

## Return the schedule on niagara games website.
def scrapeSchedule_niagaragames():
    soup = file2Soup(WORKING_DIRECTORY+"\\backend\\schedule.htm")
    table = soup.find('tbody', id = "ctl00_ctl00_ContentPlaceHolderBasicMaster_ContentPlaceHolder1_secGroup1_1_secGroup1_1_SectionContent") 
    schedule = [i.get_text() for i in table.find_all("tr")]
    stringSchedule="".join(schedule)
    schedule= stringSchedule.split("\n")
    schedule = [i for i in schedule if i]
    schedule = grabEveryN_fromList(schedule,5)
    

    return schedule

def scrape_general_info():
    soup_wiki = file2Soup_utf("C:\\Users\\Yujie\\OneDrive\\Desktop\\Computer Science\\COSC 4P02\\BrockChatbot\\backend\\canadaGamesWiki.htm")
    wiki_info_box = soup_wiki.find_all('p')
    wiki_info = [i.get_text() for i in wiki_info_box]
    #First 2 indices of info holds the most important information
    #print(wiki_info[0] + wiki_info[1])

    soup_FAQ = file2Soup_utf("C:\\Users\\Yujie\\OneDrive\\Desktop\\Computer Science\\COSC 4P02\\BrockChatbot\\backend\\canadaGamesFAQ.htm")
    cg_containers = soup_FAQ.find_all('div', class_=('cg-container'))
    FAQ = []
    for cg_container in cg_containers:
        FAQ = FAQ + cg_container.find_all('div', attrs={'data-w-id' : True})
    FAQ_results = [i.get_text() for i in FAQ]
    #Index 5 and 7 holds info not from wiki page in general FAQ page
    #print(FAQ_results[5] + FAQ_results[7])

    general_info = wiki_info[0] + wiki_info[1] + FAQ_results[5] + FAQ_results[7]
    print(general_info)
    return general_info

if __name__ == "__main__":
    ## Example use cases:
    
    #scrape_general_info()

    athlete_table = scrapeAthleteData_gemspro()
    print(athlete_table)

    #compeititors = scrapeCompetitors_nigaragames()
    #print(len(compeititors))

    #schedule = scrapeSchedule_niagaragames()
    #print(schedule)
    pass

from bs4 import BeautifulSoup
import requests, time, re

SCRAPE_IDS = True
REGION_SPECIFIC_SITE_URL = 'http://www.petango.com/Forms/ShelterSearchResults.aspx?z=10021&d=10&sh=0&s=4&g=All&size=All&c=All&a=All&dec=All&p=False&v=False&adoptD=False&adoptC=False&adoptO=False&sid=0&zs=True&ht=False'
NUM_REQUEST_ATTEMPTS = 5

def fetch_page_listing():

    # Get and parse page containing shelter list
    for attempt in range(NUM_REQUEST_ATTEMPTS):
        try:
            res = requests.get(REGION_SPECIFIC_SITE_URL, timeout=5)
            break
        except:
            time.sleep(5) # Wait 5 seconds before trying again

    page = BeautifulSoup(res.text,"html.parser")
    return page
    
    
if SCRAPE_IDS:
    
    regionList = fetch_page_listing()
    shelterUrls = regionList.findAll('a',{'class': 'btn-moredetails w90'})
    
    SHELTER_IDS = {}
    for shelter in shelterUrls:
        shelterPage = requests.get(shelter.attrs['href'])
        pageSoup = BeautifulSoup(shelterPage.text, "html.parser")
        listingLink = pageSoup.find('a',{'class': 'btn'}).attrs['href']
        pagePattern = re.compile(r'sh=([0-9]*)')
        pageId = pagePattern.search(listingLink)
        listingNumber = pageId.group(1).strip()
        SHELTER_IDS[shelter.attrs['href'].split('/')[-1]] = listingNumber

else:

    SHELTER_IDS = {
        '92ndStASPCA': 1950,
        'DogHabitRescue': 2903,
        'anjellicleCatsRescue': 994,
        'seanCaseyRescue': 408
        }
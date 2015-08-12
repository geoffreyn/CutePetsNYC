from bs4 import BeautifulSoup
import requests, time, re

ZIPCODE = '10021'
DISTANCE_IN_MILES = '10'

SCRAPE_IDS = True
SITE_URL = 'http://www.petango.com/Forms/ShelterSearchResults.aspx'
NUM_REQUEST_ATTEMPTS = 5


def fetch_page_listing():

    params = {
        'z': ZIPCODE,
        'd': DISTANCE_IN_MILES
    }

    # Get and parse page containing shelter list
    for attempt in range(NUM_REQUEST_ATTEMPTS):
        try:
            res = requests.get(SITE_URL, params, timeout=5)
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

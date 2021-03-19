import asyncio
import requests
from bs4 import BeautifulSoup



async def main():
    mainPage = 'https://burnout.fandom.com/wiki/Vehicles_(Burnout_Paradise)'
    response = requests.get(mainPage)
    page_source = response.text
    car_list_page = BeautifulSoup(page_source, 'html.parser')
    car_list_page = car_list_page.find_all('table')
    car_list_page = car_list_page.find('tr')


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main())
    finally:
        event_loop.close()
import asyncio
import requests
import os
from bs4 import BeautifulSoup


def flatten(l):
    return [item for sublist in l for item in sublist]

def create_data_directory():
    cwd = os.getcwd();
    data_path = cwd + '/data'
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    icons_path = data_path + '/icons'
    if not os.path.exists(icons_path):
        os.mkdir(icons_path)
    return data_path

def get_file_name(path):
    return os.path.basename(path)

def download_image(url, file_save_path):
    img_data = requests.get(url).content
    with open(file_save_path, 'wb+', ) as file:
        file.write(img_data)


def pull_car_data_from_table_cells(row, data_path, host):
    try:
        image = row[0]
        image = image.find('img')
        image_name = image.get('data-image-name')
        print('Donloading {} data'.format(image_name))
        image_url = image.get('data-src')
        image_path = data_path + '/icons/' + image_name
        car_stats = row[1]
        car_page = car_stats.find('a')
        car_speed = int(car_stats.find(string='Speed:').find_parent('small').nextSibling[-1])
        car_boost = int(car_stats.find(text='Boost:').find_parent('small').nextSibling[-1])
        car_strength = int(car_stats.find(text='Strength:').find_parent('small').nextSibling[-1])
        download_image(image_url, image_path)
        return {
            name: car_page.string,
            stats: {
                speed: car_speed,
                boost: car_boost,
                strength: car_strength
            },
            icon: image_path,
            wiki: host + car_page.attrs.href
        }

    except:
        return {}


async def main():
    data_path = create_data_directory()
    host = 'https://burnout.fandom.com'
    mainPage = host + '/wiki/Vehicles_(Burnout_Paradise)'
    response = requests.get(mainPage)
    page_source = response.text
    car_list_page = BeautifulSoup(page_source, 'html.parser')
    car_list_page = car_list_page.find_all('table')
    car_list_page = flatten(list(map(lambda table: table.find_all('tr'), car_list_page)))
    car_list_page = list(map(lambda row: row.find_all('td'), car_list_page))
    car_list_page = list(filter(lambda el: el != [], car_list_page))
    car_list_page = list(map(lambda row: pull_car_data_from_table_cells(row, data_path, host), car_list_page))


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main())
    finally:
        event_loop.close()
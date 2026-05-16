# blinkkit
# big basket
# jio mart


#     for i in containers:
# #  -----------url = 'https://www.jiomart.com/c/groceries/2'
#         name = i.find('span', class_='clsgetname').text
#         price = i.find('span', id='final_price').text
#         image = i.find('img', id='product-image-photo lazyautosizes lazyloaded')

#         print(f' Jiomart, {name},{price}, {image}\n')
# dataextract()
    # f.write(f' Jiomart, {name},{price}, {image}\n')
    # print('\n')
# f.close()
# ----------------------------------------------------------------------


def nextpage(url):
    for i in range(1,5):   
        only_url = url.split('=')[-2]
        urls = only_url+'='+str(i)
        print(urls)

        response = requests.get(urls)
        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.find_all('div', class_='col-md-3 p-0')

        for i in containers:
            name = i.find('span', class_='clsgetname').text
            price = i.find('span', id='final_price').text
            image = i.find('img', id='product-image-photo lazyautosizes lazyloaded')

            # print(f' Jiomart, {name},{price}, {image}\n')
            # f.write(f' Jiomart, {name},{price}, {image}\n')
        # print('\n')
    # f.close()
        
# nextpage(url)

# -----------------------------------------------------------------------


import requests
from bs4 import BeautifulSoup

url = 'https://www.jiomart.com/c/groceries/2?prod_mart_groceries_products_popularity%5Bpage%5D=1'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
containers = soup.find_all('div', class_='col-md-3 p-0')


def nextpage(url):
    for i in range(1,21):   
        int = url.split('=')[-1]
        only_url = url.split('=')[-2]
        url = only_url+'='+str(i)
        print(url)

# nextpage(url)

def data(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all('div', class_='col-md-3 p-0')

    for i in containers:
        name = i.find('span', class_='clsgetname').text
        price = i.find('span', id='final_price').text
        image = i.find('img', id='product-image-photo lazyautosizes lazyloaded')

        print(f' Jiomart, {name},{price}, {image}\n')
        
data(url)



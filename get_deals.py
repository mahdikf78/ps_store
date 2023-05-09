import requests
import json
import os
#This Library is for Reading HTML
from bs4 import BeautifulSoup

os.system('color')
print('\033[33mSearch in Playstation GOLDEN WEEK\033[0m')

def sent_sms():
    api = '64547446757776434366792B364836556E766F2B3351555133512F7A664A68363331394B6A5A45626E38733D'
    url = 'https://api.kavenegar.com/v1/{}/sms/send.json'.format(api)
    infos = {'receptor' : '09923459499','message' : 'metti'}
    rep = requests.post(url, data=infos)
    if rep.status_code == 200:
        print('cart sent with sms to {}'.format('09923459499'))
#sent_sms()

games = []
#link = []
def get_deals(url):
    number = 0
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    #This is the Main <li> tag that all products is in that
    for products in soup.find_all('li', class_='psw-l-w-1/2@mobile-s psw-l-w-1/2@mobile-l psw-l-w-1/6@tablet-l psw-l-w-1/4@tablet-s psw-l-w-1/6@laptop psw-l-w-1/8@desktop psw-l-w-1/8@max'):
        #Find Original Price
        for org_price in products.find_all('s', class_='psw-c-t-2'):
            orginal_price = org_price.get_text()
        #Find Names
        for names in products.find_all('a'):
            n = json.loads(names['data-telemetry-meta'])
            number = number + 1
            print('\033[33m-',number,':',n['name']+'\033[0m')
            games.append(f"{n['name'].lower()}, {n['price']}")
            #ignore errors for free games
            try :
                #Combine Original Price and New Price
                print(f"{orginal_price} ===> {n['price']}")
            except:
                continue
        #find consoles
        for consoles in products.find_all('span', class_='psw-platform-tag psw-p-x-2 psw-l-line-left psw-t-tag psw-on-graphic'):
            print(consoles.get_text())
        """
        #Find Images
        for img in products.find_all('img', class_='psw-top-left psw-l-fit-cover'):
            print(img.get('src'))
        """
        #Find links
        for links in products.find_all('a', class_='psw-link psw-content-link'):
            print(f"https://store.playstation.com/{links.get('href')}")
            #link.append(links.get('href'))
        print('------------')

def show_cart():
    file = open('cart.txt','r')
    text = file.read()
    print(text)
"""
def get_date():
    url = f'https://store.playstation.com/{link[0]}'
    print(url)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')

    for dates in soup.find_all('span', class_='psw-t-overline psw-t-bold psw-l-line-left psw-fill-x'):
        a = dates.get_text()
        print('\033[36m'+a[a.find('O'):][:a.rfind('3')]+'\033[0m')
"""
def search_games():
    while True:
        res = input('Search Game by Name : ')
        if res == '.':
            games.clear()
            search_pages()
            break
        elif res == '--c':
            print('')
            show_cart()
        res1 = [item for item in games if res in item]
        for i in res1:
            print('\033[32m',res1.index(i),'-',i,'\033[0m')
        
        #create cart in txt file
        def add_cart():
            if len(res1) >= 1 :
                while True:
                    add = input('type index to add cart : ')
                    if add == '.':
                        break
                    else:
                        try:
                            print(res1[int(add)])
                            file = open('cart.txt','a')
                            file.write('- '+res1[int(add)]+'\n')
                            print('added to cart.txt')
                            file.close()
                        except:
                            print('wrong index !')
        add_cart()

def search_pages():
    while True:
        page = input('what page? : ')
        try:
            if page == '--c':
                print('')
                show_cart()
            else:
                page = int(page) + 1
                url = input('paste url here : ')
                del_part = url.rfind('1')
                for i in range(1,int(page)):
                    get_deals(url[:del_part]+str(i)+'?FULL_GAME=storeDisplayClassification')
                break
        except:
            print('\033[31mwrong input\033[0m')
    print('')
    print('\033[36mFind',len(games),'Games\033[0m')
    print('')
    search_games()

search_pages()

#add sms
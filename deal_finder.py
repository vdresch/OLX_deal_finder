############################        Librarys        ############################

import requests
import re
import time
import random
import json
import pandas as pd
import yaml
import smtplib

############################        Constants        ###########################

#Header
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

############################           Code          ###########################

#This function will scrap the pages for links where the price is under the goal. 
# If it is, it will call a funtion that will scrap more info about the add and another to notify the user.
def get_listings(page_OLX, price_goal, max_pages):
    #Pagination changes depending on how the surch was made
    if(re.search('q=', page_OLX)):
        string_pagination = "&o="
    else:
        string_pagination = "?o="

    #Dataframe where the good ads will be stores
    deals = pd.DataFrame()

    #Interate throw pages
    for i in range(max_pages):
        print("Searching page %i" % int(i+1))
        page_request = page_OLX + string_pagination + str(i+1)
        page = requests.get(page_request, stream=True, headers=headers)
        #Tests if there are no more ads
        if (re.search('Nenhum anúncio foi encontrado.', page.text)):
            break
        #Get all the ads
        ads = re.search('data-json=\"(.*)}', page.text).group(1)
        ads = ads.replace("&quot;", "\"")
        ads = ads.replace("\"desktop\"", "\"desktop\"}")
        ads = json.loads(ads)

        #Look throw the ads on the page
        for ad in ads['listingProps']['adList']:
            #If price is good, open the ad
            if 'isPubListingItem' not in ad:
                if(int(ad['price'].replace('R$', '').replace('.','')) < price_goal):
                    print("Deal found!")
                    deals = deals.append(get_info_page(ad['url']), ignore_index=True)
        
        time.sleep(random.randint(3,4)*0.45234)

    return(deals)
    

#If it gets into this function, it's a good deal and we want to know more about it.
#The page will be scraped and an alert will be sent.
def get_info_page(link):
    #Open ad page
    time.sleep(random.randint(3,4)*0.45234)
    ad_page = requests.get(link, stream=True, headers=headers)

    #Get the json with all the info
    data = re.search('data-json=\"(.*)}', ad_page.text).group(1)
    data = data.replace("&quot;", "\"")
    data = data.replace("\"desktop\"", "\"desktop\"}")
    data = data.split(",\"currentZipcode", 1)[0]
    data = json.loads(data)

    #Process the info
    title = data['ad']['subject']
    description = data['ad']['body']
    price = data['ad']['priceValue']
    old_price = data['ad']['oldPrice']
    owner = data['ad']['user']['name']
    phone = data['ad']['phone']['phone']

    ad_info = {'title': title, 'description': description, 'price': price,
        'old_price': old_price, 'owner': owner, 'phone': phone, 'url': link}

    return(ad_info)




#Sends an alert with the info from de ad.
def alert(deals, email):
    try:
        server = smtplib.SMTP(email['server'], email['port'])
        sent_from = email['email']
        to = email['email']
        subject = "Deals found!"
        #body = open("email.html").read()

    except Exception as e:
        print(e)

if __name__=="__main__":

    #Page of the product you want a deal
    page_OLX = "https://rs.olx.com.br/autos-e-pecas/motos/bmw/g/650"
    #Price goal
    price_goal = 25000

    #Config some variables
    config = yaml.load(open('config.yml'))
    email = {'email': config['email'], 'password': config['password'], 'server': config['server'], 'port': config['port']}
    max_pages = config['max_pages']

    #Get the deals
    deals = get_listings(page_OLX, price_goal, max_pages)

    #Emits an email alert with all the deals found
    alert(deals, email)
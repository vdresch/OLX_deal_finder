############################        Librarys        ############################


import requests
import re


############################        Constants        ###########################

#Page of the product you want a deal
page_OLX = "https://rs.olx.com.br/autos-e-pecas/motos/bmw/g/650"

#Price goal
price_goal = 20000

#Max number of pages that will be scraped. It's used to prevent an infinite loop.
max_pages = 10

#Header
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

############################           Code          ###########################

#Pagination changes depending on how the surch was made
if(re.search('q=', page_OLX)):
    string_pagination = "&o="
else:
    string_pagination = "?o="

#This function will scrap the pages for links where the price is under the goal. 
# If it is, it will call a funtion that will scrap more info about the add and another to notify the user.
def get_listings():

    for i in range(max_pages):
        page_request = page_OLX + string_pagination + i
        page = requests.get(page_request, stream=True, headers=headers)
        #Tests if there are no more ads
        if (re.search('Nenhum anúncio foi encontrado.', page.text)):
            break
        #Get all the ads
        ads = re.search('data-json=\"(.*)}', page_request.text).group(1)

#If it gets into this function, it's a good deal and we want to know more about it.
#The page will be scraped and an alert will be sent.
def get_info_page(page):
    pass

#Sends an alert with the info from de ad.
def alert():
    pass

if __name__=="__main__":
    pass
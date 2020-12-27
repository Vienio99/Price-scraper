import os, selenium, requests, bs4, re
from selenium import webdriver
os.system('cls')


#Function which finds best deal on given category

def bestDeal(categoryLink):
    browser = webdriver.Firefox()
    browser.get(categoryLink)
    numPages = browser.find_elements_by_class_name('paging-number')
    numPages = int(numPages[-1].text)

    biggestDifference = 0
    bestDeal = ''
    bestDeals = {}

    for page in range(1, numPages + 1):
        browser.get(categoryLink[:-6] + f',strona-{page}.bhtml')

        foundElems = browser.find_elements_by_class_name('product-prices-box')

        linksList = []

        for i in range(1, len(foundElems) + 1):
            foundLinks = browser.find_element_by_css_selector(f'#products > div:nth-child({i}) > div.product-box.js-UA-product > div > div.product-main > div.product-header > h2 > a')
            foundLink = foundLinks.get_attribute('href')
            linksList.append(foundLink)
        
        for i in range(len(foundElems)):
            foundElemsText = foundElems[i].text
            foundPrices = re.findall(r'[0-9]+\s[0-9]+\s[Zz][Łł]|[0-9]+\s[Zz][Łł]', foundElemsText)
            if len(foundPrices) > 2:
                priceDifference = foundPrices[2]
                priceDifference = re.findall(r'[0-9]+', priceDifference)
                priceDifference = ''.join(priceDifference)
                if int(priceDifference) > biggestDifference:
                    biggestDifference = int(priceDifference)
                    bestDeal = linksList[i]

                    bestDeals[f'{linksList[i]}'] = int(priceDifference)
            else:
                continue
        
        print(biggestDifference)
        print(bestDeal)
        print(bestDeals)
    browser.close()
        




#Put link here

bestDeal('https://www.euro.com.pl/monitory-led-i-lcd,a1.bhtml')






#Multi threads



#Dictionary with ten best prices links as keys and 
#difference of regular price and promo price as values 
bestDealsLinks = []


#Function which sends best deals via gmail




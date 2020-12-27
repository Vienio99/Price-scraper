import os, selenium, requests, bs4, re, threading, math
from selenium import webdriver
os.system('cls')


#Function which get page number from a category and runs bestDeal function

def getPageNumber(categoryLink):
    browser = webdriver.Firefox()
    browser.get(categoryLink)
    numPages = browser.find_elements_by_class_name('paging-number')
    numPages = int(numPages[-1].text)

    #Divides numPages for threading
    if numPages < 5:
            bestDeal(categoryLink, 1, numPages + 1)
    else:
        downloadThreads = []   
        numPagesDivision = numPages / 5
        numPagesDivisionRoundDown = math.floor(numPagesDivision)

        numPagesThreading = numPagesDivisionRoundDown * 5

        bestDeal(categoryLink, numPagesThreading + 1, numPages + 1)
        for i in range(1, numPagesThreading + 1, 5):
            start = i
            end = i + 5
            downloadThread = threading.Thread(target=bestDeal, args=(categoryLink, start, end))
            downloadThreads.append(downloadThread)
            downloadThread.start()
        for downloadThread in downloadThreads:
            downloadThread.join()
            print('Done.')


#Function which finds best deal in given category
def bestDeal(categoryLink, startPage, endPage):
    browser = webdriver.Firefox()

    biggestDifference = 0
    bestDeal = ''
    bestDeals = {}
    print(startPage)
    print(endPage)
    #Iterate over every given page
    for page in range(startPage, endPage):
        browser.get(categoryLink[:-6] + f',strona-{page}.bhtml')

        #Find links of the products
        foundElems = browser.find_elements_by_class_name('product-prices-box')

        linksList = []

        for i in range(1, len(foundElems) + 1):
            foundLinks = browser.find_element_by_css_selector(f'#products > div:nth-child({i}) > div.product-box.js-UA-product > div > div.product-main > div.product-header > h2 > a')
            foundLink = foundLinks.get_attribute('href')
            linksList.append(foundLink)

        #Find highest difference in price 
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

getPageNumber('https://www.euro.com.pl/monitory-led-i-lcd,a1.bhtml')


#Function which sends best deals via gmail




from requests import get
from bs4 import BeautifulSoup
import time

start = time.time() # Timer to measure programs performance

url = 'https://www.currys.co.uk/product.xml' # Main product file
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

products = html_soup.find_all('loc')
print("Product count: ", len(products))  # Total link count in the main product file
print("\n****************************************")

counter = 0 # Loops through the products on the main product file to get the sku, name and price
for i in products:
    counter += 1
    if counter > 10:
        break
    url2 = i.text
    response = get(url2) # Loads the product page ready for scraping

    html_soup2 = BeautifulSoup(response.text, 'html.parser')
    type(html_soup2)

    productSku = html_soup2.find(attrs={"class": "prd-code"}) # Finds the SKU (product code)
    try:
        print(productSku.text)
    except:
        #print("Can't find a SKU number!")
        continue

    productName = html_soup2.find(attrs={"class":"page-title nosp"}) # Finds the name of the item
    try:
        print(productName.text.replace('\n', ' ')[1:-1])
    except:
        #print("Cant find the product name!")
        continue

    productPrice = html_soup2.find(attrs={"data-key": "current-price"}) # Finds the price of the item
    try:
        print(productPrice.text)
    except:
        #print("Can't find the price!")
        continue

    print("++++++++++++++++++++++++++++++++++++++++++++")

end = time.time()

print(end - start)

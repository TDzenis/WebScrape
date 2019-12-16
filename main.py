from requests import get
from bs4 import BeautifulSoup
import time

start = time.time()

url = 'https://www.currys.co.uk/product.xml'
response = get(url)

html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)

products = html_soup.find_all('loc')
print(len(products))  # found item count

counter = 0
for i in products:
    counter += 1
    if counter > 10:
        break
    url2 = i.text
    response = get(url2)

    html_soup2 = BeautifulSoup(response.text, 'html.parser')
    type(html_soup2)

    name = html_soup2.find('h1').find_all('span')
    fullName = ""
    for i in name:
        fullName += i.text
        fullName += " "
    print(fullName)

    price = html_soup2.find(attrs={"data-key": "current-price"})
    try:
        print(price.text)
    except:
        print("There is no price!!")

end = time.time()
print(end - start)

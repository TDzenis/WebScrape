from requests import get
from bs4 import BeautifulSoup
import time
import mysql.connector
from mysql.connector import errorcode

url = 'https://www.currys.co.uk/product.xml'  # Main product file
DB_NAME = 'products'


def get_html(linkToWebsite):
    response = get(linkToWebsite)
    html = BeautifulSoup(response.text, 'html.parser')
    return html


def connect_db(usr, pwd, hst):
    cnx = mysql.connector.connect(user=usr, password=pwd,
                                  host=hst)
    return cnx

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print("DB connected succesfuly")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)




start = time.time()  # Timer to measure programs performance

products = get_html(url).find_all('loc')
print("Product count: ", len(products))  # Total link count in the main product file
print("\n****************************************")

counter = 0  # Loops through the products on the main product file to get the sku, name and price
for i in products:
    counter += 1
    if counter > 1:
        break
    productSku = get_html(i.text).find(attrs={"class": "prd-code"})  # Finds the SKU (product code)
    productName = get_html(i.text).find(attrs={"class": "page-title nosp"})  # Finds the name of the item
    productPrice = get_html(i.text).find(attrs={"data-key": "current-price"})  # Finds the price of the item
    try:
        print(productSku.text)
        print(productName.text.replace('\n', ' ')[1:-1])
        print(productPrice.text)
    except:
        continue

    print("++++++++++++++++++++++++++++++++++++++++++++")

    # time.sleep(5) # Sleep timer to prevent the website blocking the scraping.

end = time.time()

print(round(end - start, 2), 'seconds')


cnx = connect_db('USERNAME', 'PASSWORD', 'HOST')


try:
    cnx.cursor().execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cnx.cursor())
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

cnx.close()

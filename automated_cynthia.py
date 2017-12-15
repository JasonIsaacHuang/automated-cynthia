from bs4 import BeautifulSoup
import csv
import re
import requests
from scrapers import ratecity

def write_products_to_csv(dict_list):
    keys = dict_list[0].keys()
    f = open('products.csv','w')
    writer = csv.DictWriter(f,keys)
    writer.writeheader()
    writer.writerows(dict_list)
    f.close()

def main(argv):
    products = ratecity.get_list_of_all_products()
    write_products_to_csv(products)

if __name__ == "__main__":
    main(sys.argv)

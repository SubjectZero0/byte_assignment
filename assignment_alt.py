import requests

#---------------------------------------------

#Define the list of urls 
url_list = ["https://dummyjson.com/products","https://dummyjson.com/products/categories"]

#get the json for products and categories
products_list = requests.get(url_list[0]).json()['products']
categories = requests.get(url_list[1]).json()

#----------------------------------------------

#group the products by categories
grouped_by_cat = {}

for category in categories:
    grouped_by_cat[category]=[]

for product in products_list:
    grouped_by_cat[product['category']].append(product)


#initialize dictionaries for the most expensive items and the sum of stock by category
most_expensive_by_cat = {}
item_stock_by_cat = {}

#loop through the categories of the grouped dictionary and get the most expensive items and sum of stock available
for category in grouped_by_cat:

    if len(grouped_by_cat[category]) > 0 : #we need to only get the non empty categories
        
        most_expensive_by_cat[category] = grouped_by_cat[category][0] #for every category, initialize a most expensive item
        stock_sum = 0 #also initialize the stock

        #loop through every product by its category
        for product in grouped_by_cat[category]:
            #get the most expensive item so far
            if product['price'] > most_expensive_by_cat[category]['price']:
                most_expensive_by_cat[category] = product
                
            #get the final stock sum for every category
            stock_sum += product['stock']
            item_stock_by_cat[category]=stock_sum


#find and display the highest price of all the items
price_list=[]
for product in most_expensive_by_cat.values():
    price_list.append(product['price']) 

print(f"The highest price of any item is: {max(price_list)}")

#---------------------------------------------------------------

#write a txt. Here i struggle with appropriate spacing.
with open('stats_alt.txt', 'w') as f:
    
    f.write("CATEGORY           MOST EXPENSIVE PRODUCT           PRICE   CAT STOCK\n")
    f.write("----------------   -------------------------------  -----   ---------\n")
    for category in list(most_expensive_by_cat.keys()):
        f.write(f"{category:{10}} {most_expensive_by_cat[category]['title']:{20}} {most_expensive_by_cat[category]['price']:{10}} {item_stock_by_cat[category]:{5}}\n")
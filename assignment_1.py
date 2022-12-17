import requests
import pandas as pd
#------------------------------------------

def get_json(urls):
    #helper function to get a json response from a list of urls
    res_json=[]
    for url in urls:
        res_json.append(requests.get(url).json())
    return res_json

#------------------------------------------------------------

# create a list of urls for the data
url_list = ["https://dummyjson.com/products","https://dummyjson.com/products/categories"]

#create a list for all the response data
data_list = get_json(url_list)


#create a pandas Dataframe with all the products
products_DF = pd.DataFrame(data_list[0]['products'])

#-----------------------------------------------------

#display the price of the most expensive item
print(products_DF[['price']].max())

#------------------------------------------------------

#create a Dataframe that groups items by category, title and max price
grouped_by_cat = products_DF.groupby(['category','title'],as_index=False)[['price']].max()


#From that DataFrame, extract a new one with only the most expensive items
most_expensive_items_by_cat=grouped_by_cat.sort_values(by='price', ascending=False).groupby('category',as_index=False).head(1)


#create a Dataframe that contains the categories and the sum of items in stock per category
stock_per_category = products_DF.groupby('category')[['stock']].aggregate('sum')


#merge the most_expensive_items_by_cat with stock_per_category to get the final DataFrame 
stats_txt_DF=pd.merge(most_expensive_items_by_cat,stock_per_category,how='inner',on='category')

#create a new .txt file with the stats_txt_DF
with open('stats.txt', 'w') as f:
    stats = stats_txt_DF.to_string(header=False, index=False)
    f.write("CATEGORY           MOST EXPENSIVE PRODUCT           PRICE   CAT STOCK\n")
    f.write("----------------   -------------------------------  -----   ---------\n")
    f.write(stats)


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


#create a list of product categories.
categories = data_list[1]
#-----------------------------------------------------

#display the price of the most expensive item
print(products_DF[['price']].max())

#------------------------------------------------------

#create a Dataframe that groups items by category, title and max price
grouped_by_cat = products_DF.groupby(['category','title'])[['price']].max()


#Initialize helper variables
most_expensive_items_by_cat=pd.DataFrame()
cat=[]
name = []

#loop through categories and find the most expensive item of every category
for category in categories:
    if category in grouped_by_cat.index:
        cat.append(category)
        name.append(grouped_by_cat.loc[category].idxmax().values.tolist()[0])

#append categories and item titles to the new DataFrame.   
most_expensive_items_by_cat['category']=cat
most_expensive_items_by_cat['title']=name

#create a DataFrame that groups by category and max price
highest_price_by_category = products_DF.groupby('category')[['price']].max()

#create a Dataframe that contains the categories and the sum of items in stock per category
stock_per_category = products_DF.groupby('category')[['stock']].aggregate('sum')

#merge the first two dataframes by category
stats_DF=pd.merge(most_expensive_items_by_cat, highest_price_by_category, how='inner',on='category')

#merge the stats_DF with stock_per_category to get the final DataFrame 
stats_txt_DF=pd.merge(stats_DF,stock_per_category,how='inner',on='category')

#create a new .txt file with the stats_txt_DF
with open('stats.txt', 'w') as f:
    stats = stats_txt_DF.to_string(header=False, index=False)
    f.write("CATEGORY           MOST EXPENSIVE PRODUCT           PRICE   CAT STOCK\n")
    f.write("----------------   -------------------------------  -----   ---------\n")
    f.write(stats)


#!/usr/bin/env python
# coding: utf-8

# In[54]:


pip install plotly==4.14.3


# In[2]:


#dependencies
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px


# In[3]:


#read
imdb = pd.read_csv('imdbmovies.csv')
imdb.head(2)


# In[4]:



#list(imdb.columns)


# In[5]:


#cleaning NA from imdb df based on budget,wwgross and production_company columns, to display only studios with budget and gross
budget_na = imdb[imdb['budget'].str.len() > 0]
wwgross_na  = budget_na[budget_na['worlwide_gross_income'].str.len() > 0]
usa_gross_na= wwgross_na[wwgross_na['usa_gross_income'].str.len() > 0]
studio_df=pd.DataFrame(usa_gross_na)
studio_df.head()


# In[6]:


#currency converter

currency_converter = {
  "ATS": 0.79,
  "THB": 0.033,
  "PLN": 0.27,
  'NOK':  0.12,
 'NGN': 0.0026,
 'BEF':  0.030,
 'IEP':  1.54,
 'NOK':  0.12,
 'NGN': 0.0026,
 'BEF':  0.030,
 'IEP':  1.54,
 'CZK': 0.047,
 'CAD': 0.79,
 'HUF':  0.0034,
 'FRF': 0.185, 
 'CLP': 0.0014,
 'CNY':  0.15,
 'JPY':0.0095,
 'AUD':0.79,
 'GBP' : 1.41, 
'BRL': 0.18,
 'ZAR': 0.069,

 'ARS': 0.011,
 'RUR': 0.013,
 'SGD': 0.76,
 'ESP': 1.22,
 'DOP': 0.017,
 'KRW': 0.00090, 
'DEM': 0.621,
 'FIM': 0.2041,
 'CHF': 1.10,
 'SEK': 0.12,
'INR':0.014,
 'ILS': 0.31,
 'ITL': 0.000627,
 'MXN': 0.049,
 'ISK': 0.0078,
 'VEB': 0.100125,
 'HKD': 0.13,
 'DKK': 0.16,
 'EUR': 1.22,
 'NZD': 0.73,
   '$':1 
}

currency_converter


# In[7]:


#retrieving all currencies

#converting dollar and non dollar currencies into dollar value


def currency_converter_func(currency_conv_list, currency_converter):
    
    """This function takes a a dictionary of currencies and their dollar conversion rate (currency_conv_list)
       and certain amounts of money with their respective currency attached and converts to its  dollar value
    """
    converted_usd_rate = []
    for i in currency_conv_list:
        for j, y in currency_converter.items():
            init = i.split()
            curr_key = init[0]
            curr_value = init[1]
            if curr_key == j:
                convert_rate = int(init[1]) * y
                converted_usd_rate.append(convert_rate)
            
    return converted_usd_rate


#converted_usd_rate   
    
#len(converted_usd_rate)


# In[8]:


#converting dollar and non dollar currencies into dollar value

currency_conv_list = studio_df["budget"].tolist()

converted_currencies = currency_converter_func(currency_conv_list, currency_converter)
converted_currencies


# In[9]:


#retrieving their ids

#ids = studio_df["imdb_title_id"]
#new_ids = ids.tolist()
#new_ids


# In[10]:


#converting the currencies into dollars and adding to dataframe

converted_usd_rate_df = pd.DataFrame(converted_currencies)
converted_usd_rate_df.rename(columns={0:"Budget_Dollar_Equiv"}, inplace=True)
converted_usd_rate_df


# In[11]:


#merged_studio_dollar_df["Budget_Dollar_Equiv"] = converted_usd_rate_df
#merged_studio_dollar_df.head()

#merged_studio_dollar_df = pd.merge(studio_df, converted_usd_rate_df, how="left", on="imdb_title_id")
#merged_studio_dollar_df.rename(columns={0 :"Dollar_Equiv"}, inplace=True)


# In[12]:


#creating a copy of the studio_df data
merged_studio_dollar_df = studio_df

#merging the converted dollar equivalent values to the dataframe

merged_studio_dollar_df["Budget_Dollar_Equiv"] = converted_currencies
merged_studio_dollar_df.head()


# In[13]:


#getting rid of dollar sign and converting value into float and putting them back to dataframe

def dollar_splitter(splitter):
    splitted_value = []
    for i in splitter:
        init = i.split()
        curr_value = float(init[1])
        splitted_value.append(curr_value)
    return splitted_value

    
merged_studio_dollar_df["new_usa_gross_income"] = dollar_splitter(merged_studio_dollar_df["usa_gross_income"])
merged_studio_dollar_df["new_worlwide_gross_income"] = dollar_splitter(merged_studio_dollar_df["worlwide_gross_income"])

merged_studio_dollar_df.head()


# In[14]:


#profit margins

#finding absolute profit
#merged_studio_dollar_df["profit_gross_budget"] = abs(merged_studio_dollar_df["new_worlwide_gross_income"] - merged_studio_dollar_df["Dollar_Equiv"])

merged_studio_dollar_df["profit_gross_budget"] = merged_studio_dollar_df["new_worlwide_gross_income"] - merged_studio_dollar_df["Budget_Dollar_Equiv"]
merged_studio_dollar_df.head()


# In[15]:


#visualizing the top 10 movies in terms of profit

#top_profit=top_10[['original_title',"profit_gross_budget"]]
#top_profit.plot.bar(x='original_title',y='profit_gross_budget',figsize=(15,8))




# In[16]:


#percentage profit
merged_studio_dollar_df["percent_profit_gross_budget"] = ((merged_studio_dollar_df["new_worlwide_gross_income"] - merged_studio_dollar_df["Budget_Dollar_Equiv"])/merged_studio_dollar_df["Budget_Dollar_Equiv"])*100
merged_studio_dollar_df.head()


# In[17]:


#making a copy of the dataset
highest_grossing_co=merged_studio_dollar_df
highest_grossing_co


# In[18]:


#summing up the profits by company
grouped_profit=highest_grossing_co.groupby(['production_company'])['profit_gross_budget'].sum()
grouped_budget=highest_grossing_co.groupby(['production_company'])['Budget_Dollar_Equiv'].sum()


# In[19]:


grouped_profit_df=pd.DataFrame(grouped_profit)
grouped_profit_df.describe()


# In[20]:


## dataframe for studios and their profit and production budget
grouped_budget_df=pd.DataFrame(grouped_budget)
grouped_budget_df.describe()
grouped_budget_df["profit_gross_profit"] = grouped_profit_df["profit_gross_budget"]
grouped_budget_df


# In[21]:


#grouping top 20 studios worth aquiring 
top_20_studio = grouped_budget_df.nlargest (20, ['profit_gross_profit', 'Budget_Dollar_Equiv'])
top_20_studio.head()


# In[70]:


#plotting top studio profits
#top_20_studio.plot.bar(figsize=(10,6),)
fontsize=22
top_20_studio.plot.bar(
y=["Budget_Dollar_Equiv", "profit_gross_profit"],
ylabel = "Dollars in Billions",
xlabel= "Production Companies",
rot=90,
figsize=(10,5),
fontsize= 12)


legend= 22
plt.show()


# In[67]:


# ploting the worst 20 performing studios
least_perf_20_studio = grouped_budget_df.nsmallest (20, ['profit_gross_profit', 'Budget_Dollar_Equiv'])
least_perf_20_studio.head()


# In[72]:


#studios with the least profit
least_perf_20_studio.plot.bar(y=["Budget_Dollar_Equiv", "profit_gross_profit"], rot=90, figsize=(10,5), fontsize = 12,
                             ylabel = "Dollars in Billions", xlabel= "Production Companies")


# In[73]:


#adding percentage profits by company
grouped_percent=highest_grossing_co.groupby(['production_company'])['percent_profit_gross_budget'].sum()
grouped_percent.head()


# In[74]:


#prof_budget = merged_studio_dollar_df[["production_company", "year", "Budget_Dollar_Equiv", "profit_gross_budget"]].head(20)

#prof_budget.plot.bar(x="production_company", y=["year", "Budget_Dollar_Equiv", "profit_gross_budget"], rot=30, stacked=True, figsize=(20,12))


# In[75]:


#making a copy of the merged data

movie_prefernce = merged_studio_dollar_df
movie_prefernce.head()


# In[ ]:





# In[76]:


#cleaning NA from movie_prefernce[avg_vote, review from critics and users]

movie_prefernce["reviews_from_critics"] = movie_prefernce["reviews_from_critics"].dropna()
movie_prefernce["avg_vote"] =  movie_prefernce["avg_vote"].dropna()
movie_prefernce["reviews_from_users"] = movie_prefernce["reviews_from_users"].dropna()
movie_prefernce.head(3)


# In[77]:


from simple_colors import*


# In[ ]:


# randomly selecting a movie from a list  for a user to watch based on the user input of genre and year 


user_preference=True
while user_preference:
    g = input("YOUR PREFERED GENRE:  ") #input from user for prefered genre
    y = int(input("YOUR PREFERED YEAR:   "))# input year for movie
    print()
    if movie_prefernce[movie_prefernce['genre'].str.contains(g,case=False, regex=False)].size > 0: #input value must be within the genre column else it =0
        if movie_prefernce[movie_prefernce['year'].astype(int)==y].size > 0: # entered year must be withing the year column
            movie_year = movie_prefernce[movie_prefernce['year'].astype(int)==y]
            print(black("SUGGESTED MOVIE:",['bold', 'underlined']))
            print(red(movie_year[movie_year['genre'].str.contains(g,case=False, regex=False)].sample()['original_title'],'bold'))
        
 #Just in case the user changes his mind about the genre, he will have options 
            print()
            user_option = input('DO YOU LIKE THE SUGGESTED MOVIE? y/n:  ')
            if user_option == 'n':
                continue
            else:
                break
        else:
            print(blue('No Movie for that year, PLEASE MAKE NEW INPUT','bold'))
    else:
        print(blue('No Movie for that genre, PLEASE MAKE NEW INPUT','bold'))
       
    
print()
print("*******************")        
print(blue("Enjoy the Movie"))
print("*******************")
    


# In[ ]:





# In[ ]:





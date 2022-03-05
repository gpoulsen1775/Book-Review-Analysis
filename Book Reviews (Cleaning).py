#!/usr/bin/env python
# coding: utf-8

# In[114]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as ns
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


# In[122]:


#Get Data Frame
dfData = pd.read_csv("/Users/grantpoulsen/Desktop/Sentiment Data/bookDataScraped")
dfWords = pd.read_csv('/Users/grantpoulsen/Desktop/Sentiment Data/wordDataScraped')
dfWords.drop("Unnamed: 0", 1, inplace = True)
dfData.drop("Unnamed: 0", 1, inplace = True)


# In[123]:


#Fix Word Count & Drop Na Data

#Drop na Words that appeared
dfWords = dfWords.dropna()
dfWords.isna().sum()

#Drop na Data since we were missing data that was unique to each entry
dfData = dfData.dropna()
dfData.isna().sum()
dfData.reset_index(inplace = True, drop = True)


# In[124]:


#Remove Stop Words & Show it Worked

#Show a stopword
print(dfWords[dfWords['Word'] == 'you'])

#Lets Get Rid of Stopwords#####################
sws = set(stopwords.words('english'))

for w in dfWords['Word']:
    
    if(w.lower() in sws):
        dfWords = dfWords[dfWords["Word"] != w]
        
###############################################

#Show that the stop word you was removed
dfWords[dfWords['Word'] == 'you']

#Reset the index
dfWords.reset_index(inplace = True, drop = True)


# In[125]:


#Add a metric for calculating variance 
for index,row in dfWords.iterrows():
    
    dfWords.loc[index,'Variance'] = np.var([dfWords.loc[index,'0.5Star'], dfWords.loc[index,'1.0Star'], dfWords.loc[index,'1.5Star'], dfWords.loc[index,'2.0Star'],dfWords.loc[index,'2.5Star'], dfWords.loc[index,'3.0Star'], dfWords.loc[index,'3.5Star'], dfWords.loc[index,'4.0Star'], dfWords.loc[index,'4.5Star'], dfWords.loc[index,'5.0Star']])

dfWords.head(20)


# In[126]:


#Add a metric for expected value
for index,row in dfWords.iterrows():
    
    dfWords.loc[index,'Mean'] = (.5 *dfWords.loc[index,'0.5Star'] + 1.0 *dfWords.loc[index,'1.0Star'] + 1.5 *dfWords.loc[index,'1.5Star'] + 2.0 *dfWords.loc[index,'2.0Star'] + 2.5 *dfWords.loc[index,'2.5Star'] + 3.0 *dfWords.loc[index,'3.0Star'] + 3.5 *dfWords.loc[index,'3.5Star'] + 4.0 *dfWords.loc[index,'4.0Star'] + 4.5 *dfWords.loc[index,'4.5Star'] + 5.0 *dfWords.loc[index,'5.0Star']) / dfWords.loc[index,'Count']
    
dfWords.head(20)


# In[127]:


#We have a heavy bais towards using a word just once. 
dfWords['Count'].describe()


# In[128]:


#Make Stars Numeric
dfData['Stars'] = dfData['Stars'].str.replace('/5','')

for index,row in dfData.iterrows():
    
    if(dfData.loc[index,'Stars'] == ''):
        
        dfData.loc[index,'Stars'] = 0
        

dfData['Stars'] = dfData['Stars'].astype(float)


# In[130]:


#Save Collected Data
dfWords.to_csv(path_or_buf = "/Users/grantpoulsen/Desktop/wordsCleaned")
dfData.to_csv(path_or_buf = "/Users/grantpoulsen/Desktop/bookDataCleaned")


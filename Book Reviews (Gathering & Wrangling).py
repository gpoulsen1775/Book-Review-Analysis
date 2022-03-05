#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Imports
import re
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from helium import *
from selenium import webdriver 


# <H1> Webscrape Data on Books & Their Corresponding Rating </H1>

# In[4]:


#Webscrape 468 Reviews

#Header To Stop Website From Sending 403 Request
header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

#Define DF
book_review_data = pd.DataFrame(columns=["Title","Author", "Stars", "Format", "Pages", "Publisher", "Publish Date", "ISBN","Issue","Category"])

#Set First Page
currentPage = "https://manhattanbookreview.com/all-reviews/"

#For 26 Pages of Reviews: 522 Book Review
for i in range(26):
    
    #Print Whether the request worked & Current Page
    print(requests.get(currentPage,headers = header))
    print(currentPage)
    
    #Request & Format HTML 
    page = requests.get(currentPage,headers = header).text
    soup = BeautifulSoup(page,'html.parser')
    
    #Get all tags that contain Links to the Reviews
    reviewTags = soup.find_all(href = re.compile("^https://manhattanbookreview.com/product/"))
    
    #Display Link to next page
    nextPage = soup.find(rel = "next").get('href')
    
    #For Each tag 
    for reviewTag in reviewTags:

        #Extract Page for that review
        link = reviewTag["href"]
        
        #Open Driver
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')

        #Get Page, html, and quit
        driver.get(link)
        html = driver.page_source
        driver.quit()
        
        #Format HTML
        soup2 = BeautifulSoup(html, "html")
        
        #Get all info on book
        reviewData = soup2.find_all('td')
        
        #Extract Data
        title = soup2.find("title").text.replace(" - Manhattan Book Review","")
        author = reviewData[0].text
        stars = reviewData[1].text
        fmt = reviewData[2].text
        pageCount = reviewData[3].text
        publisher = reviewData[4].text
        publishDate = reviewData[5].text
        ISBN = reviewData[6].text
        issue = reviewData[8].text
        category = reviewData[9].text
        
        #Tack on Info
        book_review_data = book_review_data.append({"Title":title,"Author":author,"Stars":stars,"Format":fmt,"Pages":pageCount,"Publisher":publisher,"Publish Date":publishDate,"ISBN":ISBN,"Issue":issue,"Category":category}, ignore_index = True)

    #Move to the next page
    currentPage = nextPage
        
    


# <H1> Webscrape Data on Words & Their Corresponding Rating </H1>

# In[16]:


#Webscrape 468 Reviews

#Make dataframe to collect info on words
word_data = pd.DataFrame(columns=["Word","0.5Star","1.0Star","1.5Star","2.0Star","2.5Star","3.0Star","3.5Star","4.0Star","4.5Star","5.0Star", "Count"])

#Header To Stop Website From Sending 403 Request
header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}

#Set First Page
currentPage = "https://manhattanbookreview.com/all-reviews/"

#For 26 Pages of Reviews: 468 Book Review
for i in range(26):
    
    #Print Whether the request worked & Current Page
    print(requests.get(currentPage,headers = header))
    print(currentPage)
    
    #Request & Format HTML 
    page = requests.get(currentPage,headers = header).text
    soup = BeautifulSoup(page,'html.parser')
    
    #Get all tags that contain Links to the Reviews
    reviewTags = soup.find_all(href = re.compile("^https://manhattanbookreview.com/product/"))
    
    #Display Link to next page
    nextPage = soup.find(rel = "next").get('href')
    
    #For Each tag 
    for reviewTag in reviewTags:

        #Extract Page for that review
        link = reviewTag["href"]
        
        #Open Driver
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')

        #Get Page, html, and quit
        driver.get(link)
        html = driver.page_source
        driver.quit()
        
        #Format HTML
        soup2 = BeautifulSoup(html, "html")
        
        #Find the linebreak containing the review
        br = soup2.find_all('br')[1]
        
        #Find the star review & chop off out of 5 piece
        sr = soup2.find_all('td')[1].text.replace('/5','')

        #If the review was left w/o a score put it @ the lowest rating
        if(sr == ''):
    
            sr = .5
        
        #If the review formatted score improperly fix it
        elif(" 1/2" in sr):
            
            sr = sr[0] + ".5"
            sr = float(sr)

        #Record its rating
        else:
    
            sr = float(soup2.find_all('td')[1].text.replace('/5',''))

        #Find the paragraphs
        ps = br.find_next_siblings(attrs = {'class':''})

        #Stripdown to text
        for i in range(len(ps)):
            ps[i] = ps[i].text

        #Turn into one string
        ps = " ".join(ps)

        #Seperate Words
        ps = ps.split(" ")

        #List of Words
        words = ps

        #Iterate Through & Add to Data
        for word in words:
        
            #Strip Word down to all alphanumeric 
            word = ''.join(t for t in word if t.isalnum());
            
            #If our word contained no alphanumeric skip it
            if(word == ''):
                continue
            
            #If we already have the word
            if(word_data['Word'].str.contains(word).any()):
        
                #Incrament
                word_data.loc[word_data["Word"] == word, str(sr) + "Star"] = word_data.loc[word_data["Word"] == word, str(sr) + "Star"] + 1
                word_data.loc[word_data["Word"] == word,"Count"] = word_data.loc[word_data["Word"] == word,"Count"] + 1
            
            #If we don't have the word
            else:
        
                #Insert & Incrament
                word_data = word_data.append({"Word":word,"0.5Star":0,"1.0Star":0,"1.5Star":0,"2.0Star":0,"2.5Star":0,"3.0Star":0,"3.5Star":0,"4.0Star":0,"4.5Star":0,"5.0Star":0, "Count":1}, ignore_index = True)
                word_data.loc[word_data["Word"] == word, str(sr) + "Star"] = word_data.loc[word_data["Word"] == word,  str(sr) + "Star"] + 1
        
    #Move to the next page
    currentPage = nextPage
   

#Set index to be word
word_data.set_index(["Word"])
word_data.head()   


# <H1> Save Collected Data </H1>

# In[21]:


#Save Collected Data
word_data.to_csv(path_or_buf = "/Users/grantpoulsen/Desktop/word_review")
book_review_data.to_csv(path_or_buf = "/Users/grantpoulsen/Desktop/book_review_data")


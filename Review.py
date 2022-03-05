#!/usr/bin/env python
# coding: utf-8

# In[146]:



class Review: 

    #Initialize Class with dataframe
    def __init__(self,df):
        
        self.df = df
      
    #Get score of review
    def score(self,string):
        
        #Split by period first in case user did not use spaces following periods
        sentences = string.split(".")
        
        counter = 0
        
        #Split each sentence into words with characters included
        for sentence in sentences:
            
            sentences[counter] = sentences[counter].split(" ")
            counter = counter + 1
        
        counter = 0
        
        #Combine the lists for each sentence
        for sentence in sentences:
            
            #Skip the first one
            if(counter == 0):
                
                counter = counter + 1
                continue
            
            #Append
            sentences[0] = sentences[0] + sentences[counter]
            counter = counter + 1
        
        #Now we have one list with all the words
        sentences = sentences[0]
        
        #Lets rename for readability
        words = sentences
        
        counter = 0
        
        #Strip the alphanumeric
        for word in words:
            
            words[counter] = ''.join(token for token in word if token.isalnum());
            
        #Get Recorded Words as list
        dfWord = df["Word"].to_list()
        
        #Get words that exist in dataframe
        knownWords = [word for word in words if word in dfWord]
    
        print(knownWords)
        
        score = 0
        
        #Sum Score
        for word in knownWords:
            
            print(self.df.loc[df['Word'] == word,'Mean'].values[0])
            score = score + self.df.loc[df['Word'] == word,'Mean'].values[0]
            
        #Normalize by length
        score = score / len(knownWords)
        
        return score


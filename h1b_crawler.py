#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 17:19:05 2021

@author: peterlin0629
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bs4 as bs
import urllib
import datetime

url_list = [] 

year = datetime.datetime.now().year
url_base = "https://h1bdata.info/index.php?em=&job=" 
title = "Business+Analyst"  
url_end = "&city=&year="

n_year = int(input("how many years you want to track back?"))

for i in range(n_year):
    url_list.append(url_base + title + url_end + str(year-i))


raw_data = []

def insert_data(): 
    for i in range(len(url_list)):
        r = urllib.request.urlopen(url_list[i]) 
        soup = bs.BeautifulSoup(r, 'html.parser')
        main_table = soup.find_all("table", {"id":"myTable"})   #the table contains the main content
        main_body = main_table[0].find_all("tbody")
        
        
        head_element = []
        head = []

        for i in main_table:
            head_element = i.find_all("th")
        for i in head_element:
            head.append(i.get_text().strip())
            
            
        body_element = []
        body = []
        
        for i in main_body:
            body_element = i.find_all("tr")
        for i in body_element:
            body_row = []
            for j in i.find_all("td"):
                body_row.append(j.get_text().strip())
            body.append(body_row)


        for i in range(len(body)):
            h1b_dict = {}
            for j, k in zip(head, body[i]):
                h1b_dict[j] = k
            raw_data.append(h1b_dict)
                    
insert_data()

df = pd.DataFrame(raw_data)
df.to_csv("h1b_" + str(year - n_year +1) +"to" +str(year) +".csv")


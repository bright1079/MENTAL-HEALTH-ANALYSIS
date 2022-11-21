#!/usr/bin/env python
# coding: utf-8

# <h1 style= "color:black; font-size:392%"> NUMBER OF <b style="color:red">CANCER</b> SURGERIES PERFORMED IN CALIFORNIA HOSPITALS    FROM 2013 TO 2020 </h1>
# 
# 
# <h2 style="color:black; font-size:300%">BACKGROUND</h2> 
# 
# 
# <b style="font-size:200%"> The dataset used for this ANALYSIS was obtained from <a href="
# https://data.chhs.ca.gov/dataset/number-of-cancer-surgeries-volume-performed-in-california-hospitals">data.chhs.ca.gov</a> </b>
# 
# 
# 
# 
# 
# 
# 
# 
# Citation:  	HCAI Patient Discharge Data and Ambulatory Surgery Data (for breast cancer only), 2013 - 2019
# 
# 
# 

# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:#5642C5;
#            font-size:210%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 40px;
#               color:white;">
# IMPORT RELEVANT LIBRARIES
# </p>
# </div>

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:#5642C5;
#            font-size:210%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 20px;
#               color:white;">
# READ DATASET
# </p>

# In[125]:


data=pd.read_csv("cancer.csv", encoding="unicode_escape")
data


#  <h1 style="color:blue"; font-size:100%">INSPECT DATA:</h1> 
#     
#  <h2 style="color:blue; font-size:150%">Dataset Dimension, Size, Numerical Summary and Dataset Column Type:</h2>

# In[32]:


print("This is the shape of the data: ", data.shape)
print("This is the total numerical summary of the data", data.describe())


# In[33]:


# Dataset column type
data.info()


#  <h1 style="color:red"; font-size:100%">DATA CLEANING AND MANIPULATION:</h1>

# In[35]:


# check for names of columns
data.columns


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 20px;
#               color:white;">
# INSIGHT:Some of the columns have have to be renamed to avoid ambiquity during analysis
# </p>

# In[131]:


data=data.rename(columns={"OSHPDID":"OSHPD_ID", "# of Cases (ICD 9)":"No_of_cases1", "# of Cases (ICD 10)":"No_of_cases2"})
data


# In[37]:


#check for null data
data.isnull().sum()


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:#5642C5;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 20px;
#               color:white;">
# IMPORT "missingno" LIBRARY TO SHOW THE DISTRIBUTION OF MISSING VALUES IN THE DATAFRAME
# </p>

# In[126]:


import missingno as mn
mn.matrix(data)


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight1: We have equal numbers(88) that are missing in the ["County"] and ["OSHPD_ID"] columns respectively. Similarly, the ["LONGITUDE"] AND ["LATITUDE"] columns have the same values(95) that are missing. While for the no of cases columns, we have unequal missing digits.
#     
#    
# </p>
# </div>
# 

# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;"> Insight2: When we look closely to the above missing matrix map, we can see that the thin lines drawn on the missing values for the above mentioned columns["County" and "OSHPD_ID"] are on the the same plane, hence each pair of column mentioned above are linearly correlated.
# 
#    
# </p>
# </div>

# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight3: For the number of cases 1 and 2 columnns, we can see that both columns are inversely related, so therefore we               can conclude that when a particular value is given in case 1, then case 2 value will be missing and vuce versa.
# 
#     
#    
# </p>
# </div>

# WE CAN SEE THAT THE COLUMNS COUNTRY AND OSPHDID HAVE THE SAME MISSING VALUES(88). SIMILARLY, THE COLUMNS FOR LONGITUDE
# LATITUDE HAVE SIMILAR TREND(95). LET US SEE IF THERE IS A CORRELATION. Before then, let us fill null data.

# In[127]:


#fill missing values
data=data.fillna("Empty")
data


# In[128]:


# We do not need some columns
data=data.drop(["LONGITUDE", "LATITUDE"], axis=1)
data


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: 
# from the above output, it seems like the ["Hospital"] titled "Statewide" corresponds to empty cells in the ["County"]'s column. Let us confirm to be sure.
# </p>
# </div>
# 
# 
# 

# In[132]:


# Check if statewide hospital==empty in the county column
check1=data[((data["Hospital"]=="Statewide")&(data["County"]=="Empty"))]
print("The shape of empty cells in county column",check1.shape)
check2=data[((data["County"]=="Empty") & (data["OSHPD_ID"]=="Empty"))]
print("The shape of Hospital named Statewide: ",check2.shape)


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:blue;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: The assumption is confirmed, so we actually do not know which country and ID #(OSHPD_ID) Statewide hospital
# belongs to, we can call the unknown 
# country "state" and generate a unique id(OSHPDID) from the mean of other countries ID
# 
# 
# 
# </p>
# </div>
# 
# 
# 
# .

# In[134]:


data["County"]=data["County"].replace(to_replace=["Empty"],value= "State")
data["OSHPD_ID"]=data["OSHPD_ID"].replace(to_replace=["Empty"],value= 0)
data


# In[135]:


#taking the mean of OSHPDID as the new ID for the Statewide Hospital
IDmean=data["OSHPD_ID"].mean()
IDmean=round(IDmean)
IDmean


# In[136]:


# replacing 
data["OSHPDID"]=data["OSHPD_ID"].replace(to_replace=[0],value= IDmean)
data


# In[137]:


print(data["OSHPD_ID"].nunique())
print(data["Hospital"].nunique())


# </h1 style: "color: blue"; "font-size:200%"However, after checking for unique ID and hospitals, and the data did not tally, we will further drop the OSHPDID <h1>
# column

# In[138]:


data=data.drop(["OSHPDID"], axis="columns")
data


# # explore the no_of_cases, and check for correlation

# In[139]:


data["No_of_cases1"]=data["No_of_cases1"].replace(to_replace=["Empty"],value= 0)
data["No_of_cases2"]=data["No_of_cases2"].replace(to_replace=["Empty"],value= 0)
data


# In[140]:


print("This is the shape of case1 column : ", data["No_of_cases1"].shape)
print("This is the shape of case2 column : ", data["No_of_cases2"].shape)


# In[141]:


# we can create a series that from the size above. After creating that, we use it to plot our scatter plots
series=pd.Series(range(15699))
series


#  <h1 style="color:blue"; font-size:100%">INSPECT DATA:</h1> 
#     
#  <h2 style="color:blue; font-size:150%">We create and join two scattered plots for the numbers of case 1 and 2 using the series(having a range 15699) we created above :</h2>

# In[149]:


fig=plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.scatter(data["No_of_cases1"], series, label="No_of_cases1")
ax1.scatter(data["No_of_cases2"], series, label="No_of_cases2")
plt.title("Scatter plot combining case 1 & 2", fontsize=18, color="red")
plt.legend()
plt.xlabel("Series(0 - 15699)", color="red", fontsize=15)
plt.ylabel("No of Cases(1 & 2)", color="red", fontsize=15)


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: Most of the values are densely concentrated at 0(because, when a value is filled in case1, case2 is omitted and vice versa). Secondly, most values filled  were in column case2. And lastly, the values are roughly concentrated between 0 to 75000. 
# </p>
# </div>
# 

# In[111]:


#Check for correllation
check=data[((data["No_of_cases1"]=="Empty") & (data["No_of_cases2"]=="Empty"))]
print("The shape of the data is: ", check.shape)
col1, col2=data["No_of_cases1"], data["No_of_cases2"]
col=col1.corr(col2)
print("The correlation is: " , col, "\n and we can see we have no correlation ")


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: 
# we can see that there is no instance where we had both columns for cases empty. Therefore, we will form a new column that will join columns for case1 and case2 and deleting the cells 0 values. We use the mask() function to achieve this
# </p>
# </div>
# 

# In[150]:


# Using mask()
data["No_of_cases1"].mask(data["No_of_cases1"]==0, data["No_of_cases2"], inplace=True)
data


# In[151]:


# ["No_of_cases1"] is filled up, so we drop the ["No_of_cases"]
data=data.drop(["No_of_cases2"], axis=1)
data


# In[152]:


# recheck for null values
data.isnull().sum()


# <h1 style="color:blue"; font-size:100%">CREATE HEATMAP</h1> 
# 

# In[153]:


heatmap1=data.groupby("Surgery").Year.value_counts().unstack()
heatmap1


# In[154]:


heatmap1.isnull().sum()


# In[155]:


#Using seaborn to make heatmap
sns.set(rc = {'figure.figsize':(15,8)})
sns.heatmap(heatmap1,cmap="RdBu", annot=True, fmt=".0f")


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: we can see that Colon and Breast surgeries were more common from 2013 to 2020, while Esophagus is the least.
# 
# </div>
# 

# <h1 style="color:blue"; font-size:100%">GROUP EACH COLUMN BY NO OF CASES AND VISUALIZATION</h1> 

# In[156]:


year_group=data.groupby(["Year"]).No_of_cases1.sum()
year_group=pd.DataFrame(year_group.reset_index())
year_group=year_group.sort_values(by=["No_of_cases1"], ascending=[False])
year_group=year_group.reset_index()
year_group.columns=["index", "Year","No_of_cases1"]
year_group=year_group.drop(["index"], axis=1)



county_group=data.groupby(["County"]).No_of_cases1.sum()
county_group=pd.DataFrame(county_group.reset_index())
county_group=county_group.sort_values(by=["No_of_cases1"], ascending=[False])
county_group=county_group.reset_index()
county_group.columns=["index", "Country","No_of_cases1"]
county_group=county_group.drop(["index"], axis=1)


hospital_group=data.groupby(["Hospital"]).No_of_cases1.sum()
hospital_group=pd.DataFrame(hospital_group.reset_index())
hospital_group=hospital_group.sort_values(by=["No_of_cases1"], ascending=[False])
hospital_group=hospital_group.reset_index()
hospital_group.columns=["index", "Hospital","No_of_cases1"]
hospital_group=hospital_group.drop(["index"], axis=1)



surgery_group=data.groupby(["Surgery"]).No_of_cases1.sum()
surgery_group=pd.DataFrame(surgery_group.reset_index())
surgery_group=surgery_group.sort_values(by=["No_of_cases1"], ascending=[False])
surgery_group=surgery_group.reset_index()
surgery_group.columns=["index", "Surgery","No_of_cases1"]
surgery_group=surgery_group.drop(["index"], axis=1)


# In[121]:


fig=plt.figure(figsize=(20,20))
Cases=year_group["No_of_cases1"]
Year=year_group["Year"]
ax1=sns.barplot(x=Year, y=Cases, data=year_group, order=Year)
ax1.bar_label(ax1.containers[0]);



# In[157]:


fig=plt.figure(figsize=(20,20))
Cases=county_group["No_of_cases1"]
County=county_group["Country"]
ax=sns.barplot(x=County, y=Cases, data=year_group)
ax.bar_label(ax.containers[0])
plt.xticks(rotation=90);



# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:red;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: We can see that the county(province) that was empty at the beginning of this notebook which we replaced as "state" has the highest value of surgeries, followed by Los Angeles. On the other hand, Colusa has the mininum with a value of just 1.
# 
# </div>
# 
# 
# </div>
# 

# In[161]:


fig=plt.figure(figsize=(20,20))
Cases=surgery_group["No_of_cases1"]
Surgery=surgery_group["Surgery"]
ax=sns.barplot(x=Surgery, y=Cases, data=year_group)




# In[165]:



fig=plt.figure(figsize=(20,20))
Cases=hospital_group["No_of_cases1"]
Hospital=hospital_group["Hospital"]
ax=sns.barplot(y=Hospital, x=Cases, data=year_group)
plt.xticks(rotation=90, fontsize=10)

plt.show()


# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:blue;
#            font-size:110%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 10px;
#               color:white;">    Insight: The data is too noisy, I will need to reduce the parameters in order to visualize properly
# 
# </p>
# </div>
# 

# <div style="color:white;
#            display:fill;
#            border-radius:5px;
#            background-color:#5642C5;
#            font-size:210%;
#            font-family:Verdana;
#            letter-spacing:0.5px">
# 
# <p style="padding: 40px;
#               color:white;">
# BUILDING SEVERAL ML MODELS
# </p>

# # I am stuck here, because most of my parameters are discrete categorical variables, so i need to learn frequency encoding to change my parameters to digits for my machine learning models
# 
# 
# counter or frequency encoding

# In[166]:


cols=data.columns
for i in cols:
    print("This is the unique value of", i, ":", data[i].nunique())


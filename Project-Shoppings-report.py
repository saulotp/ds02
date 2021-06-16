import pandas as pd
import matplotlib.pyplot as plt 

## ----------------------------- INITIAL SETTINGS -----------------------------##
#Setting a good quality for images that will be generates in this script
plt.rcParams["figure.dpi"] = 300




## ----------------------------- MAIN CODE -----------------------------##
#Creating a master DataFrame (dfmain) after read the excel file
dfmain = pd.read_excel("~/DataScience/Vendas.xlsx", parse_dates=['Data'])  

#converting DATA column from string to dateformat
dfmain['Data'] = pd.to_datetime(dfmain['Data'])


#DataFrame with mall ID and sum of total sales value (ID LOJA, VALOR FINAL)
dftotalvalue = dfmain[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()

#Sorting values to find wich mall had the best performance (Shopping Vila Velha)
dftotalvalue = dftotalvalue.sort_values(by='Valor Final', ascending=False)

#DataFrame with mall ID and mean of total sales value (ID LOJA, VALOR FINAL)
dfmeanvalue = dfmain[['ID Loja', 'Valor Final']].groupby('ID Loja').mean()
dfmeanvalue = dfmeanvalue.sort_values(by='Valor Final', ascending=False)


#Total value of all sales (Column sum() VALOR FINAL)
total = dftotalvalue['Valor Final'].sum()


#Add a Column on DataFrame to show a percentual value among all malls, i.e how much percent of sales each mall represents 
#for example: I know tha all malls sales represents 100%, but how much percent Shopping Vila Velha represent?
#below code show us that Shopping Vila Velha represents 4.14% from 100% (all malls together)
dftotalvalue['%']=dftotalvalue['Valor Final']*100/total





## -------------------------  MALL ANALYSIS  ------------------------- ##
#In this section we can extract data for each mall only changing the ['ID Loja'] == 'Selected Mall'

# Creating a new DataFrame with the selected mall data only
dfmall = dfmain.loc[dfmain['ID Loja'] == 'Shopping Morumbi']


#Creating another DataFrame from (dfmall), but this time I want to know how much each product was sold
dfproductsoldvalue = dfmall[['ID Loja', 'Produto', 'Valor Final']].groupby('Produto').sum()


#New DataFrame to sort the itens and find out wich product had the most sales
dfproductsoldvalue = dfproductsoldvalue.sort_values(by='Valor Final', ascending=False)

#Total value of all sales (Column sum() VALOR FINAL)
dfmalltotal = dfproductsoldvalue['Valor Final'].sum()

#Adding a new (%) Column to last DataFrame
dfproductsoldvalue['%']= dfproductsoldvalue['Valor Final']*100/dfmalltotal






## --------------------- Interval Date analisis --------------------- ##
#New DataFrame to select a specific date interval
dfmalldates = dfmall[['Data','Produto', 'Valor Final']]

#Sum of total sales by mounth
dfmalldatessumlsales = dfmalldates.resample('M', on='Data').sum()
dfmalldatessumlsales.columns = [''] * len(dfmalldatessumlsales.columns)

#Plot the dataframe data into graphic. 
pt = dfmalldatessumlsales.plot(style='.-', ms=15, color='red', figsize=(20,10), lw=5, legend=False, xlabel='', title = 'Total Sales')
pt.axes.title.set_size(20)


#Mean of total sales by mounth
dfmalldatesmean = dfmalldates.resample('M', on='Data').mean()
dfmalldatesmean = dfmalldatesmean.sort_values(by='Valor Final', ascending=False)

#removing label from VALOR TOTAL column
dfmalldatesmean.columns = [''] * len(dfmalldatesmean.columns)

#Plot the dataframe data into graphic
dfmalldatesmean.plot(figsize=(20,10))

# In this case the interval selected was January from `2019-01-01` until `2019-01-31`
dfdatesselection = (dfmalldates['Data'] >= '2019-01-01') & (dfmalldates['Data'] <= '2019-01-31')
dfselected = dfmalldates[dfdatesselection]

#filtering data by product
dftotalvalueproduct = dfselected[['Produto', 'Valor Final']].groupby('Produto').sum()

#Total value of all sales (Column sum() VALOR FINAL)
dftotalproductsum = dftotalvalueproduct['Valor Final'].sum()


#after sum, this line code can sort values from the product with more sales to product with less sales
dftotalvalueproduct = dftotalvalueproduct.sort_values(by='Valor Final', ascending=False)

#Adding a new (%) Column to last DataFrame
dftotalvalueproduct['%'] = dftotalvalueproduct['Valor Final']*100/dftotalproductsum



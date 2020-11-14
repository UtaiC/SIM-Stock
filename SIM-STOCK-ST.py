import streamlit as st
import pandas as pd
#from sklearn import datasets
#from sklearn.ensemble import RandomForestClassifier
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import math
from matplotlib.ticker import FuncFormatter
import ipywidgets as widgets

Del=pd.read_excel('Del-Data.xlsx')
Del.set_index('PartNo',inplace=True)

DC=pd.read_excel('DC-Data.xlsx')
DC.set_index('PartNo',inplace=True)

QC=pd.read_excel('QC-Data.xlsx')
QC.set_index('PartNo',inplace=True)

FN=pd.read_excel('FN-Data.xlsx')
FN.set_index('PartNo',inplace=True)

db=pd.read_excel('Database.xlsx')
db.set_index('PartNo',inplace=True)

WIP=pd.read_excel('WIP.xlsx')
WIP.set_index('PartNo',inplace=True)

MC=pd.read_excel('MC-Data.xlsx')
MC.set_index('PartNo',inplace=True)

st.header('STOCK Update and Balance')
#st.subheader('Oct-2020')

WIP=WIP[['BF','BM','FG0','FG1']]
#WIP=WIP['PartNo'].astype(str)
#WIP=WIP[WIP>0]
#st.text('WIP-BF Update')
#st.write(WIP)

Del=Del['Del-Pcs'].groupby('PartNo').sum()
#st.text('DC-BF Update')
#st.write(Del)

QC=QC['FG1-Pcs'].groupby('PartNo').sum()
#st.text('DC-BF Update')
#st.write(QC)

DC=DC['BF-Pcs'].groupby('PartNo').sum()
#st.text('DC-BF Update')
#st.write(DC)

FN=FN[['BM-Pcs','FG0-Pcs']].groupby('PartNo').sum()
#st.text('FN-BM Update')
#st.write(FN)

MC=MC['M-FG0'].groupby('PartNo').sum()
#st.text('FN-BM Update')
#st.write(MC)

MCm=pd.merge(db,MC,on='PartNo',how='left')

Delm=pd.merge(MCm,Del,on='PartNo',how='left')

FG1m=pd.merge(Delm,QC,on='PartNo',how='left')

WIPm=pd.merge(FG1m,WIP,on='PartNo',how='left')

FNm=pd.merge(WIPm,FN,on='PartNo',how='left')

STbf=pd.merge(FNm,DC,on='PartNo',how='left')


STbf=STbf.fillna(0)
STbf=STbf[['BF','BM','FG0','FG1','BF-Pcs','BM-Pcs','FG0-Pcs','M-FG0','FG1-Pcs','Del-Pcs']]
st.subheader('STOCK DATA before Balance')
st.write(STbf)
#STbf.to_excel('STOCK-DATA2.xlsx')

STbf['BF_STOCK']=(STbf['BF']+STbf['BF-Pcs'])-(STbf['BM-Pcs']+STbf['FG0-Pcs'])
BF_STOCK=STbf['BF_STOCK']
#st.subheader('BF Stock Balance')
#st.write(BF_STOCK)

STbf['BM_STOCK']=(STbf['BM']+STbf['BM-Pcs'])-(STbf['M-FG0']+STbf['FG1-Pcs'])
BM_STOCK=STbf[['BM_STOCK']]
#st.subheader('BM Stock Balance')
#st.write(BM_STOCK)

STbf['FG0_STOCK']=(STbf['FG0']+STbf['FG0-Pcs']+STbf['M-FG0'])-(STbf['FG1-Pcs'])
FG0_STOCK=STbf['FG0_STOCK']
#st.subheader('FG0 Stock Balance')
#st.write(FG0_STOCK)

STbf['FG1_STOCK']=(STbf['FG1']+STbf['FG1-Pcs'])-(STbf['Del-Pcs'])
FG1_STOCK=STbf['FG1_STOCK']
#st.subheader('FG0 Stock Balance')
#st.write(FG0_STOCK)

STbf['Delivery']=STbf['Del-Pcs']
Delivery=STbf['Delivery']
#st.subheader('FG0 Stock Balance')
#st.write(Delivery)


selected_ST_Type = st.sidebar.multiselect('Select Stock Type',['BF_STOCK','BM_STOCK','FG0_STOCK','FG1_STOCK','Delivery'],default=['BF_STOCK'],)

selected_Part = st.sidebar.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680'],default=['3000'],)
Show_Stock=STbf.loc[selected_Part][selected_ST_Type]
st.subheader('Sort Stock by Selected')
st.write(Show_Stock)



Delis=STbf['Del-Pcs']
#st.write(Delis)

QCst=STbf['FG1-Pcs']
#st.write(QCst)

WIPbf=STbf['BF']
WIPfg0=STbf['FG0']
#st.write(WIPbf)
#st.write(WIPfg0)

DCbf=STbf['BF-Pcs']
#st.write(DCbf)

FNbf=STbf['BM-Pcs']
FNfg0=STbf['FG0-Pcs']
#st.write(FNbf)
#st.write(FNfg0)

FGbl=STbf['FG1-Pcs']
#st.write(FGbl)

MCbl=STbf['M-FG0']
#st.write(MCbl)

BFstock=((WIPbf+DCbf)-FNbf)

#st.write(BFstock)

FG0stock=((WIPfg0+FNfg0+MCbl)-(FGbl))

#st.write(BFstock)

FG1stock=(FGbl-Delis)

#st.write(FG1stock)

#st.subheader('Delivery Update')
#st.write(Delis)


Showstock=STbf[['BF_STOCK','BM_STOCK','FG0_STOCK','FG1_STOCK','Delivery']]
#howstock.to_excel('STOCKUPDATE.xlsx')
st.subheader('STOCK DATA after Balnace')
st.write(Showstock)
st.bar_chart(Showstock)


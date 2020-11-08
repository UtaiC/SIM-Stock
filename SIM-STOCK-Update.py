import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import altair as alt

st.set_page_config(layout="wide")

Logo=Image.open('SIM-Logo.jpeg')
st.image(Logo,width=500)

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

WIP=WIP[['BF','BM','FG0','FG1']]
Del=Del['Del-Pcs'].groupby('PartNo').sum()
QC=QC['FG1-Pcs'].groupby('PartNo').sum()
DC=DC['BF-Pcs'].groupby('PartNo').sum()
FN=FN[['BM-Pcs','FG0-Pcs']].groupby('PartNo').sum()
MC=MC['M-FG0'].groupby('PartNo').sum()

MCm=pd.merge(db,MC,on='PartNo',how='left')
Delm=pd.merge(MCm,Del,on='PartNo',how='left')
FG1m=pd.merge(Delm,QC,on='PartNo',how='left')
FNm=pd.merge(FG1m,FN,on='PartNo',how='left')
DCm=pd.merge(FNm,DC,on='PartNo',how='left')
STbf=pd.merge(DCm,WIP,on='PartNo',how='left')
#st.write(STbf)

STbf=STbf.fillna(0)
STbf=STbf[['BF','BM','FG0','FG1','BF-Pcs','BM-Pcs','FG0-Pcs','M-FG0','FG1-Pcs','Del-Pcs']]
st.subheader('STOCK DATA before Balance')
st.write(STbf)

STbf['BF_STOCK']=(STbf['BF']+STbf['BF-Pcs'])-(STbf['BM-Pcs']+STbf['FG0-Pcs'])
BF_STOCK=STbf['BF_STOCK']

STbf['BM_STOCK']=(STbf['BM']+STbf['BM-Pcs'])-(STbf['M-FG0']+STbf['FG1-Pcs'])
BM_STOCK=STbf[['BM_STOCK']]

STbf['FG0_STOCK']=(STbf['FG0']+STbf['FG0-Pcs']+STbf['M-FG0'])-(STbf['FG1-Pcs'])
FG0_STOCK=STbf['FG0_STOCK']

STbf['FG1_STOCK']=(STbf['FG1']+STbf['FG1-Pcs'])-(STbf['Del-Pcs'])
FG1_STOCK=STbf['FG1_STOCK']

STbf['Delivery']=STbf['Del-Pcs']
Delivery=STbf['Delivery']

selected_ST_Type = st.sidebar.multiselect('Select Stock Type',['BF_STOCK','BM_STOCK','FG0_STOCK','FG1_STOCK','Delivery'],default=['BF_STOCK'],)

selected_Part = st.sidebar.multiselect('Select PartNo', ['1632','1732','2532','2633','9231','9330','1231','1530','1630','2731','2831','4333','4433','5130','5230','5330','2001','2031','2902','3102','5402',
'6803','7702','7802','9701','0201','0231','0802','2130','2200','4600','2102','3000','3100','4900','5000','9907','9910','493C','4946','8549','8551','9112','9115','9524',
'9115','9706','9708','0626','0628','5679','5400','5501','0702','0801','8551','0802','1771','T3100','3113','9775','9680'],default=['3000'],)
Show_Stock=STbf.loc[selected_Part][selected_ST_Type]
st.subheader('Sort Stock by Selected')
st.write(Show_Stock)

Delis=STbf['Del-Pcs']
QCst=STbf['FG1-Pcs']
WIPbf=STbf['BF']
WIPfg0=STbf['FG0']
DCbf=STbf['BF-Pcs']
FNbf=STbf['BM-Pcs']
FNfg0=STbf['FG0-Pcs']
FGbl=STbf['FG1-Pcs']
MCbl=STbf['M-FG0']

BFstock=((WIPbf+DCbf)-FNbf)

FG0stock=((WIPfg0+FNfg0+MCbl)-(FGbl))

FG1stock=(FGbl-Delis)

Showstock=STbf[['BF_STOCK','BM_STOCK','FG0_STOCK','FG1_STOCK','Delivery']]

st.subheader('STOCK DATA after Balnace')
st.write(Showstock)
st.bar_chart(Showstock)

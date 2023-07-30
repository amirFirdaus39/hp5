import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import dateutil.relativedelta
import itertools
import openpyxl
import streamlit as st

#streamlit run "d:/pyfile/financehp5/B5_4_2 Finance.py"
st.title("B5-4-2 Last Month Payment")

list_name = ['Ziad','Amir','Lutfi','Adnan','Kimi']
empty = [0,0,0,0,0]
col = {"NAME": list_name,
       "API":empty,
       "AIR":empty,
       "WIFI":empty,
       "OTHERS":empty,
       "REFUND":empty
       }

df = pd.DataFrame(col)

fix = pd.read_excel("data/hp5.xlsx",sheet_name='Fix')
rent = pd.read_excel("data/hp5.xlsx",sheet_name='Rent')
flow = pd.read_excel("data/hp5.xlsx",sheet_name='Flow')

lastmonth = datetime.now() - dateutil.relativedelta.relativedelta(months=1)
lastmonth = int(lastmonth.strftime("%Y%m"))
currentmonth = datetime.now() 
currentmonth = int(currentmonth.strftime("%Y%m"))

currentkey = [1,2,3,4,5,6]
lastkey = [7,8,9,10,11,12]

def calculate(lastmonth,fix,rent,flow,key): 
       df = pd.DataFrame(col)
       name = ['Ziad','Amir','Lutfi','Adnan','Kimi']
       n = len(name)
       
       api = fix.loc[fix['YM'] == lastmonth,'API'].reset_index(drop=True)
       air = fix.loc[fix['YM'] == lastmonth,'AIR'].reset_index(drop=True)
       wifi = fix.loc[fix['YM'] == lastmonth,'WIFI'].reset_index(drop=True)
       
       apip = api[0]/n
       airp = air[0]/n
       wifip = wifi[0]/n
       
       df['AIR'] = airp
       df['API'] = apip
       df['WIFI'] = wifip
       
       df = pd.merge(df,rent,how='left',on=['NAME'])
       flow = flow.loc[flow['YM'] == lastmonth].reset_index(drop=True)
       flow['REFUND'] = flow['PAID'] - (flow['PAID']/flow['NUM_SPLIT'])
       flow['PER'] = (flow['PAID']/flow['NUM_SPLIT'])
       
       for name in list_name:
           for i in range(len(flow['NAME_LIST'])):
               if name in flow['NAME_LIST'][i]:
                   df['OTHERS'] = np.where(df['NAME']==name,df['OTHERS']+flow['PER'][i],df['OTHERS'])
               if name in flow['NAME'][i]:
                   df['REFUND'] = np.where(df['NAME']==name,df['REFUND']+flow['REFUND'][i],df['REFUND'])
       
       df['REFUND'] = np.where(df['NAME']=='Adnan',df['REFUND']+(wifi[0]-wifip),df['REFUND'])
       df['REFUND'] = df['REFUND']*-1
       df['TOTAL'] = df['API'] + df['AIR'] + df['WIFI'] + df['RENT'] + df['OTHERS'] +  df['REFUND'] 
       df = df[['NAME','API','AIR','WIFI','OTHERS','RENT','REFUND','TOTAL']]
       df['API'] = df['API'].apply(lambda x : round(x,2))
       df['AIR'] = df['AIR'].apply(lambda x : round(x,2))
       df['WIFI'] = df['WIFI'].apply(lambda x : round(x,2))
       df['OTHERS'] = df['OTHERS'].apply(lambda x : round(x,2))
       df['RENT'] = df['RENT'].apply(lambda x : round(x,2))
       df['REFUND'] = df['REFUND'].apply(lambda x : round(x,2))
       df['TOTAL'] = df['TOTAL'].apply(lambda x : round(x,2))
       
       st.header(f"📝 {str(lastmonth)[:4]}-{str(lastmonth)[4:]}")
       st.write("---") 
       col1, col2 = st.columns(2)
       with col1:
           st.subheader("Overall Payments")
           st.write(f"Electricity: RM{api[0]}")
           st.write(f"Water: RM{air[0]}")
           st.write(f"Wifi: RM{wifi[0]}")
           st.write(f"Rent: RM1800")
           st.table(df.style.format({"API": "{:.2f}",
                                       "AIR": "{:.2f}",
                                       "WIFI": "{:.2f}",
                                       "OTHERS": "{:.2f}",
                                       "RENT": "{:.2f}",
                                       "REFUND": "{:.2f}",
                                       "TOTAL": "{:.2f}"
                                       }))
           type = ['API','AIR','WIFI','OTHERS','RENT','REFUND']
           # options = st.multiselect(
           #     'Choose Unpaid Payments:',
           #     type, default=type)
       with col2:
           st.subheader("Individual Payments")
           tab1, tab2, tab3, tab4, tab5 = st.tabs(list_name)
              
           #ziad
           with tab1:
               options = st.multiselect(
               'Choose Unpaid Payments:',
               type, default=type,key=key[0])
               z_df = df.loc[df['NAME'] == 'Ziad', options]
               z = z_df.sum(axis=1)
               z_df['TOTAL'] = round(z,2)
               st.table(z_df.style.format({"API": "{:.2f}",
                                           "AIR": "{:.2f}",
                                           "WIFI": "{:.2f}",
                                           "OTHERS": "{:.2f}",
                                           "RENT": "{:.2f}",
                                           "REFUND": "{:.2f}",
                                           "TOTAL": "{:.2f}"
                                           }))
               st.write("Ziad has to pay a total amount of:")
               st.subheader(f"RM{round(z.values[0],2)}")
           #amir
           with tab2:
               options = st.multiselect(
               'Choose Unpaid Payments:',
               type, default=type,key=key[1])
               am_df = df.loc[df['NAME'] == 'Amir', options]
               am = am_df.sum(axis=1)
               am_df['TOTAL'] = round(am,2)
               st.table(am_df.style.format({"API": "{:.2f}",
                                           "AIR": "{:.2f}",
                                           "WIFI": "{:.2f}",
                                           "OTHERS": "{:.2f}",
                                           "RENT": "{:.2f}",
                                           "REFUND": "{:.2f}",
                                           "TOTAL": "{:.2f}"
                                           }))
               st.write("Amir has to pay a total amount of:")
               st.subheader(f"RM{round(am.values[0],2)}")
       
           #lutfi
           with tab3:
               options = st.multiselect(
               'Choose Unpaid Payments:',
               type, default=type,key=key[2])
               lf_df = df.loc[df['NAME'] == 'Lutfi', options]
               lf = lf_df.sum(axis=1)
               lf_df['TOTAL'] = round(lf,2)
               st.table(lf_df.style.format({"API": "{:.2f}",
                                           "AIR": "{:.2f}",
                                           "WIFI": "{:.2f}",
                                           "OTHERS": "{:.2f}",
                                           "RENT": "{:.2f}",
                                           "REFUND": "{:.2f}",
                                           "TOTAL": "{:.2f}"
                                           }))
               st.write("Lutfi has to pay a total amount of:")
               st.subheader(f"RM{round(lf.values[0],2)}")
           #adnan
           with tab4:
               options = st.multiselect(
               'Choose Unpaid Payments:',
               type, default=type,key=key[3])
               ad_df = df.loc[df['NAME'] == 'Adnan', options]
               ad = ad_df.sum(axis=1)
               ad_df['TOTAL'] = round(ad,2)
               st.table(ad_df.style.format({"API": "{:.2f}",
                                           "AIR": "{:.2f}",
                                           "WIFI": "{:.2f}",
                                           "OTHERS": "{:.2f}",
                                           "RENT": "{:.2f}",
                                           "REFUND": "{:.2f}",
                                           "TOTAL": "{:.2f}"
                                           }))
               st.write("Adnan has to pay a total amount of:")
               st.subheader(f"RM{round(ad.values[0],2)}")
           #kimi
           with tab5:
               options = st.multiselect(
               'Choose Unpaid Payments:',
               type, default=type,key=key[4])
               km_df = df.loc[df['NAME'] == 'Kimi', options]
               km = km_df.sum(axis=1)
               km_df['TOTAL'] = round(km,2)
               st.table(km_df.style.format({"API": "{:.2f}",
                                           "AIR": "{:.2f}",
                                           "WIFI": "{:.2f}",
                                           "OTHERS": "{:.2f}",
                                           "RENT": "{:.2f}",
                                           "REFUND": "{:.2f}",
                                           "TOTAL": "{:.2f}"
                                           }))
               st.write("Kimi has to pay a total amount of:")
               st.subheader(f"RM{round(km.values[0],2)}")
       
       st.write("---")
       
if len(fix.loc[fix['YM'] == currentmonth]) != 0:
       calculate(currentmonth,fix,rent,flow)

calculate(lastmonth,fix,rent,flow)

import streamlit as st
import geopandas as gpd
import requests
import pandas as pd
from sqlalchemy import create_engine
import branca
import folium
from streamlit_folium import folium_static, st_folium
import plotly.express as px
from dash import Dash, dcc, html, Input, Output,dash_table
import dash_core_components as dcc
import dash_html_components as dhc
import matplotlib.pyplot as plt
import urllib
import geojson
from shapely.geometry import Point,LineString
#import pymysql
import mysql.connector

engine=create_engine("mysql+mysqlconnector://root:mypass@localhost/phonepe11")
year=st.sidebar.selectbox("Select the year",["Select year","2018","2019","2020","2021","2022","2023"])
quarter=st.sidebar.selectbox("Select the quarter",["Select quarter","Quarter1","Quarter2","Quarter3","Quarter4"])
var=st.sidebar.selectbox("Select graph to be displayed based on:",["Select","Total Transactions","Total Amount","Average amount per transaction"])
overall=st.sidebar.selectbox("Select your choice",["Select year and quarter","overall plot","category wise plot","Visualization for all years"])


year1='2018'
q='1.json'
@st.cache_data
def data_fetch(year,q):
    data=pd.read_sql("""select sum(count1) as Transactions, sum(amount1) as Total_Amount, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')""" % (year1,q),engine)
    rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s') group by State""" % (year1,q),engine)
    rech=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Recharge & bill payments")""" % (year1,q),engine)
    peer=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Peer-to-peer payments")""" % (year1,q),engine)
    merc=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Merchant payments")""" %(year1,q),engine)
    fin=pd.read_sql("""select  sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Financial Services")""" % (year1,q),engine)
    oth=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Others")""" % (year1,q),engine)
    
    

    year2=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 group by year1""",engine)
    #rec1=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount where name1=("Recharge & bill payments") from phonepe_table1""",engine)
    #peer1=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where name1=("Peer-to-peer payments")""",engine)
    #merc1=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where name1=("Merchant payments")""",engine)
    #fin1=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where name1=("Financial Services")""",engine)
    #oth1=pd.read_sql("""select sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where name1=("Others")""",engine)
    return data,rec,rech,peer,merc,fin,oth,year2
    #return data,rec,rech,peer,merc,fin,oth,year2,rec1,peer1,merc1,fin1,oth1

def plotg(data,rec,rech,peer,merc,fin,oth):
    col1,col2=st.columns(2)
    with col1:
        st.metric("Total Number of Transactions",int(data["Transactions"]))
    with col2:
        st.metric("Total Amount Collected","Rs. "+str(int(data["Total_Amount"])))

    st.metric("Average Amount Collected","Rs. "+str(int(data["Average_Amount"])))

    # data1=geojson.loads(open("states_india.geojson").read())
    # states = gpd.GeoDataFrame.from_features(data1, crs="EPSG:4326")
    df1 = requests.get(
        "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    ).json()
    states = gpd.GeoDataFrame.from_features(df1, crs="EPSG:4326")
    #states.head()
    statesmerge = states.merge(rec, how="right",left_on="ST_NM", right_on="State")
    statesmerge["geometry"] = statesmerge.geometry.simplify(0.05)

    #df1=gpd.read_file(r"C:\Users\shamr\Desktop\phonepe3\states_india.geojson")
    #app=Dash(__name__)
    fig = px.choropleth(
        statesmerge,
        geojson=df1,
        featureidkey='properties.ST_NM',
        locations= 'State',
        color=x,
        color_continuous_scale='Greens',
        hover_data=['Transactions','Total_Amount','Average_Amount']

    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)
    c1,c2,c3=st.columns(3)
    with c1:
        st.metric("Recharge and ",str(int(rech["Total_Amount"])))
    with c2:
        st.metric("Peer to peer payments",str(int(peer["Total_Amount"])))
    with c3:
        st.metric("Merchant Payments",str(int((merc["Total_Amount"]))))
    c4,c5,c6=st.columns(3)
    with c4:
        st.metric("Financial Services ",str(int(fin["Total_Amount"])))
    with c5:
        st.metric("Others",str(int(oth["Total_Amount"])))

    labels="Recharge and Bill Payments","Peer to Peer Payments","Merchant Payments","Financial Services","Others"
    amt=[int(rech["Total_Amount"]),int(peer["Total_Amount"]),int(merc["Total_Amount"]),int(fin["Total_Amount"]),int(oth["Total_Amount"])]
    fig1,ax1=plt.subplots()
    ax1.pie(amt,labels=labels,autopct='%1.1f%%')
    st.pyplot(fig1)
    #year2,rec1,peer1,merc1,fin1,oth1=data_overall()
    #if graph=="Overall plot":
        
        #st.bar_chart(year2["Total_Amount"])
    #fig=plt.subplots(amt,labels)

if year=="2018":
    year1='2018'
elif year=="2019":
    year1='2019'
elif year=="2020":
    year1='2020'
elif year=="2021":
    year1='2021'
elif year=="2022":
    year1='2022'
elif year=="2023":
    year1='2023'
if quarter=="Quarter1":
    q='1.json'
elif quarter=='Quarter2':
    q='2.json'
elif quarter=='Quarter3':
    q='3.json'
elif quarter=='Quarter4':
    if year=="2023":
        st.error("No data for 2023 Quarter4")
    else:
        q='4.json'

#data,rec,rech,peer,merc,fin,oth,year2,rec1,peer1,merc1,fin1,oth1=data_fetch(year1,q)
data,rec,rech,peer,merc,fin,oth,year2=data_fetch(year1,q)
if var=="Total Transactions":
    x="Transactions"
elif var=="Total Amount":
    x="Total_Amount"
elif var=="Average amount per transaction":
    x="Average_Amount"
if overall=="overall plot":
    year1='2018'
    plotg(data,rec,rech,peer,merc,fin,oth)
elif overall=="category wise plot":
    category=st.sidebar.selectbox("Select a category",["Select a category","Recharge & bill payments","Peer-to-peer payments","Merchant payments","Financial Services","Others"])
    if category=="Recharge & bill payments":
        rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Recharge & bill payments") group by State""" % (year1,q),engine)
        
    elif category=="Peer-to-peer payments":
        rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Peer-to-peer payments") group by State""" % (year1,q),engine)
    elif category=="Merchant payments":
        rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Merchant payments") group by State""" % (year1,q),engine)
    elif category=="Financial Services":
        rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Financial Services") group by State""" % (year1,q),engine)
    elif category=="Others":
        rec=pd.read_sql("""select state1 as State,sum(amount1) as Total_Amount,sum(count1) as Transactions, avg(amount1/count1) as Average_Amount from phonepe_table1 where year1=('%s') and quarter1=('%s')  and name1=("Others") group by State""" % (year1,q),engine)
    plotg(data,rec,rech,peer,merc,fin,oth)
elif overall=="Visualization for all years":
    graph=st.sidebar.selectbox("Display graph",["Overall plot","quarterwise plot"])           
    if graph=="Overall plot":
        fig2,ax2=plt.subplots()
        labels="2018","2019","2020","2021","2022","2023"
        ax2.pie(year2["Total_Amount"],labels=labels,autopct='%1.1f%%')
        st.pyplot(fig2)



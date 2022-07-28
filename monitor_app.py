#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:21:26 2022

@author: remionette
"""


import sqlite3
import streamlit as st
import pandas as pd

con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = []
for row in cur.fetchall():
    tables.append(row[0])

option = st.selectbox('PC NAME', (tables))
sql = "select * from {}".format(option)

df = pd.read_sql(sql, con)

if st.button('Refresh'):
    st.metric("GPU Name", df['name'].values[-1], "Drivers: " + df['driver'].values[-1] , delta_color="off")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "{} °C".format(df['temperature'].values[-1]))
    col2.metric("Total Memory", "{} Mb".format(df['memoryTotal'].values[-1]))
    col3.metric("Free Memory", "{} Mb".format(df['memoryFree'].values[-1]))
    st.download_button(label="Download data as CSV", data=df.to_csv().encode('utf-8'), file_name='data.csv', mime='text/csv')
    st.area_chart(df['temperature'])
    st.area_chart(df['memoryUsed'])

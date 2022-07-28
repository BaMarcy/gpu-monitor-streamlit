#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:21:26 2022

@author: remionette
"""

from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json
import streamlit as st
import pandas as pd


app = Flask(__name__)
con = sqlite3.connect('data.db', check_same_thread=False)
cur = con.cursor()

@app.route('/gpu', methods=["POST"])
def monitor_GPU():
    data = json.loads(request.data)
    # str, str, str, str, real, real, real, real
    l  =[
        datetime.now(),
        data["name"],
        data["driver"], 
        data["memoryTotal"], 
        data["memoryFree"], 
        data["memoryUsed"], 
        data["temperature"]
        ]
    print(data["table"])
    try:
        sql = '''INSERT INTO {} (date, name, driver, memoryTotal, memoryFree, memoryUsed, temperature)
                  VALUES ( ? , ? , ? , ? , ? , ? , ?)'''.format(data["table"])
        cur.execute(sql, l)
    except:
        sql = '''CREATE TABLE IF NOT EXISTS {} (date text, name text, driver text, memoryTotal real, memoryFree real, 
                    memoryUsed real, temperature real)'''.format(data["table"])
        cur.execute(sql)
    con.commit()
    return jsonify({'result': 'OK'})



app.run(threaded=True, host='0.0.0.0', port=6666)




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

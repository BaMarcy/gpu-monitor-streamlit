#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 12:20:37 2022

@author: remionette
"""

from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json

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

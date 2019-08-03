#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 15:10:53 2019

@author: i501895
"""

import cx_Oracle
import csv

con = cx_Oracle.connect('hr/hrpsw@localhost/orcl')
cur = con.cursor()
with open("hackathon_data.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='|')
    for lines in csv_reader:
        cur.execute(
            "insert into new_locations (customer_id, manufacturer_id, society_id,"
            " city_id, route_id, store_id,order_id,order_date, category_id,subcategory_id,"
            "product_id,product_quantity,selling_price_per_unit,total_cost,subscription"
            "product_addedtobasket_on ) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10,"
            ":11, :12, :13, :14, :15)",
            (lines['LOCATION_ID'], lines['STREET_ADDRESS'], lines['POSTAL_CODE'],
             lines['CITY'], lines['STATE_PROVINCE'], lines['COUNTRY_ID']))

cur.close()
con.commit()
con.close()
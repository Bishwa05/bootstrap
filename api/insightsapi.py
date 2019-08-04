import pandas as pd
import flask
from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# load default page
@app.route('/')
def home():
    return render_template('home.html')

# A route to return all cities
#@app.route('/mbh/v1/cities/all', methods=['GET'])
def api_all():
    cities = [
        {'id': 0},
        {'id': 1},
        {'id': 2},
        {'id': 3},
        {'id': 4}
    ]
    return jsonify(cities)


# A route to return all cities
@app.route('/mbh/v1/socity/details', methods=['GET'])
def api_socity_details():
    if 'storeid' in request.args:
        id = int(request.args['societyid'])
#load our data from CSV
    tx_data = pd.read_csv('../data/sample_data.csv')

    newdf = tx_data[['society_id','category_id','subcategory_id','product_id']]

#To find with the provided city
    newdf= newdf[newdf['society_id'] == id]
    newdf.groupby(['category_id', 'subcategory_id'])
    groupby_cond_counts = newdf.groupby(['category_id', 'subcategory_id']).count()
    print(groupby_cond_counts) #This to return to show the count. 
    print(newdf) #This to be return when we query by society_id
    export = newdf.to_json (orient='records')
    return jsonify(export)


@app.route('/mbh/v1/store/details', methods=['GET'])
def api_store_details():
    if 'storeid' in request.args:
        id = int(request.args['storeid'])
#load our data from CSV
    tx_data = pd.read_csv('../data/sample_data.csv')
    newdf = tx_data[['store_id','society_id','category_id','subcategory_id','product_id']]

    #To find with the provided city
    newdf= newdf[newdf['store_id'] == id]
    newdf.groupby(['society_id','category_id', 'subcategory_id'])
    groupby_cond_counts = newdf.groupby(['society_id','category_id', 'subcategory_id']).count()
    print(groupby_cond_counts) #This to return to show the count. 

    print(newdf) #This to be return when we query by store_id
    export = newdf.to_json (orient='records')
    return jsonify(export)

@app.route('/mbh/v1/city/details', methods=['GET'])
def api_city_details():
    if 'cityid' in request.args:
        id = int(request.args['cityid'])
#load our data from CSV
    tx_data = pd.read_csv('../data/sample_data.csv')
    newdf = tx_data[['city_id','manufacturer_id','society_id','store_id']]

#To find with the provided city
    newdf= newdf[newdf['city_id'] == id]
    newdf.groupby(['city_id', 'store_id'])
       # groupby_city_store_counts = newdf.groupby(['city_id', 'store_id']).count()
#print(groupby_city_store_counts) #This to return to show the count. 

    print(newdf) #This to be return when we query by cityid
    export = newdf.to_json (orient='records')
    return jsonify(export)

app.run()


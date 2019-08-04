import flask
import pandas as pd
from flask import request, jsonify, render_template
import predictDate as pd
import findUniqueCities as uc
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# load default page
@app.route('/')
def home():
    return render_template('home.html')

# route to load insights view
@app.route('/mbh/v1/insights')
def insights():
    return render_template('home.html')

# route to load AOV view
@app.route('/mbh/v1/aov')
def aov():
    return render_template('aov.html')

# A route to return all cities
@app.route('/mbh/v1/cities/all', methods=['GET'])
def api_all():
    cities = [
        {'id': 0},
        {'id': 1},
        {'id': 2},
        {'id': 3},
        {'id': 4}
    ]
    print(uc.findUniqueCities())
    return jsonify(cities)

# A route to get the socities by city ID
@app.route('/mbh/v1/societies/bycityid', methods=['GET'])
def societyByCityID():
    if 'cityid' in request.args:
        id = int(request.args['cityid'])

    societies = [
        {'id' : id*1001},
        {'id': id*1002},
        {'id': id*1003},
        {'id': id*1004}
    ]
    return jsonify(societies)

# A route to return customer product prediction / recommendation by society ID
@app.route('/mbh/v1/customers/bysocietyid', methods=['GET'])
def customerProductRecoBySocietyID():
    if 'societyid' in request.args:
        id = int(request.args['societyid'])
    products_tuple=pd.predict_next_purchase_date(1120112)
    print (products_tuple)
    products = [
        {'custid' : products_tuple[0][0], 'productid': products_tuple[0][1], 'recurring': products_tuple[0][2]}
        # {'custid' : id* 2, 'productid': id * 1002, 'recurring': 'Weekly'},
        # {'custid': id * 3, 'productid': id * 1003, 'recurring': 'Daily'},
        # {'custid': id * 4, 'productid': id * 1004, 'recurring': 'Monthly'}
    ]
    return jsonify(products)

# A route to return customer product prediction / recommendation by society ID
@app.route('/mbh/v1/orders/bysociety', methods=['GET'])
def orderRevenueBySocietyID():
    if 'societyid' in request.args:
        id = int(request.args['societyid'])

    tx_data = pd.read_csv('../data/sample_data.csv')
    newdf = tx_data[['subcategory_id', 'total_cost']]
    newdf.columns = ['subcatid', 'totrev']
    getsum = newdf.groupby(['subcatid']).sum()
    print(getsum) # Total revenue for each subcategory
    #orderdf = newdf.groupby(['subcategory_id']).count()
    # print(orderdf)#Total no of orders per sub category

    #final = pd.merge(getsum, orderdf, on='subcategory_id')
    #final.columns = ["Total_Revenue", "Total_Orders"]
    #print(final)  # Count of Orders per sub category
    #final['Total_Orders'].loc[final['Total_Orders'] >= 1] = final['Total_Revenue'] / final['Total_Orders']
    #print(final)  # AOV per sub category

    orders = [
        {'subcatid': id * 1, 'totrev': id * 1001 },
        {'subcatid': id * 2, 'totrev': id * 1002 },
        {'subcatid': id * 3, 'totrev': id * 1003},
        {'subcatid': id * 4, 'totrev': id * 1004},
        {'subcatid': id * 5, 'totrev': id * 1005},
        {'subcatid': id * 6, 'totrev': id * 1006},
        {'subcatid': id * 7, 'totrev': id * 1007},
    ]
    return jsonify(getsum.to_json ())

app.run()


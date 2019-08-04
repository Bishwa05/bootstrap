import flask
from flask import request, jsonify, render_template

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

    products = [
        {'custid' : id*1, 'productid': id * 1001, 'recurring': 'Monthly'},
        {'custid' : id* 2, 'productid': id * 1002, 'recurring': 'Weekly'},
        {'custid': id * 3, 'productid': id * 1003, 'recurring': 'Daily'},
        {'custid': id * 4, 'productid': id * 1004, 'recurring': 'Monthly'}
    ]
    return jsonify(products)

app.run()


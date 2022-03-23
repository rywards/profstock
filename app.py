# working from https://docs.sqlalchemy.org/en/14/tutorial/metadata.html
from sqlalchemy import MetaData, create_engine, insert,Table, Column, Integer, String, select
from sqlalchemy.orm import Session
from flask import Flask, render_template, request
from flask_s3 import FlaskS3
from urllib import response
import requests
import json

# initializing flask app and database connection
app = Flask(__name__)

engine = create_engine("mysql+mysqldb://root:root@localhost/profstock", echo=True, future=True)
session = Session(engine)
metadata_obj = MetaData()




# route decorators
# these determine the location of different endpoints
@app.route("/")
def home():
    return render_template("index.html")


# Gets list of all registered users
@app.route("/users", methods=['GET'])
def users():

    users = Table('users', metadata_obj, autoload_with=engine)
    statement = session.query(users).all()
    allusers = json.dumps([row._asdict() for row in statement], indent=4)
    return render_template('users.html', allusers=allusers)

@app.route("/userportfolio", methods=['GET'])
def userportfolio():
    # need uid and username
    return 56

@app.route("/userportfolio/change", methods=['POST'])
def changeportfolio():
    # need uid and username
    return 72

@app.route("/testdbcon")
def testdb():
    conn = mysql.connection
    cursor = conn.cursor()

    # fetchall gets all the results of query
    # fetchone gets one result from the query
    cursor.execute("select * from stocks where stockid = 4;")
    data = cursor.fetchone()
    return str(data)

@app.route("/SignUpPage.html")
def signup():
    return render_template("SignUpPage.html")

@app.route("/stocksearch.html")
def stockinfo():
    return render_template("stocksearch.html")


# Ryan Edwards
# this is where the ticker post request data goes
# we can do some calculations here as necessary
@app.route("/stockinfo.html", methods=['POST'])
def pullstockinfo():
    ticker = request.form['ticker']

    params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
    }

    api_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker + '/eod/latest', params)
    api_response = api_result.json()

    close = api_response['close']
    openprice = api_response['open']
    high = api_response['high']
    low = api_response['low']
    volume = api_response['volume']
    date = api_response['date']


    return render_template("stockinfo.html", 
                            ticker=ticker,  
                            close=close,
                            openprice=openprice,
                            high=high,
                            low=low,
                            volume=volume,
                            date=date)


if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'
# working from https://docs.sqlalchemy.org/en/14/tutorial/metadata.html
from sqlalchemy import MetaData, create_engine, insert,Table, Column, Integer, String, select
from sqlalchemy.orm import Session
import flask
from flask import Flask, render_template, request
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
def userportfolio(uid,username):
    return 56

@app.route("/userportfolio/change")
def changeportfolio(uid,username):
    return 72

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
    symbol = api_response['symbol']


    return render_template("stockinfo.html", 
                            symbol=symbol,  
                            close=close,
                            openprice=openprice,
                            high=high,
                            low=low,
                            volume=volume,
                            date=date)


if __name__ == '__main__':
    app.run(debug=True)

app.static_folder = 'static'
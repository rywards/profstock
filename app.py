from importlib.metadata import metadata
import json, requests
from textwrap import indent

from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from os import environ as env
from urllib.parse import quote_plus, urlencode
from urllib import response

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from sqlalchemy import MetaData, create_engine, insert,Table, Column, Integer, String, select
from sqlalchemy.orm import Session as Alcsession

# initializing database connection
engine = create_engine("mysql+mysqldb://root:root@localhost/profstock", echo=True, future=True)
alcsession = Alcsession(engine)
metadata_obj = MetaData()

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


# route decorators
# these determine the location of different endpoints
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/profile.html")
def profile():
    if (session):
        #return render_template("profile.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))
        return jsonify(session.get('user'), json.dumps(session.get('user')))
    else:
        return redirect("/login")


# Gets list of all registered users
@app.route("/users", methods=['GET'])
def users():
    users = Table('users', metadata_obj, autoload_with=engine)
    statement = alcsession.query(users).all()
    allusers = json.dumps([row._asdict() for row in statement], indent=4)

    if (session):
        sessioninfo=session.get('user')
        pretty=json.dumps(sessioninfo, indent=4)
        userinfo = json.loads(pretty)
        uid = userinfo['userinfo']['sub']
        username = userinfo['userinfo']['name']
        email = userinfo['userinfo']['email']
        
        statement = users.insert().values(uid=uid,
                                          username=username,
                                          email=email)
        alcsession.execute(statement)
        alcsession.commit()
        #return render_template("users.html", username=username)
        return jsonify(username)

@app.route("/topusers", methods=['GET'])
def topusers():
    return 45

# Ryan Edwards
# this is where the ticker post request data goes
# we can do some calculations here as necessary
@app.route("/stockinfo", methods=['POST'])
def pullstockinfo():
    ticker = request.form['ticker']

    stocks = Table('stocks', metadata_obj, autoload_with=engine)
    result = alcsession.query(stocks).filter_by(ticker = ticker).first()
    
    if not result:

        params = {
            'access_key': 'b690ef1a94c38681861a3a78272a9c98'
        }

        api_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker, params)
        api_response = api_result.json()
        name = api_response['name']
        newstock = stocks.insert().values(ticker=ticker,
                                          name=name)
        alcsession.execute(newstock)
        alcsession.commit()

    
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



    #return render_template("stockinfo.html", 
    #                        ticker=ticker,  
    #                        close=close,
    #                        openprice=openprice,
    #                       high=high,
    #                        low=low,
    #                        volume=volume,
    #                        date=date)
    return api_response

@app.route("/portfolio", methods=['POST','GET'])
def portfolio():
    
    users = Table('users', metadata_obj, autoload_with=engine)
    userstocks = Table('userstocks', metadata_obj, autoload_with=engine)
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)
    
    # check to make sure a session is active
    if (session):

        # get user id from session info in sqlalchemy query
        sessioninfo=session.get('user')
        pretty=json.dumps(sessioninfo, indent=4)
        userinfo = json.loads(pretty)
        uid = userinfo['userinfo']['sub']
        name = userinfo['userinfo']['name']
        result = alcsession.query(users).filter_by(uid = uid).first()
        uid = result[0]

        # get portfolio from sqlalchemy query
        existsconn = alcsession.query(userstocks).filter_by(portfolioid = uid).first()
        existsportfolio = alcsession.query(portfolios).filter_by(portfolioid = uid).all()
        if (not existsconn):
            createconn = userstocks.insert().values(portfolioid=uid,
                                                        uid=uid,
                                                        wid=uid)
            alcsession.execute(createconn)
            alcsession.commit()

        # creating a root entry
        if (not existsportfolio):
            stockid=0
            createportfolio = portfolios.insert().values(portfolioid=uid,
                                                         stockid=stockid)
            alcsession.execute(createportfolio)
            alcsession.commit()

        # adding or removing portfolio items
        if (request.method == 'POST'):
        
          ticker = request.form['ticker']
          status = request.form['changeport']
          tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).first()
          
          if (status == "Remove Portfolio"):
              portfremove = alcsession.query(portfolios).filter_by(portfolioid=uid, stockid=tickerexist[0]).delete()
              print(portfremove)
              print("remove")
              alcsession.commit()
              return redirect("/portfolio")
          
          if (status == "Add Portfolio"):
            portfadd = portfolios.insert().values(portfolioid=uid,
                                                 stockid=tickerexist[0])
            alcsession.execute(portfadd)
            alcsession.commit()
            return redirect("/portfolio")
              
        if (request.method == 'GET'):
          
          # cleaning up portfolio output
          #jsonport = json.dumps([row._asdict() for row in existsportfolio], indent=4)
          stockdata = {}
          data = []
          for row in existsportfolio:
              jsonport = json.dumps(row._asdict(), indent=4)
              jsonport = json.loads(jsonport)
              stockdata['portfolioid'] = jsonport['portfolioid']
              stockdata['stockid'] = jsonport['stockid']
              stockdata['buydate'] = jsonport['quantity']
              stockdata['initvalue'] = jsonport['initvalue']
              print(stockdata)
              data.append(stockdata)
              
          print(data)
          #return render_template("portfolio.html", stockdata=stockdata)
          return jsonify(stockdata)
    else:
        return redirect("/login")


@app.route("/watchlist", methods=['GET','POST'])
def watchlist():

    users = Table('users', metadata_obj, autoload_with=engine)
    watchlists = Table('watchlists', metadata_obj, autoload_with=engine)
    userstocks = Table('userstocks', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)

    if (session):
        
        sessioninfo=session.get('user')
        pretty=json.dumps(sessioninfo, indent=4)
        userinfo = json.loads(pretty)
        uid = userinfo['userinfo']['sub']
        name = userinfo['userinfo']['name']
        result = alcsession.query(users).filter_by(uid = uid).first()
        uid = result[0]

        existswatch = alcsession.query(watchlists).filter_by(wid = uid).first()
        if (not existswatch):
            createconn = watchlists.insert().values(uid=uid,
                                                    wid=uid,
                                                    stockid=0)
            alcsession.execute(createconn)
            alcsession.commit()
        
        existswatch = alcsession.query(watchlists).filter_by(wid = uid).all()
        
        watchlistdata = {}
        
        # this is used when the watchlist is being retrieved
        if (request.method == 'GET'):
            ids = []
            stocknames = []
            for row in existswatch:
                jsonport = json.dumps(row._asdict(), indent=4)
                jsonport = json.loads(jsonport)
                watchlistdata['stockid'] = jsonport['stockid']
                print(type(watchlistdata))
                ids.append(watchlistdata['stockid'])
            
            for e in range(len(ids)):
                try:
                    getname = alcsession.query(stocks).filter_by(stockid=ids[e]).first()
                    stocknames.append(getname[2])

                except TypeError:
                    continue

            #return render_template("WatchList.html",stocknames=stocknames)
            return jsonify(stocknames)
        
        # this is used when a stock is being added to the watchlist
        if (request.method == 'POST'):

            ticker = request.form['ticker']
            status = request.form['changelist']
            
            tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).first()
            
            if (status == "Remove Watchlist"):
              watchlistremove = alcsession.query(watchlists).filter_by(uid=uid, stockid=tickerexist[0]).delete()
              print(watchlistremove)
              print("remove")
              alcsession.commit()
              return redirect("/watchlist")
            
            print(tickerexist[0])
            watchlistinsert = watchlists.insert().values(uid=uid,
                                                   wid=uid,
                                                   stockid=tickerexist[0])
            alcsession.execute(watchlistinsert)
            alcsession.commit()
            
            #return render_template("WatchList.html",tickerexist=tickerexist)
            return jsonify(tickerexist)

    else:
        return redirect("/login")

@app.route("/stockadd", methods=['POST','GET'])
def stockadd():
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    conn = engine.connect()

    if (session):
        # get user id from session info in sqlalchemy query
        sessioninfo=session.get('user')
        pretty=json.dumps(sessioninfo, indent=4)
        userinfo = json.loads(pretty)
        uid = userinfo['userinfo']['sub']
        result = alcsession.query(users).filter_by(uid = uid).one()
        uid = result[0]

        # Stock id
        ticker = request.form['ticker']
        tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).one()
        stockid = tickerexist[0]

        addStock = portfolios.insert().values(portfolioid = uid, stockid = stockid)
        conn.execute(addStock)
        conn.commit()



@app.route("/stockremove", methods=['POST','GET'])
def stockremove():
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    conn = engine.connect()

    if (session):
        # get user id from session info in sqlalchemy query
        sessioninfo=session.get('user')
        pretty=json.dumps(sessioninfo, indent=4)
        userinfo = json.loads(pretty)
        uid = userinfo['userinfo']['sub']
        result = alcsession.query(users).filter_by(uid = uid).one()
        uid = result[0]

        # Stock id
        ticker = request.form['ticker']
        tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).one()
        stockid = tickerexist[0]

        # Execute and commit query
        removeStock = portfolios.delete().where(portfolios.c.portfolioid == portfolioid and portfolios.c.stockid == stockid)
        conn.execute(removeStock)
        conn.commit()

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

app.static_folder = 'static'
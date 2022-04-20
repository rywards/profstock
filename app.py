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
from sqlalchemy.sql import func

from flask import send_file


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

# function returns current user's information in JSON format
def session_info():
    sessioninfo = session.get('user')
    pretty=json.dumps(sessioninfo, indent=4)
    userinfo = json.loads(pretty)
    return userinfo

# function
def load_tables():
    users = Table('users', metadata_obj, autoload_with=engine)
    userstocks = Table('userstocks', metadata_obj, autoload_with=engine)
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)
    return users, userstocks, portfolios, stocks

# function for calling api
def stockAPI(ticker):
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

    return api_response


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
        userinfo = session_info()
        uid = userinfo['userinfo']['sub']
        username = userinfo['userinfo']['name']
        email = userinfo['userinfo']['email']

        statement = users.insert().values(uid=uid,
                                          username=username,
                                          email=email)
        alcsession.execute(statement)
        alcsession.commit()

        return jsonify(username)

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
        print(api_response)
        name = api_response['name']
        newstock = stocks.insert().values(ticker=ticker,
                                          name=name)
        alcsession.execute(newstock)
        alcsession.commit()

    # getting the most recent stock data
    params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
    }

    info_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker + '/eod/latest', params)
    name_result = requests.get('http://api.marketstack.com/v1/tickers/' + ticker, params)
    stock_info = info_result.json()
    stock_name = name_result.json()

    stock = json.dumps([stock_info, stock_name])

    return stock

@app.route("/portfolio", methods=['POST','GET'])
def portfolio():

    users = Table('users', metadata_obj, autoload_with=engine)
    userstocks = Table('userstocks', metadata_obj, autoload_with=engine)
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)

    # check to make sure a session is active
    if (session):

        userinfo = session_info()
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

        # creating a root entry in the portfolio
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

        userinfo = session_info()
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

# Andrew S. and Ryan Edwards
# Returns the users with highest portfolio return percentage
@app.route("/leaderboard", methods=['POST', 'GET'])
def leaderboard():

    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    users = Table('users', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)


    # Query to get portfolio id | sum(total invested) for each user
    sqlInvested = alcsession.query(users.username, portfolios.quantity, portfolios.ticker, portfolios.portfolioid, func.sum(portfolios.quantity * portfolios.initvalue).label('total_invested')
    ).join(users
    ).group_by(portfolios.portfolioid
    ).all()

    alcsession.commit()


    # Saves the returned dafta in the arrays
    for user in sqlInvested:
        users.append(user.portfolioid)
        usernames.append(user.username)
        invested.append(user.total_invested)


    getTickers = alcsession.query(portfolios.c.portfolioid, portfolios.c.quantity, stocks.c.ticker
    ).join(stocks, stocks.c.stockid == portfolios.c.stockid
    ).all()
    
    alcsession.commit()

    # Get current amounts from api
    for i in range(0, len(users)):
        total = 0
        for t in getTickers:
            if t.portfolioid == users[i]:
                api_reponse = stockAPI(t.ticker)

                print(api_reponse)
                init_value = 0
                init_value = t.quantity * api_reponse.get('open')

                total += init_value

        current_amounts.append(total)

    # Calculate ((current prices / total invested) - 1) * 100 for each user
    for j in range(0, len(users)):
        percentages.append((( float(current_amounts[j]) / float(invested[j])) - 1) * 100)

    for count in range(0, len(users)):
        indecies.append(count + 1)

    # Sort and return json to front end
    # https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    # This helped me sort 2 lists the same way
    zippedreturn = zip(percentages, usernames, indecies)
    sortedreturn = sorted(zippedreturn, reverse=True)

    # Returns json, in order, from largest percentage to smallest
    # Returns a list of elements, each element has 2 values, a percentage + or -, and the username
    #return jsonify(sortedreturn)
    return jsonify(sortedreturn)
    


@app.route("/sharing", methods=['POST', 'GET'])
def share():
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    users = Table('users', metadata_obj, autoload_with=engine)
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


    # Query to get portfolio id | sum(total invested) for each user
    sqlInvested = alcsession.query(portfolios.c.portfolioid, users.c.username, func.sum(portfolios.c.quantity * portfolios.c.initvalue).label('total_invested')
    ).join(users, users.c.uid == portfolios.c.portfolioid
    ).group_by(portfolios.c.portfolioid
    ).all()
    
    alcsession.commit()


    users = [] # Array to hold the users from the database
    invested = [] # Array to hold total amount invested by each user
    current_amounts = [] # Array to hold current amount user's stocks are worth
    percentages = [] # Holds percentage for each user up/down
    usernames = [] # Holds usernames
    tickers = [] # Holds a list of tickers for each user
    userStocks = [] # Holds the current user's stocks
    currentValues = [] # Holds init values for each user stock
    differences = [] # Holds difference in init values for each stock
    previousValues = [] # Holds previous values for each stock

    # Saves the returned data in the arrays
    for user in sqlInvested:
        users.append(user.portfolioid)
        usernames.append(user.username)
        invested.append(user.total_invested)
    
    getTickers = alcsession.query(portfolios.c.portfolioid, portfolios.c.quantity, stocks.c.ticker
    ).join(stocks, stocks.c.stockid == portfolios.c.stockid
    ).all()
    
    alcsession.commit()

    # Get current amounts from api
    for i in range(0, len(users)):
        total = 0
        for t in getTickers:
            if t.portfolioid == users[i]:
                api_reponse = stockAPI(t.ticker)

                init_value = 0
                init_value = t.quantity * api_reponse.get('open')

                total += init_value

        current_amounts.append(total)



    # Calculate ((current prices / total invested) - 1) * 100 for each user
    for j in range(0, len(users)):
        percentages.append((( float(current_amounts[j]) / float(invested[j])) - 1) * 100)

    # https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    # Sort both lists in the same way
    percentages_sorted, users_sorted = map(list, zip(*sorted(zip(percentages, users), reverse=True)))

    # Gets user's current position on the leaderboard
    # Gets user's total portfolio return
    for i in range(0, len(users_sorted)):
        if users_sorted[i] == uid: 
            leaderboardPos = i + 1
            totalPortfolioReturn = percentages_sorted[i]

    
    # ----------------------------------------------------------------------
    # This part is for finding best performing stock
    # Query to get portfolio id | sum(total invested) for each user
    sqlInvested = alcsession.query(portfolios.c.portfolioid, stocks.c.ticker, portfolios.c.quantity, stocks.c.name, portfolios.c.initvalue
    ).join(stocks, stocks.c.stockid == portfolios.c.stockid
    ).all()
    
    alcsession.commit()


    # Get current init values for each stock
    for stock in sqlInvested:
        if stock.portfolioid == uid: 
            userStocks.append(stock.name)
            previousValues.append(stock.quantity * stock.initvalue)
            api_response = stockAPI(stock.ticker)  # Call api
            init_value = 0
            init_value = stock.quantity * api_response.get('open')
            currentValues.append(init_value)


    # Find the largest difference between init values
    # We would then return the best performing stock, and how much percentage it is up
    percentage = 0
    for i in range(0, len(currentValues)):
        differences.append(float(currentValues[i]) - float(previousValues[i]))

        if differences[i] > percentage:
            bestStock = userStocks[i]
            percentage = differences[i]

    # Returns the user's total portfolio return, leaderboard position, and the user's best performing
    # stock, and how much that stock is up (percentage)
    # Still need to add in profile image
    #returnValuesJson = {'totalPortfolio' : totalPortfolioReturn, 'leaderboardPosition': leaderboardPos, 
    #                    'bestStock': bestStock, 'bestStockPercentage': percentage}
    #return returnValuesJson

    file = open("stats.html", "w")
    data = f"""<html>
            <head>
            <title>Stats</title>
            </head>
            <body>
  
            <p>Total Portfolio Return: {totalPortfolioReturn}</p>
            <p>Leaderboard Position: {leaderboardPos}</p>
            <p>Best Stock: {bestStock}</p>
            <p>{bestStock} percentage: {percentage}%</p>


  
            </body>
            </html>
            """
    file.write(data)
    file.close()

    return send_file("stats.html", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

app.static_folder = 'static'

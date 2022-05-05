from importlib.metadata import metadata
import json, requests
from textwrap import indent

from flask import Flask, render_template, request, jsonify, redirect, session, url_for, send_file
from os import environ as env
from urllib.parse import quote_plus, urlencode
from urllib import response

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from sqlalchemy import MetaData, create_engine, insert,Table, Column, Integer, String, select
from sqlalchemy.orm import Session as Alcsession
from sqlalchemy.sql import func

# initializing database connection
engine = create_engine('mysql+mysqldb://root:Warlord2000%4029!@localhost/profstock', echo=True, future=True)
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

# Function returns current user's information in JSON format.
def session_info():
    sessioninfo = session.get('user')
    pretty=json.dumps(sessioninfo, indent=4)
    userinfo = json.loads(pretty)
    return userinfo

# Function to get the initial purchase amount of a stock
# based on the buydate.
def stock_init_val(ticker, amount, buydate):

    print(ticker)
    # getting the most recent stock data
    params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
    }
    route = 'http://api.marketstack.com/v1/tickers/' + ticker + '/eod/' + buydate
    print(route)

    api_buydate = requests.get(route, params)
    buydate_info = api_buydate.json()
    print(buydate_info)

    buydate_value = buydate_info['close'] * amount

    return buydate_value

# Function to get the current value of a portfolio holding
def stock_curr_val(ticker, amount):
    # getting the most recent stock data
    print(ticker)
    params = {
    'access_key': 'b690ef1a94c38681861a3a78272a9c98'
    }
    route = 'http://api.marketstack.com/v1/tickers/' + ticker + '/eod/latest'

    api_current = requests.get(route, params)
    curr_info = api_current.json()

    curr_val = curr_info['close'] * amount

    return curr_val

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

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    users()
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

# Andrew S. and Ryan Edwards
# When this endpoint is hit, a zipped return of 3 lists is returned
# The 3 lists contain the usernames, portfolio return percentage, and leaderboard position
# of all of the users in the database
# The usernames are found in the first sqlalchemy query, and stored in the users list
# The return percentages are then found by taking the total_invested field from the first sqlalchemy
# query, and comparing it to the current_amounts. The result of this is stored in the percentages list.
# The indecies are found by generating a list of indecies for how many people are in the list, and 
# then simply sorting the list later.
# Once the users, percentages, and indecies lists are filled with the data, all 3 are sorted in the same way.
# The 3 sorted lists are then zipped, so all 3 can be returned to be displayed on the home page.
@app.route("/leaderboard", methods=['GET'])
def leaderboard():

    # These are the 3 tables the sqlalchemy queries will need to use
    portfolios = Table('portfolios', metadata_obj, autoload_with=engine)
    users = Table('users', metadata_obj, autoload_with=engine)
    stocks = Table('stocks', metadata_obj, autoload_with=engine)


    # This query gets the primary key, username, and the total amount invested for each user in the database
    sqlInvested = alcsession.query(portfolios.c.portfolioid, users.c.username, func.sum(portfolios.c.quantity * portfolios.c.initvalue).label('total_invested')
    ).join(users, users.c.uid == portfolios.c.portfolioid
    ).group_by(portfolios.c.portfolioid
    ).all()

    alcsession.commit()


    # These are all of the lists where data will be stored
    users = [] # Array to hold the users from the database
    invested = [] # Array to hold total amount invested by each user
    current_amounts = [] # Array to hold current amount user's stocks are worth
    percentages = [] # Holds percentage for each user up/down
    usernames = [] # Holds usernames
    tickers = [] # Holds a list of tickers for each user
    indecies = [] # Indexs for return

    # Saves the returned data from the first sqlachemy query in the lists
    for user in sqlInvested:
        users.append(user.portfolioid)
        usernames.append(user.username)
        invested.append(user.total_invested)


    # This query gets the primary key for who bought each stock, and then how much of the stock was bought.
    # It also gets the ticker, so we can use it to find the current amount of the stock now.
    getTickers = alcsession.query(portfolios.c.portfolioid, portfolios.c.quantity, stocks.c.ticker
    ).join(stocks, stocks.c.stockid == portfolios.c.stockid
    ).all()

    alcsession.commit()

    # Goes through all of the tickers that we just got from the previous query.
    # Goes through each user stored in the users list earlier.
    # If the primary key matches the user we are current searching for, we hit the api
    # to find the current price of the stock, and multiply it by the original quantity.
    # The total is then added onto the total variable, and at the end, the total
    # is stored in the current_amounts list.
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



    # Takes the current amount of the stocks - the total cost of the stocks to begin with, and divides it by
    # the total amount initially. Multiplying it by 100 then gives us the percentage up/down for each user
    for j in range(0, len(users)):
        percentages.append( ((float(current_amounts[j]) - float(invested[j])) / float(invested[j])) * 100)

    # Simply generates a list of how many indecies we need
    for count in range(0, len(users)):
        indecies.append(count + 1)


    # https://stackoverflow.com/questions/19931975/sort-multiple-lists-simultaneously
    # This helped me sort 2 lists the same way
    # Sorts the 3 lists that we need to return the same way. Now, the 3 lists that were created are all sorted the same way,
    # in order, and can be returned
    percentages_sorted, usernames_sorted, indecies_sorted = map(list, zip(*sorted(zip(percentages, usernames, indecies), reverse=True)))

    # This actually sorts the indecies list, so now each person has the correct index for leaderboard position
    for count in range(0, len(indecies)):
        indecies_sorted[count] = count + 1

    # Zips all 3 lists so they can be returned to the front end
    sortedreturn = zip(percentages_sorted, usernames_sorted, indecies_sorted)

    # Returns the 3 lists
    return sortedreturn

    '''
    # Calculate ((current prices / total invested) - 1) * 100 for each user
    for j in range(0, len(users)):
        percentages.append((( float(current_amounts[j]) / float(invested[j]))) * 100)

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
    print(sortedreturn[0][0])

    return sortedreturn
'''

# route decorators
# these determine the location of different endpoints
@app.route("/")
def home():
    leaderboardlist = leaderboard()
    return render_template("index.html", leaderboardlist=leaderboardlist)

@app.route("/profile", methods=['GET','POST'])
def profile():
    users = Table('users', metadata_obj, autoload_with=engine)

    if (session):

        userinfo = session_info()
        uid = userinfo['userinfo']['sub']
        username = userinfo['userinfo']['name']
        email = userinfo['userinfo']['email']
        picture = userinfo['userinfo']['picture']
        print("PATH  TO PICTURE: ", picture)

        if (request.method == 'GET'):
            statement = alcsession.query(users).filter_by(uid=uid).first()
            return render_template("profile.html", username=username,
                                                    email=email,
                                                    picture=picture)
        if (request.method == 'POST'):

            username = request.form['username']
            email = request.form['email']

            statement = alcsession.query(users).filter_by(uid=uid).update(username=username,
                                                                          email=email)
            alcsession.execute(statement)
            alcsession.commit()

            return redirect("/profile")


    else:
        return redirect("/login")

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

    date = stock_info['date']
    name = stock_name['name']
    openprice = stock_info['open']
    close = stock_info['close']
    high = stock_info['high']
    low = stock_info['low']
    volume = stock_info['volume']
    dividend = stock_info['dividend']

    stock = json.dumps([stock_info, stock_name])


    return render_template("stockinfo.html", date=date,
                                             name=name,
                                             openprice=openprice,
                                             high=high,
                                             low=low,
                                             volume=volume,
                                             dividend=dividend,
                                             ticker=ticker)

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

        # Keeping track of portfolios for users
        # Sets the active portfolio to the first index of portfolionames
        portfolionames = []
        for row in existsportfolio:
            portfolionames.append(row[5])
        try:
            activeportfolio = portfolionames[0]
        except:
            activeportfolio = ""

        # If the request type is a post request, go here.
        if (request.method == 'POST'):

          ticker = request.form['ticker']
          status = request.form['changelist']
          stockidexist = alcsession.query(stocks).filter_by(stockid = ticker).first()
          tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).first()

          if (status == "Change Portfolio"):
              activeportfolio = ticker
              getname = alcsession.query(portfolios).filter_by(portfolioid=uid,
                                                                name=ticker).all()
              data = []
              curr_val = 0
              for row in getname:
                  stockdata = {}
                  result = alcsession.query(stocks).filter_by(stockid=row.stockid).first()
                  stockdata['stockid'] = row.stockid
                  stockdata['stockname'] = result[2]
                  stockdata['buydate'] = row.buydate
                  stockdata['quantity'] = row.quantity
                  stockdata['initvalue'] = row.initvalue
                  stockdata['portname'] = row.name
                  activeportfolio = row.name

                  curr_val += stock_curr_val(result[1], row.quantity)

                  data.append(stockdata)
              #return render_template("portfolio.html")
              return render_template("portfolio.html", data=data,
                                                        curr_val=curr_val,
                                                        portfolionames=portfolionames,
                                                        activeportfolio=activeportfolio)

          if (status == "Remove Portfolio"):
              try:
                  portfremove = alcsession.query(portfolios).filter_by(portfolioid=uid, stockid=tickerexist[0]).delete()
                  alcsession.commit()
                  return redirect("/portfolio")
              except TypeError:
                  portfremove = alcsession.query(portfolios).filter_by(portfolioid=uid, stockid=stockidexist[0]).delete()
                  alcsession.commit()
                  return redirect("/portfolio")



          if (status == "Add Portfolio"):

            # buydate must be strictly in Y-m-d format.
            # ex. 2015-12-25 (christmas 2015)

            # Need to make sure input is correct or will get a bad request
            ticker = str(ticker)
            buydate = str(request.form['buydate'])
            quantity = int(request.form['quantity'])
            portname = request.form['portname']
            initvalue = stock_init_val(ticker, quantity, buydate)
            portfadd = portfolios.insert().values(portfolioid=uid,
                                                 stockid=tickerexist[0],
                                                 buydate=buydate,
                                                 quantity=quantity,
                                                 initvalue=initvalue,
                                                 name=portname)
            alcsession.execute(portfadd)
            alcsession.commit()
            return redirect("/portfolio")

        if (request.method == 'GET'):
          data = []
          curr_val = 0
          for row in existsportfolio:
              stockdata = {}
              portname = alcsession.query(portfolios).filter_by(stockid=row.stockid, name=activeportfolio).first()
              result = alcsession.query(stocks).filter_by(stockid=row.stockid).first()
              stockdata['stockid'] = row.stockid
              stockdata['stockname'] = result[2]
              stockdata['buydate'] = row.buydate
              stockdata['quantity'] = row.quantity
              stockdata['initvalue'] = row.initvalue
              curr_val += stock_curr_val(result[1], row.quantity)
              print(curr_val)

              data.append(stockdata)
          #return render_template("portfolio.html")
          return render_template("portfolio.html", data=data,
                                                    curr_val=curr_val,
                                                    activeportfolio=activeportfolio,
                                                    portfolionames=portfolionames)
    else:
        return redirect("/login")


# Handles call to watchlist endpoint
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


        existswatch = alcsession.query(watchlists).filter_by(wid = uid).all()

        # Keeping track of watchlists for users
        # sets active watchlist as first index
        watchlistnames = []
        for row  in existswatch:
            watchlistnames.append(row[3])

        try:
            activewatchlist = watchlistnames[0]
        except:
            activewatchlist = ""


        # this is used when the watchlist is being retrieved
        if (request.method == 'GET'):

            data = []
            for row in existswatch:
                watchlistdata = {}
                try:
                    result = alcsession.query(watchlists).filter_by(stockid=row.stockid, name=activewatchlist).first()
                    stockname = alcsession.query(stocks).filter_by(stockid=row.stockid).first()
                    watchlistdata['stockid'] = result.stockid
                    watchlistdata['stockname'] = stockname[2]
                    stockeod = stockAPI(stockname[1])
                    watchlistdata['currprice'] = stockeod['close']
                    data.append(watchlistdata)
                except:
                    continue


            return render_template("WatchList.html",data=data,
                                                    watchlistnames=watchlistnames)

        # this is used when a stock is being added to the watchlist
        if (request.method == 'POST'):

            ticker = request.form['ticker']
            status = request.form['changelist']

            tickerexist = alcsession.query(stocks).filter_by(ticker = ticker).first()
            stockidexist = alcsession.query(stocks).filter_by(stockid = ticker).first()

            # Sets the active watchlist to the ticker value
            # Uses this to find the new active watchlist.
            if (status == "Change Watchlist"):
                activewatchlist = ticker
                getname = alcsession.query(watchlists).filter_by(wid=uid,
                                                                  name=ticker).all()
                data = []
                for row in getname:
                    watchlistdata = {}
                    result = alcsession.query(watchlists).filter_by(stockid=row.stockid, name=activewatchlist).first()
                    stockname = alcsession.query(stocks).filter_by(stockid=row.stockid).first()
                    watchlistdata['stockid'] = row.stockid
                    watchlistdata['stockname'] = stockname[2]
                    stockeod = stockAPI(stockname[1])
                    watchlistdata['currprice'] = stockeod['close']
                    data.append(watchlistdata)
                #return render_template("portfolio.html")
                return render_template("WatchList.html", data=data,
                                                          watchlistnames=watchlistnames,
                                                          activewatchlist=activewatchlist)

            if (status == "Remove Watchlist"):
                try:
                    portfremove = alcsession.query(watchlists).filter_by(wid=uid, stockid=tickerexist[0]).delete()
                    alcsession.commit()
                    return redirect("/watchlist")
                except TypeError:
                    portfremove = alcsession.query(watchlists).filter_by(wid=uid, stockid=stockidexist[0]).delete()
                    alcsession.commit()
                    return redirect("/watchlist")

            if (status == "Add Watchlist"):
                watchname = request.form['watchname']
                watchlistinsert = watchlists.insert().values(uid=uid,
                                                   wid=uid,
                                                   stockid=tickerexist[0],
                                                   name=watchname)
                alcsession.execute(watchlistinsert)
                alcsession.commit()
                return redirect("/watchlist")

            return render_template("WatchList.html",tickerexist=tickerexist)

    else:
        return redirect("/login")


# Andrew, Ryan
# When this endpoint is hit, an html file is returned that contains a mini snapshot of the current
# user's profile. It contains the profile's image, the user's total portfolio return percentage up/down,
# the user's best performing stock, and what percentage that stock is up/down.
@app.route("/snapshot", methods=['POST', 'GET'])
def snapshot():
    # These are the 3 tables the sqlalchemy queries will need to use
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
        picture = userinfo['userinfo']['picture']

        result = alcsession.query(users).filter_by(uid = uid).first()
        uid = result[0]


        # This query gets the primary key, username, and the total amount invested for each user in the database
        sqlInvested = alcsession.query(portfolios.c.portfolioid, users.c.username, func.sum(portfolios.c.quantity * portfolios.c.initvalue).label('total_invested')
        ).join(users, users.c.uid == portfolios.c.portfolioid
        ).group_by(portfolios.c.portfolioid
        ).all()

        alcsession.commit()

        # These are all of the lists where data will be stored
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

        # This query gets the primary key for who bought each stock, and then how much of the stock was bought.
        # It also gets the ticker, so we can use it to find the current amount of the stock now.
        getTickers = alcsession.query(portfolios.c.portfolioid, portfolios.c.quantity, stocks.c.ticker
        ).join(stocks, stocks.c.stockid == portfolios.c.stockid
        ).all()

        print(getTickers)

        # Goes through all of the tickers that we just got from the previous query.
        # Goes through each user stored in the users list earlier.
        # If the primary key matches the user we are current searching for, we hit the api
        # to find the current price of the stock, and multiply it by the original quantity.
        # The total is then added onto the total variable, and at the end, the total
        # is stored in the current_amounts list.
        for i in range(0, len(users)):
            total = 0
            for t in getTickers:
                if t.portfolioid == users[i]:
                    api_reponse = stockAPI(t.ticker)

                    init_value = 0
                    init_value = t.quantity * api_reponse.get('open')

                    total += init_value

            current_amounts.append(total)

        # Takes the current amount of the stocks - the total cost of the stocks to begin with, and divides it by
        # the total amount initially. Multiplying it by 100 then gives us the percentage up/down for each user
        for j in range(0, len(users)):
            percentages.append( ((float(current_amounts[j]) - float(invested[j])) / float(invested[j])) * 100)

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
        # Query to get portfolio id, and stock info for all stocks in db
        sqlInvested = alcsession.query(portfolios.c.portfolioid, stocks.c.ticker, portfolios.c.quantity, stocks.c.name, portfolios.c.initvalue
        ).join(stocks, stocks.c.stockid == portfolios.c.stockid
        ).all()

        alcsession.commit()


        # Get current init_values for all stocks
        for stock in sqlInvested:
            if stock.portfolioid == uid:
                userStocks.append(stock.name)
                previousValues.append(stock.initvalue / stock.quantity)
                api_response = stockAPI(stock.ticker)  # Call api
                init_value = 0
                init_value = stock.quantity * api_response.get('open')
                currentValues.append(init_value)


        # Find the largest difference between init values (then vs. now)
        # We would then return the best performing stock, and how much percentage it is up
        percentage = 0
        bestStock = ""
        for i in range(0, len(currentValues)):
            differences.append(float(currentValues[i]) - float(previousValues[i]))

            if (differences[i] > percentage):
                print("differences done")
                bestStock = userStocks[i]
                percentage = differences[i]


        # Returns the file
        print("creating file")
        file = open("stats.html", "w")
        data = f"""<html>
                    <head>
                    <title>Stats</title>
                    </head>
                    <body>

                    <img src={picture}>
                    <p style="font-weight:bold">Total Portfolio Return: {totalPortfolioReturn}</p>
                    <p>Leaderboard Position: {leaderboardPos}</p>
                    <p>Best Stock: {bestStock}</p>
                    <p>{bestStock} percentage: {percentage}%</p>

                    </body>
                    </html>
                    """
        file.write(data)
        file.close()

        return send_file("stats.html", as_attachment=True)

    else:
        return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

app.static_folder = 'static'
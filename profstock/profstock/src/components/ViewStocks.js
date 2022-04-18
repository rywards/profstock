import React from 'react';
import axios from 'axios';

<>
<script src="https://unpkg.com/react@17/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</>

export default class ViewStocks extends React.Component {
    state = {
        stocks: []
    }

    componentDidMount() {
        axios.get('http://api.marketstack.com/v1/tickers/')
          .then(res => {
            const stocks = res.data;
            this.setState({ stocks });
          })
    }

    render() {
        return (
          <tbody>
            <tr>
                <th scope="row">Date of Information</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.date}>{stocks.date}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Close Price</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.closeprice}>{stocks.closeprice}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Open Price</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.openprice}>{stocks.openprice}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Day High</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.high}>{stocks.high}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Day Low</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.low}>{stocks.low}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Daily Volume</th>
                {
                this.state.stocks
                    .map(stocks =>
                    <td key={stocks.volume}>{stocks.volume}</td>
                    )
                }
            </tr>
          </tbody>
        )
    }
}


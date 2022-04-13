import React from 'react';
import axios from 'axios';

export default class ViewStocks extends React.Component {
    state = {
        date: '',
        closeprice: '',
        openprice: '',
        high: '',
        low: '',
        volume: ''
    }

    componentDidMount() {
        axios.get(`https://jsonplaceholder.typicode.com/users`)
          .then(res => {
            const persons = res.data;
            this.setState({ date, closeprice, openprice, high, low, volume });
          })
    }

    render() {
        return (
          <tbody>
            <tr>
                <th scope="row">Date of Information</th>
                {
                this.state.date
                    .map(date =>
                    <td key={date}>{date}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Close Price</th>
                {
                this.state.closeprice
                    .map(closeprice =>
                    <td key={closeprice}>{closeprice}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Open Price</th>
                {
                this.state.openprice
                    .map(openprice =>
                    <td key={openprice}>{openprice}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Day High</th>
                {
                this.state.high
                    .map(high =>
                    <td key={high}>{high}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Day Low</th>
                {
                this.state.low
                    .map(low =>
                    <td key={low}>{low}</td>
                    )
                }
            </tr>
            <tr>
                <th scope="row">Daily Volume</th>
                {
                this.state.volume
                    .map(volume =>
                    <td key={volume}>{volume}</td>
                    )
                }
            </tr>
          </tbody>
        )
    }
}


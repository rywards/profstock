import React from 'react';
import axios from 'axios';
import './SubLinks.js';

<>
<script src="https://unpkg.com/react@17/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</>


export default class SubInfo extends React.Component {
    
    state = {
        persons: []
    }
    componentDidMount() {
        axios.get(`https://jsonplaceholder.typicode.com/users`)
          .then(res => {
            const persons = res.data;
            this.setState({ persons });
          })
      }

    
    render() {
      return (
        <h3>
          <div id="homeContainer">
            <div id="Top10StockTable">
              {Top10Stock()}
            </div>
            

            <div id="TopUsersTable">
            <table className = "home2" align="center">
                <thead>
                <tr>
                    <th colSpan = '3'>Top users</th>
                </tr>
                <tr>
                    <th>#</th>
                    <th>Username</th>
                    <th>Name</th>
                </tr>
                </thead>
                <tbody>
                {
                this.state.persons
                    .map(person =>
                        <tr key={person.id}>
                        <td key={1}>{person.id}</td>
                        <td key={2}>{person.username}</td>
                        <td key={3}>{person.name}</td>
                      </tr>
                    )
                }
                </tbody>
            </table>
            </div>


            <div id="clear"></div>
        </div>
        </h3>);
    }  
}
function Top10Stock() {
    const items = [
    {
      id: 1,
      name: 'APPLE INC',
      marketCap:'$2.599 T',
      price: '$159.30',
      ticket: 'AAPL'
    },
    {
      id: 2,
      name: 'Saudi Aramco',
      marketCap:'$2.386 T',
      price: '$11.94',
      ticket: '2222.SR'
    },
    {
      id: 3,
      name: 'MICROSOFT CORP.',
      marketCap:'$2.090 T',
      price: '$278.91',
      ticket: 'MSFT'
    },
    {
      id: 4,
      name: 'Alphabet (Google)',
      marketCap:'$1.670 T',
      price: '$2,529',
      ticket: 'GOOG'
    },
    {
      id: 5,
      name: 'Amazon',
      marketCap:'$1.398 T',
      price: '$2,749',
      ticket: 'AMZN'
    },
    {
      id: 6,
      name: 'Tesla',
      marketCap:'$831.54 B',
      price: '$804.58',
      ticket: 'TSLA'
    },
    {
      id: 7,
      name: 'Berkshire Hathaway',
      marketCap:'$715.71 B',
      price: '$484,527',
      ticket: 'BRK-A'
    },
    {
      id: 8,
      name: 'Meta (Facebook)',
      marketCap:'$535.97 B',
      price: '$187.47',
      ticket: 'FB'
    },
    {
      id: 9,
      name: 'NVIDIA',
      marketCap:'$532.09 B',
      price: '$213.52',
      ticket: 'NVDA'
    },
    {
      id: 10,
      name: 'TSMC',
      marketCap:'$519.23 B',
      price: '$99.29',
      ticket: 'TSM'
    }]


    const itemRows = [];
    for (let item of items) {
      const row = (
        <tr key={item.id}>
          <td key={1}>{item.id}</td>
          <td key={2}>{item.name}</td>
          <td key={3}>{item.marketCap}</td>
          <td key={4}>{item.price}</td>
          <td key={5}>{item.ticket}</td>
        </tr>
      );
      itemRows.push(row);
    }
    return (
      <table className = "home2" align="center">
        <thead>
          <tr>
            <th colSpan = '5'>Top 10 Stocks by Market Cap</th>
          </tr>
          <tr>
            <th>#</th>
              <th>Name</th>
              <th>Market Cap</th>
              <th>Price</th>
              <th>ticket</th>
          </tr>
        </thead>
        <tbody>
          {itemRows}
        </tbody>
      </table>
    );
  }

  function TopUsers() {
    const items = [
    {
      id: 1,
      name: 'benadelson29',
      percent: '0 %',
    },
    {
      id: 2,
      name: 'servis38',
      percent: '0 %'
    },
    {
      id: 3,
      name: 'BJohnstone9291',
      percent: '0 %'
    },
    {
      id: 4,
      name: 'JohnstoneB',
      percent: '0 %'
    },
    {
      id: 5,
      name: 'trieuj77',
      percent: '0 %'
    },
    {
      id: 6,
      name: 'malonem6',
      percent: '0 %'
    }]

    
    const itemRows = [];
    for (let item of items) {
      const row = (
        <tr key={item.id}>
          <td key={1}>{item.id}</td>
          <td key={2}>{item.name}</td>
          <td key={3}>{item.percent}</td>
        </tr>
      );
      itemRows.push(row);
    }
    return (
      <table className = "home2" align="center">
        <thead>
          <tr>
            <th colSpan = '3'>Top users</th>
          </tr>
          <tr>
            <th>#</th>
            <th>Username</th>
            <th>Return #%</th>
          </tr>
        </thead>
        <tbody>
          {itemRows}
        </tbody>
      </table>
    );
  }
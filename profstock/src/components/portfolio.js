import React from 'react';
import axios from 'axios';



class Stock extends React.Component {
  stocks = fetch('http://localhost:5000/portfolio')

  items = [
    {
      id: 1,
      name: 'APPLE INC',
      marketCap: '$2.599 T',
      price: '$159.30',
      ticket: 'AAPL',
      quantity: '24'
    },
    {
      id: 2,
      name: 'Saudi Aramco',
      marketCap: '$2.386 T',
      price: '$11.94',
      ticket: '2222.SR',
      quantity: '65'
    },
    {
      id: 3,
      name: 'MICROSOFT CORP.',
      marketCap: '$2.090 T',
      price: '$278.91',
      ticket: 'MSFT',
      quantity: '23'
    },
    {
      id: 4,
      name: 'Alphabet (Google)',
      marketCap: '$1.670 T',
      price: '$2,529',
      ticket: 'GOOG',
      quantity: '20'
    },
    {
      id: 5,
      name: 'Amazon',
      marketCap: '$1.398 T',
      price: '$2,749',
      ticket: 'AMZN',
      quantity: '12'
    },
    {
      id: 6,
      name: 'Tesla',
      marketCap: '$831.54 B',
      price: '$804.58',
      ticket: 'TSLA',
      quantity: '42'
    },
    {
      id: 7,
      name: 'Berkshire Hathaway',
      marketCap: '$715.71 B',
      price: '$484,527',
      ticket: 'BRK-A',
      quantity: '22'
    },
    {
      id: 8,
      name: 'Meta (Facebook)',
      marketCap: '$535.97 B',
      price: '$187.47',
      ticket: 'FB',
      quantity: '23'
    },
    {
      id: 9,
      name: 'NVIDIA',
      marketCap: '$532.09 B',
      price: '$213.52',
      ticket: 'NVDA',
      quantity: '25'
    },
    {
      id: 10,
      name: 'TSMC',
      marketCap: '$519.23 B',
      price: '$99.29',
      ticket: 'TSM',
      quantity: '4'
    }]
  constructor(props) {
    super(props);
    this.state = { value: '' };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleClick = (event) => {

    this.setState({ value: event.target.value });

    this.removeStock(this.state.value);
    event.preventDefault();
  }
  handleSubmit(event) {
    alert('Your stock is: ' + this.state.value);
    event.preventDefault();
  }

  removeStock(ticket) {
    var list = this.items;
    console.log(ticket)
    for (let i = 0; i < list.length; i++) {

      if (list[i].ticket === ticket) {
        //alert('match found');
        list[i].quantity = 'i';
      }
    }

  }

  sayHello() {
    alert('You clicked me!');
  }

  createlist() {
    const list = this.items.map((item) =>
      <tr key={item.id}>
        <td>{item.name}</td>
        <td>{item.quantity}</td>
        <button value={item.ticket} onClick={this.handleClick}>Remove</button>
      </tr>
    );
    return (
      <tbody>{list}</tbody>
    )

  }


  render() {
    
    return (
      <>

        <div id="homeContainer">
          <div id="Top10StockTable">
            <div class="tickerinfo">

              <table className="home2" align="center">
                <thead>
                  <tr>
                    <th>stock</th>
                    <th>quantity</th>
                  </tr>
                </thead>

                {this.createlist()}

              </table>

            </div>
          </div>
        </div>
      </>
    );
  }
}

export default Stock;
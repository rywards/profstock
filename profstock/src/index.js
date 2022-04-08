import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

class Stock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: 'MSFT'};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('Your stock is: ' + this.state.value);
    event.preventDefault();
  }
  
  render() {
    console.log(this.state)
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

    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Stock:
          <select value={this.state.value} onChange={this.handleChange}>
            <option value="MSFT">MICROSOFT</option>
            <option value="AAPL">APPLE</option>

          </select>
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}


ReactDOM.render(
  <Stock />,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

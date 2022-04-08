import logo from './logo.svg';
import './App.css';

function App() {
  return (

        
        <NumberList numbers={numbers} />
 
  );
}

function ListItem(props) {
  // Correct! There is no need to specify the key here:
  return <option>{props.value}</option>;
}

function NumberList(props) {
  const numbers = props.numbers;
  const listItems = numbers.map((number) =>
    // Correct! Key should be specified inside the array.
    <ListItem key={number.toString()} value={number} />
  );
  return (
    <select>
      {listItems}
    </select>
  );
}

const numbers = [1, 2, 3, 4, 5];
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

export default App;

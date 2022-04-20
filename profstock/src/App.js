import logo from './logo.svg';
import './App.css';

import PersonList from './components/PersonList.js';
import SubLinks from './components/SubLinks';
import StockList from './components/StockList';

function App() {
  return (
    <div ClassName="App">
      <SubLinks/>
      <StockList/>
    </div>
  )
}

export default App;

//import logo from './logo.svg';
import './App.css';
//import './style.css'
import StockSearch from './components/StockSearch.js';
import AddStock from './components/AddStock.js';
import ViewStocks from './components/ViewStocks.js'
import SubLinks from './components/SubLinks.js';
import PersonList from './components/ProfileInfo.js';
import UserEdit from './components/ProfileEdit.js';

//import PersonList from './components/PersonList.js';

function App() {
  return (
    <div ClassName="StockHome">
      <header>
        <h1>ProfStock</h1>
      </header>
      <SubLinks/>
      <StockSearch/>
      <AddStock/>
      <ViewStocks/>

  

      <footer>
        <p></p>
      </footer>


    </div>
  )
}

export default App;

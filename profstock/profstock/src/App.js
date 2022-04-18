//import logo from './logo.svg';
import './profileEdit.css';
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
    <div >
      <header>
        <h1>Profile Page</h1>
      </header>
      <PersonList/>
      <UserEdit/>
      

  

      <footer>
        <p></p>
      </footer>


    </div>
  )
}

export default App;

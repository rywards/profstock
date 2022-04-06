import './App.css';
//import '../../static/style.css';
//<PersonList/>
import PersonList from './components/PersonList.js';
import SubInfo from './components/StockList.js';
import SubLinks from './components/SubLinks.js';

function App() {
  return (
    <div ClassName="StockHome">
      
      <header>
      <h1>ProfStock</h1>
      </header>
      
      <SubLinks/>
      <SubInfo/>
      
      <footer>
      <p></p>
      </footer>
      <p><PersonList/></p>
    </div>
    
  )
}

export default App;

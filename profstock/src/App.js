import './App.css';
//import '../../static/style.css';
//<PersonList/>
import PersonList from './components/PersonList.js';
import SubInfo from './components/StockList.js';
import SubLinks from './components/SubLinks.js';

function App() {
  let users = fetch('http://localhost:5000/users');
  ///*
  return window.print(users);
    //console.log("users are " + users.uid)
  
  //*/
 
  /*
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
    </div>
    
  )
  /*/
}

export default App;

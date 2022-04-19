import logo from './logo.svg';
import './App.css';

import PersonList from './components/PersonList.js';
import SubLinks from './components/SubLink.js';
import WatchInfo from './components/Watchlist';

function App() {
  return (
    <div ClassName="Watchlist">
     
     <header>
      <h1>ProfStock</h1>
      </header>
      
      <SubLinks/>
      <WatchInfo/>

  
      <footer>
      <p></p>
      </footer>
      <p><PersonList/></p>
    </div>
  )
}

export default App;
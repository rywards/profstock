import './App.css';
import Stock from './components/Portfolio';
import SubLinks from './components/SubLinks';

function App() {
  return (
    <div ClassName="StockHome">
        <header>
          <h1>ProfStock</h1>
        </header>
        <SubLinks />
        <Stock />
          
    </div>
 
  );
}

export default App;

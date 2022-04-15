import './App.css';
import Stock from './components/portfolio';
import SubLinks from './components/sublink';

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

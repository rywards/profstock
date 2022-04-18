import './App.css';
import StockSearch from './components/StockSearch.js';
import AddStock from './components/AddStock.js';
import ViewStocks from './components/ViewStocks.js'
import SubLinks from './components/SubLinks.js';

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


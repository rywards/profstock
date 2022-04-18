import './App.css';
import StockSearch from './components/StockSearch.js';
import AddStock from './components/AddStock.js';
import ViewStocks from './components/ViewStocks.js'
import SubLinks from './components/SubLinks.js';

function App() {
    return (
        <div>
            <header>
                <h1>StockInfo</h1>
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


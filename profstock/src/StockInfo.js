import './style.css';
import StockSearch from './components/StockSearch.js';
import AddStock from './components/AddStock.js';
import ViewStocks from './components/ViewStocks.js'

function App() {
    return (
        <div>
            <header>
                <h1>ProfStock</h1>
            </header>
            <StockSearch/>
            <AddStock/>
            <ViewStocks/>

            <footer>
                <p></p>
            </footer>


        </div>
    )
}


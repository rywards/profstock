import './profileEdit.css';
import PersonList from './components/ProfileInfo.js';
import UserEdit from './components/ProfileEdit.js';

function App() {
    return (
        <div>
            <header>  
            /*Used to compile components and display profile info */
            <title> Profile Page </title> 
            </header>  
            <h1 class= "pfph1"></h1>
            
            <PersonList/>
            <UserEdit/>
        </div>


    )
    }
   

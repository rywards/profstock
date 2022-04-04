import logo from './logo.svg';
import './App.css';

/*
Resources for getting authentication working
https://auth0.com/blog/complete-guide-to-react-user-authentication/
https://www.youtube.com/watch?v=MqczHS3Z2bc
https://www.youtube.com/watch?v=aRBgA8N0ioM&t=373s
*/
import PersonList from './components/PersonList.js';

function App() {
  return (
    <div ClassName="App">
      <PersonList/>
    </div>
  )
}

export default App;
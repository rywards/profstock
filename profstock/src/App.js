import './App.css';
import LoginButton from './components/LoginButton';
import LogoutButton from './components/LogoutButton';

/*
Resources for getting authentication working

https://auth0.com/blog/complete-guide-to-react-user-authentication/
https://www.youtube.com/watch?v=MqczHS3Z2bc
https://www.youtube.com/watch?v=aRBgA8N0ioM&t=373s

*/

function App() {
  return (
    <>
    <LoginButton/>
    <LogoutButton/>
    </>
  );
}

export default App;

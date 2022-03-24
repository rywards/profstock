import './App.css';
import LoginButton from './components/LoginButton';
import LogoutButton from './components/LogoutButton';
import { useAuth0 } from "@auth0/auth0-react";

/*
Resources for getting authentication working

https://auth0.com/blog/complete-guide-to-react-user-authentication/
https://www.youtube.com/watch?v=MqczHS3Z2bc
https://www.youtube.com/watch?v=aRBgA8N0ioM&t=373s

*/

function App() {
  const { user } = useAuth0();
  //const userInfo = JSON.stringify(user, null, 2);
  //const primaryKey = userInfo.sub;

  //console.log(primaryKey);
  return (
    <>
    <LoginButton/>
    <LogoutButton/>
    <div className="row">
        <pre className="col-12 text-light bg-dark p-4">
          {JSON.stringify(user, null, 2)}
        </pre>
    </div>
    </>
  );
}

export default App;

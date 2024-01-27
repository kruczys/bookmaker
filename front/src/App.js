import Bets from './Bets';
import {UserProvider} from "./UserContext";
import Signup from "./Signup";
import Login from "./Login";
import UserInfo from "./UserInfo";

function App() {
  return (
      <UserProvider>
          <h3>Bukmacher.pl - tutaj przegrasz wszystkie swoje pieniadze! :)</h3>
          <Login />
          <Signup />
          <UserInfo/>
          <Bets/>
      </UserProvider>
  );
}

export default App;

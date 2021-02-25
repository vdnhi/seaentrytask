import { useState } from "react";
import EventFeed from "./containers/EventFeed";
import LoginPage from "./containers/LoginPage";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  return (
    <div className="App">
      {window.sessionStorage.getItem("token") !== null ? <EventFeed /> : <LoginPage onChangeAuthState={setIsAuthenticated}/>}
    </div>
  );
}

export default App;

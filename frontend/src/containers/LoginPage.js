import { useState } from "react";
import { Button, FormGroup, InputGroup } from "@blueprintjs/core";
import { AppToaster } from "../components/Toaster";
import axios from "axios";
import CryptoJS from "crypto-js";

function LoginPage(props) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    axios
      .post("user/prelogin/", {
        username: username,
      })
      .then(function (response) {
        const key = response.data["key"];
        axios
          .post("user/login/", {
            username: username,
            password: CryptoJS.AES.encrypt(password, key).toString(),
            role: 1,
          })
          .then(function (response) {
            AppToaster.show({ message: "Login successful", intent: "success" });
            const token = response.data["token"];
            const userId = response.data["user_id"];
            window.sessionStorage.setItem("token", token);
            window.sessionStorage.setItem("userId", userId);
            props.onChangeAuthState(true);
          })
          .catch(function (error) {
            console.log(error);
            AppToaster.show({ message: "Login failed!", intent: "warning" });
          });
      })
      .catch(function (error) {
        AppToaster.show({ message: "Login failed!", intent: "warning" });
      });
  };

  return (
    <div>
      <FormGroup label="Username" labelFor="username-input">
        <InputGroup
          id="username-input"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </FormGroup>
      <FormGroup label="Password" labelFor="password-input">
        <InputGroup
          id="password-input"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </FormGroup>

      <Button intent="primary" text="Login" onClick={handleLogin} />
    </div>
  );
}

export default LoginPage;

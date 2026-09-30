import { useState } from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ActionCard from "./ActionCard";
import mainbg from "../assets/mainbg.png";

function AppLayout() {
  const [name, setName] = useState("");

  const [planet, setPlanet] = useState({
    id: "",
    name: "",
    image: "",
    story: "",
    properties: {}
  });

  const [userProp, setUserProp] = useState({
    maxAcc: Math.floor(Math.random() * (500 - 300 + 1)) + 300,
    o2: 19,
    hull: 28,
    fuel: 40,
    requiredElements: ["Oxygen", "Hydrogen", "Iron", "Carbon"],
    collectedElements: []
  });

  return (
    <div
      className="app"
      style={{ backgroundImage: `url(${mainbg})` }}
    >
      <ActionCard userProp={userProp} />

      <Navbar />

      <main>
        <Outlet
          context={{
            name,
            setName,
            planet,
            setPlanet,
            userProp,
            setUserProp
          }}
        />
      </main>
    </div>
  );
}

export default AppLayout;
import { useState } from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import ActionCard from './ActionCard'
import mainbg from "../assets/mainbg.png";

function AppLayout() {
  const [name, setName] = useState("");
  const [planet, setPlanet] = useState("")

  return (
    <div
      className="app"
      style={{ backgroundImage: `url(${mainbg})` }}
    >
      <ActionCard />
      <Navbar />

      <main>
        <Outlet context={{ name, setName ,planet, setPlanet}} />
      </main>
    </div>
  );
}

export default AppLayout;
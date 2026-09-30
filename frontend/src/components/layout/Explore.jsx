import { useOutletContext, useNavigate } from "react-router-dom";
import "./Explore.css";
import { useState,useEffect } from "react";

function Explore() {
  const { name } = useOutletContext();
  const [data, setData] = useState("")
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch("http://127.0.0.1:8000/explore",{
        "method":"GET"
      })
      const data = await res.json()
      console.log(data)
      setData(data)

    }

    fetchData()  
  
  }, [])
  

  return (
    <div className="explore-page">

      <div className="terminal page2-terminal">

        <p className="terminal-line">
          <span >&gt;&gt;&gt;</span> system back online
        </p>

        <p className="system-message">
          <span className="terminal-line-span">&gt;&gt;&gt;</span>{" "}
          Welcome back, {name || "[user]"}. Life support is critical:{" "}
          <strong>O2</strong> reserves are plummeting below 19%,{" "}
          <strong>ship hull</strong> strength is 28% and{" "}
          <strong>fuel</strong> less than 40%. Five mysterious stars flicker
           on your navigation terminal. Scan their compositions, manage
            your route carefully, and secure life-saving resources before the 
            deep space claims you.
        </p>

        <button
          className="proceed-btn"
          onClick={() => navigate("/planetSelection")}
        >
          proceed
        </button>

      </div>

    </div>
  );
}

export default Explore;
import { NavLink } from "react-router-dom";
import { Howler, Howl } from "howler";
import { useState, useEffect } from "react";
import logo from "../assets/dedsec.png";
import "./Navbar.css";
import soundOn from "../assets/soundOn.png";
import soundOff from "../assets/soundOff.png";
import bgMusic from "../assets/bgmusic.wav";

const sound = new Howl({
  src: [bgMusic],
  volume: 0.4,
  loop: true
});

function Navbar() {
  const [muted, setMuted] = useState(false);

  useEffect(() => {
    sound.play();
  }, []);

  const toggleMute = () => {
    Howler.mute(!muted);
    setMuted(!muted);
  };

  return (
    <div className="navbar">
      <img src={logo} alt="DEDSEC" className="navbar-logo" />

      <div className="navbar-links">
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "activeBtnCls" : ""
          }
        >
          Play
        </NavLink>

        <NavLink to="/how-to-play">
          How to play
        </NavLink>

        <NavLink to="/about">
          About Us
        </NavLink>
      </div>

      <div className="muteBtn" onClick={toggleMute}>
        {muted ? (
          <img src={soundOff} />
        ) : (
          <img src={soundOn} />
        )}
      </div>
    </div>
  );
}

export default Navbar;
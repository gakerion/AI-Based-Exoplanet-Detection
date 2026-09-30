import { useOutletContext, useNavigate } from "react-router-dom";
import { TypeAnimation } from "react-type-animation";
import { useState } from "react";
import "./Home.css";

function Home() {
  const { name, setName } = useOutletContext();
  const navigate = useNavigate();

  const [showNameEntered, setShowNameEntered] = useState(false);
  const [showBrain, setShowBrain] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleProceed = () => {
    if (!name.trim() || loading) return;

    setLoading(true);

    // Show "name entered"
    setTimeout(() => {
      setShowNameEntered(true);
    }, 300);

    // Show "waking up brain.exe..."
    setTimeout(() => {
      setShowBrain(true);
    }, 1300);

    // Navigate after everything
    setTimeout(() => {
      navigate("/missionIntro");
    }, 2800);
  };

  return (
    <div className="home">

      <div className="terminal">

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span>{" "}
          <TypeAnimation
            sequence={["welcome"]}
            speed={50}
            cursor={false}
          />
        </p>

        <div className="terminal-space"></div>

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span>{" "}
          <TypeAnimation
            sequence={["type your name to play"]}
            speed={40}
            cursor={false}
          />
        </p>

        <div>
          <span
            className="terminal-line-span"
            style={{ color: "#7fffff", fontWeight: "bold" }}
          >
            &gt;&gt;&gt;{" "}
          </span>

          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="name-input"
            disabled={loading}
          />
        </div>

        {showNameEntered && (
          <p className="terminal-line">
            <span>&gt;&gt;&gt;</span>{" "}
            <TypeAnimation
              sequence={["name entered"]}
              speed={40}
              cursor={false}
            />
          </p>
        )}

        {showBrain && (
          <p className="terminal-line">
            <span>&gt;&gt;&gt;</span>{" "}
            <TypeAnimation
              sequence={["waking up brain.exe..."]}
              speed={40}
              cursor={false}
            />
          </p>
        )}

        <button
          className="proceed-btn"
          onClick={handleProceed}
          disabled={!name.trim() || loading}
        >
          {loading ? "loading..." : "proceed"}
        </button>

      </div>

    </div>
  );
}

export default Home;
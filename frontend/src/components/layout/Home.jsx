import { useOutletContext, useNavigate } from "react-router-dom";
import './Home.css'


function Home() {
  const { name, setName } = useOutletContext();
  const navigate = useNavigate();

  const handleProceed = () => {
    if (!name.trim()) return;

    navigate("/missionIntro");
  };

  return (
    <div className="home">

      <div className="terminal">

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span> welcome
        </p>

        <div className="terminal-space"></div>

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span> type your name to play
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
          />
        </div>

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span> name entered
        </p>

        <p className="terminal-line">
          <span>&gt;&gt;&gt;</span> waking up brain.exe...
        </p>

        <button
          className="proceed-btn"
          onClick={handleProceed}
          disabled={!name.trim()}
        >
          proceed
        </button>

      </div>

    </div>
  );
}

export default Home;
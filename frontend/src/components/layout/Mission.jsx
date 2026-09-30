import { useOutletContext, useNavigate } from "react-router-dom";
import "./Mission.css";

function Mission() {
  const { planet } = useOutletContext();
  const navigate = useNavigate();

  return (
    <div className="mission-page">
      <div className="mission-box">
        <div className="mission-planet">
          <img
            src={planet.image}
            alt={planet.name}
            className="mission-planet-image"
          />

          <h2>Star ID: {planet.id}</h2>
          <p>Name: {planet.name}</p>
        </div>

        <div className="mission-elements">
          <p>
            <span>&gt;&gt;&gt;</span> You have collected the following elements:
          </p>

          <p><span>&gt;&gt;&gt;</span> Oxygen</p>
          <p><span>&gt;&gt;&gt;</span> Metallicity</p>
          <p><span>&gt;&gt;&gt;</span> Hydrogen</p>
        </div>
      </div>

      <div className="mission-buttons">
        <button onClick={() => navigate("/planetDetails")}>
          back
        </button>

        <button onClick={() => navigate("/missionResult")}>
          proceed
        </button>
      </div>
    </div>
  );
}

export default Mission;
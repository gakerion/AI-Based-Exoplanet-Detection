import { useOutletContext, useNavigate } from "react-router-dom";
import "./MissionIntro.css";

function MissionIntro() {
  const { name, userProp } = useOutletContext();
  const navigate = useNavigate();

  return (
    <div className="mission-intro-page">

      <div className="mission-terminal">

        <p className="mission-line">
          <span>&gt;&gt;&gt;</span> system back online
        </p>

        <div className="mission-message">

          <span>&gt;&gt;&gt;</span>{" "}
          System diagnostic complete. Good morning,
          Commander {name || "user"}. All primary crew bio
          metrics indicate unresponsive states. Vessel is
          currently adrift in deep space with max. acceleration of{"   "}
          <strong>{userProp.maxAcc} m/s²</strong>. Your mission, should you choose
          to accept it: identify target exoplanets, verify
          resource compositions, and save your crew mates by
          navigating to these exoplanets and collecting the
          required elements. Awaiting orders.

        </div>

        <button
          className="proceed-btn"
          onClick={() => navigate("/explore")}
        >
          proceed
        </button>

      </div>

    </div>
  );
}

export default MissionIntro;
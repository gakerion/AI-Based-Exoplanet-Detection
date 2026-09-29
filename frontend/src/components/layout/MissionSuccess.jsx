import { useNavigate, useOutletContext } from "react-router-dom";
import "./MissionSuccess.css";

import earth from "../../assets/earth.png";

function MissionSuccess() {
  const navigate = useNavigate();
  const { name } = useOutletContext();

  const planet = {
    id: "XXXXXXXX",
    name: "Kepler 1b, XXXXXXX",
    image: earth,
  };

  const collectedElements = ["X", "Y", "Z"];

  return (
    <div className="success-page">

      <div className="success-card">

        {/* LEFT - Planet information */}
        <div className="success-planet">

          <div className="success-image-box">
            <img
              src={planet.image}
              alt={planet.name}
              className="success-planet-image"
            />
          </div>

          <h3>
            Star ID: {planet.id}
          </h3>

          <p>
            Name: {planet.name}
          </p>

        </div>


        {/* RIGHT - Terminal message */}
        <div className="success-terminal">

          <p className="success-message">
            <span>&gt;&gt;&gt;</span>{" "}
            Congratulations: you have successfully rescued yourself,
            the crew mates and the ship somehow. You barely made it alive.
          </p>

          <p>
            <span>&gt;&gt;&gt;</span>{" "}
            You collected the following elements:
          </p>

          {collectedElements.map((element) => (
            <p key={element}>
              <span>&gt;&gt;&gt;</span> {element}
            </p>
          ))}

        </div>

      </div>


      {/* Sign off button */}
      <button
        className="signoff-btn"
        onClick={() => navigate("/")}
      >
        sign off, for now
      </button>

    </div>
  );
}

export default MissionSuccess;
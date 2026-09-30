import { useOutletContext } from "react-router-dom";
import "./MissionResult.css";

function MissionResult() {
  const { planet } = useOutletContext();

  const failedElements = ["X", "Y", "Z"];

  return (
    <div className="result-page">

      <div className="result-card">

        {/* LEFT - Planet information */}
        <div className="result-planet">

          <div className="planet-image-box">
            <img
              src={planet.image}
              alt={planet.name}
              className="result-planet-image"
            />
          </div>

          <h3>
            Star ID: {planet.id}
          </h3>

          <p>
            Name: {planet.name}
          </p>

        </div>


        {/* RIGHT - Terminal */}
        <div className="result-terminal">

          <p>
            <span>&gt;&gt;&gt;</span>{" "}
            Congratulations: you have successfully rescued yourself, the crew mates and the ship somehow. You barely made it alive.
          </p>

          <p><span>&gt;&gt;&gt;</span> Oxygen</p>
          <p><span>&gt;&gt;&gt;</span> Metallicity</p>
          <p><span>&gt;&gt;&gt;</span> Hydrogen</p>

          {/* {failedElements.map((element) => (
            <p key={element}>
              <span>&gt;&gt;&gt;</span> {element}
            </p>
          ))} */}

        </div>

      </div>

      <button className="bruh-btn">
        bruh
      </button>

    </div>
  );
}

export default MissionResult;
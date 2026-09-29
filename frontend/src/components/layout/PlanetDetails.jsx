import { useOutletContext, useNavigate } from "react-router-dom";
import "./PlanetDetails.css";

import earth from "../../assets/earth.png";

function PlanetDetails() {
  const { planet } = useOutletContext();
  const navigate = useNavigate();

  return (
    <div className="planet-details-page">

      <div className="planet-details-box">

        {/* Left side */}
        <div className="planet-info">

          <img
            src={earth}
            alt="Planet"
            className="details-planet-image"
          />

          <h2>
            Star ID: {planet.id}
          </h2>

          <p>
            Name: {planet.name}
          </p>

        </div>


        {/* Right side */}
        <div className="planet-description">

          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Aliquam semper tincidunt odio nec tempor. Etiam sodales
            magna eget sem suscipit accumsan. Aliquam placerat aliquet
            urna, vel iaculis tortor tincidunt a. Phasellus eget
            volutpat.
          </p>

          <p>
            In elementum mollis nibh fringilla aliquet. In eget
            venenatis lorem. Nulla eget blandit tellus. Aenean
            eleifend ante massa. Sed rhoncus quis risus sed dictum.
            Vestibulum id luctus turpis, vitae pretium arcu.
          </p>

          <p>
            Praesent eget molestie tellus. Etiam vel tellus semper
            lobortis purus in, placerat purus. Vestibulum consectetur
            blandit eros at vulputate.
          </p>

        </div>

      </div>


      {/* Buttons */}

      <div className="planet-details-buttons">

        <button
          onClick={() => navigate("/planetSelection")}
        >
          back to the menu
        </button>

        <button
          onClick={() => navigate("/mission")}
        >
          proceed to the planet
        </button>

      </div>

    </div>
  );
}

export default PlanetDetails;
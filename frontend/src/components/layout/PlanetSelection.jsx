import { useEffect, useState } from "react";
import { useOutletContext, useNavigate } from "react-router-dom";
import "./PlanetSelection.css";

import earth from "../../assets/earth.png";
import bluePlanet from "../../assets/bluePlanet.png";
import orangePlanet from "../../assets/orangePlanet.png";
import redPlanet from "../../assets/redPlanet.png";
import sunPlanet from "../../assets/sunPlanet.png";

function PlanetSelection() {
  const navigate = useNavigate();

  const { planet, setPlanet } = useOutletContext();

  const [planetList, setPlanetList] = useState([]);

  const planetImages = [
    earth,
    bluePlanet,
    orangePlanet,
    redPlanet,
    sunPlanet
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/planetSelection", {
          method: "GET"
        });

        if (!res.ok) {
          throw new Error(`HTTP error: ${res.status}`);
        }

        const data = await res.json();

        console.log("Planet list:", data);

        // Backend returns: [["KIC1", "KIC2", ...]]
        setPlanetList(data[0]);

      } catch (error) {
        console.error("Error fetching planets:", error);
      }
    };

    fetchData();
  }, []);

  const handleProceed = () => {
    if (!planet) return;

    console.log("Selected planet:", planet);

    navigate("/planetDetails");
  };

  return (
    <div className="planet-selection-page">

      <div className="planet-grid">

        {planetList.map((id, index) => {

          const isSelected = planet?.id === id;

          return (
            <div
              key={id}
              className={`planet-card ${isSelected ? "selected" : ""}`}
              onClick={() =>
                setPlanet({
                  id: id,
                  name: `Kepler-${id}b`,
                  image: planetImages[index % planetImages.length],
                  story: "",
                  element: {}
                })
              }
            >

              <img
                src={planetImages[index % planetImages.length]}
                alt={`Planet ${id}`}
                className="planet-image"
              />

              <p className="planet-id">
                Star ID: {id}
              </p>

              <p className="planet-name">
                Name: Kepler-{id}b
              </p>

            </div>
          );
        })}

      </div>

      <button
        className="proceed-btn"
        disabled={!planet}
        onClick={handleProceed}
      >
        proceed
      </button>

    </div>
  );
}

export default PlanetSelection;
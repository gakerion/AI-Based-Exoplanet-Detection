import { useOutletContext, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "./PlanetDetails.css";

function PlanetDetails() {
  const { planet, setPlanet } = useOutletContext();
  const navigate = useNavigate();

  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getPlanetDetails = async () => {
      if (!planet?.id) return;

      try {
        setLoading(true);

        const response = await fetch(
          `http://localhost:8000/planetDetails?id=${planet.id}`,
          {
            method: "POST",
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Planet details:", data);

        setDetails(data);

        // Save backend properties in shared planet object
        setPlanet(prev => ({
          ...prev,
          properties: data,
        }));

      } catch (error) {
        console.error("Error fetching planet details:", error);
      } finally {
        setLoading(false);
      }
    };

    getPlanetDetails();
  }, [planet?.id]);

  return (
    <div className="planet-details-page">

      <div className="planet-details-box">

        {/* Left side */}
        <div className="planet-info">

          <img
            src={planet.image}
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

          {loading ? (
            <p>Scanning planet...</p>
          ) : details ? (
            <>
            <p>{details.composition_text}</p>
              {/* <p>
                Oxygen: {details.Oxygen}
              </p>

              <p>
                Hydrogen: {details.Hydrogen}
              </p>

              <p>
                Metallicity: {details.Metallicity}
              </p>

              <p>
                Mass: {details.Mass}
              </p>

              <p>
                Gravity: {details.Gravity}
              </p>

              <p>
                Radius: {details.Radius}
              </p>

              <p>
                Distance: {details.Distance}
              </p> */}
            </>
          ) : (
            <p>Unable to retrieve planet data.</p>
          )}

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
          disabled={loading || !details}
        >
          proceed to the planet
        </button>

      </div>

    </div>
  );
}

export default PlanetDetails;
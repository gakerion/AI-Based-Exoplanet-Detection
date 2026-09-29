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
  const [planetList, setplanetList] = useState()
  const { planet, setPlanet } = useOutletContext();


  const planets = [
    {
      id: "K001",
      name: "Kepler-1b",
      image: earth
    },
    {
      id: "K002",
      name: "Kepler-2b",
      image: bluePlanet
    },
    {
      id: "K003",
      name: "Kepler-3b",
      image: orangePlanet
    },
    {
      id: "K004",
      name: "Kepler-4b",
      image: redPlanet
    },
    {
      id: "K005",
      name: "Kepler-5b",
      image: sunPlanet
    }
  ];

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch("/explore", {
        "method": "GET"
      })
      const data = await res.json()
      setplanetList(data)

    }

    fetchData()

  }, [])

  const handleProceed = async () => {
    if (!planet) return;

    console.log("Selected planet:", planet);
    setPlanet(planet)


    // const res = await fetch("/explore", {
    //   "method": "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   "body": JSON.stringify(planet.id)
    // })
    // const data = await res.json()
    // setplanetList(data)


    navigate("/planetDetails");
  };

  return (
    <div className="planet-selection-page">

      <div className="planet-grid">

        {planets.map((planet) => (
          <div
            key={planet.id}
            className={`planet-card ${planet?.id === planet.id
                ? "selected"
                : ""
              }`}
            onClick={() => setPlanet(planet)}
          >

            <img
              src={planet.image}
              alt={planet.name}
              className="planet-image"
            />

            <p className="planet-id">
              Star ID: {planet.id}
            </p>

            <p className="planet-name">
              Name: {planet.name}
            </p>

          </div>
        ))}

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
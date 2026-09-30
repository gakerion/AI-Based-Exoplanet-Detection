import "./HowToPlay.css";

function HowToPlay() {
  return (
    <div className="how-to-play-page">

      <div className="how-to-play-container">

        {/* Main Terminal Box */}
        <main className="how-to-play-card">

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            WELCOME, ASTRONAUT.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            You are stranded somewhere in the deep reaches of space.
            Your ship is running low on essential resources and you
            need to find them before it is too late.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            Five mysterious exoplanets have appeared on your navigation
            terminal. Your mission is simple: explore them, analyse
            their composition and collect the resources you need.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            STEP 01 — SELECT A PLANET
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            Choose one of the five planets displayed on your terminal.
            Every planet has different properties and resources.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            STEP 02 — SCAN THE PLANET
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            The system will analyse the planet and reveal information
            such as oxygen, hydrogen, metallicity, mass, radius,
            distance and gravity.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            STEP 03 — WATCH THE GRAVITY
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            Your spacecraft has a maximum acceleration limit.
            If the planet's gravity is greater than your maximum
            acceleration, your ship will not survive the landing.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            STEP 04 — COLLECT RESOURCES
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            If a planet contains one of the required elements,
            you can collect it. You need to explore different planets
            to complete your resource requirements.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            STEP 05 — COMPLETE THE MISSION
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            Collect all four required elements:
            OXYGEN, HYDROGEN, IRON and CARBON.
            Once all four are secured, the mission is complete.
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            REMEMBER:
          </div>

          <div className="how-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            Resources are limited. Gravity can kill you.
            Choose your planets carefully.
          </div>

          <div className="how-line how-bold">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            GOOD LUCK, ASTRONAUT.
          </div>

          <div className="how-line how-bold">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            YOUR MISSION STARTS NOW.
          </div>

        </main>


        {/* DEDSEC Logo */}
        <div className="how-logo-container">
          <img
            src="/logo.png"
            alt="DEDSEC Logo"
            className="how-dedsec-logo"
          />
        </div>


        {/* Footer Card */}
        <footer className="how-footer-card">

          <div className="how-footer-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            YOU ARE ON DEDSEC PROPERTY
          </div>

          <div className="how-footer-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            For more information contact:{" "}
            <a href="mailto:mohammed_b261522mt@nitc.ac.in">
              mohammed_b261522mt@nitc.ac.in
            </a>
          </div>

          <div className="how-footer-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:darshan_d260449ma@nitc.ac.in">
              darshan_d260449ma@nitc.ac.in
            </a>
          </div>

          <div className="how-footer-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:chetan_b260436ec@nitc.ac.in">
              chetan_b260436ec@nitc.ac.in
            </a>
          </div>

          <div className="how-footer-line">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:akshal_b260226ee@nitc.ac.in">
              akshal_b260226ee@nitc.ac.in
            </a>
          </div>

          <div className="how-footer-line how-colored">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            COPYRIGHT © 2026 | ALL RIGHTS RESERVED | REFRAIN FROM bs
          </div>

          <div className="how-footer-line how-colored">
            <span className="how-arrow">&gt;&gt;&gt;</span>
            lawyers and docs are banned for life :|.
          </div>

        </footer>

      </div>

    </div>
  );
}

export default HowToPlay;
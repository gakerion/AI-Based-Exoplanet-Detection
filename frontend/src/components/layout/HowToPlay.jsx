import "./HowToPlay.css";

import logo from "../../assets/dedsec.png";

function HowToPlay() {
  return (
    <div className="how-to-play-page">

      <div className="how-to-play-container">

        {/* Main Message Card */}
        <main className="terminal-card">

          <div className="prompt">
            &gt;&gt;&gt; Good morning, Boss.
            <br />
            <br />

            <div className="terminal-body">

              <p>
                I am pleased to inform you that you survived the jump, though
                my diagnostics suggest celebrating just yet would be premature.
                Main power is offline, and reserve life support is draining
                rapidly—your remaining supply of{" "}
                <span className="highlight">
                  oxygen, overall ship hull strength, and thruster fuel
                </span>{" "}
                gives us a very narrow survival window. I have scanned our
                immediate sector and isolated five candidate star systems using
                their{" "}
                <span className="highlight">
                  Kepler Input Catalog (KIC)
                </span>{" "}
                designations. Our mission is straightforward: locate an
                exoplanet with the right environmental conditions before your
                life support reads zero.
              </p>

              <p>
                To proceed, select a target KIC ID from your console so I can
                initiate a high-resolution spectroscopic scan. If an exoplanet
                is detected, I will immediately analyze its elemental
                composition for vital resources. If a single planet lacks
                everything you need to sustain life, you will need to plan a
                multi-system route—carefully calculating your fuel burn and
                transit time to harvest missing components across multiple
                worlds. Miscalculate your trajectory to a wrong exoplanet,
                ignore the sensor data, or simply hesitate too long, and I'm
                afraid life support will cease permanently.
              </p>

              <p>
                Whenever you are ready, Captain.
              </p>

            </div>
          </div>

          <div className="prompt-end">
            &gt;&gt;&gt;
          </div>

        </main>


        {/* DEDSEC Logo */}
        <div className="logo-container">
          <img
            src={logo}
            alt="DEDSEC Logo"
            className="dedsec-logo"
          />
        </div>


        {/* Footer Card */}
        <footer className="footer-card">

          <div className="line">
            <span className="arrow">&gt;&gt;&gt;</span>
            YOU ARE ON DEDSEC PROPERTY
          </div>

          <div className="line">
            <span className="arrow">&gt;&gt;&gt;</span>
            For more information contact:{" "}
            <a href="mailto:mohammed_b261522mt@nitc.ac.in">
              mohammed_b261522mt@nitc.ac.in
            </a>
          </div>

          <div className="line">
            <span className="arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:darshan_d260449ma@nitc.ac.in">
              darshan_d260449ma@nitc.ac.in
            </a>
          </div>

          <div className="line">
            <span className="arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:chetan_b260436ec@nitc.ac.in">
              chetan_b260436ec@nitc.ac.in
            </a>
          </div>

          <div
            className="line"
            style={{ color: "#A6FFFB" }}
          >
            <span className="arrow">&gt;&gt;&gt;</span>
            COPYRIGHT © 2026 | ALL RIGHTS RESERVED | REFRAIN FROM bs
          </div>

          <div
            className="line"
            style={{ color: "#A6FFFB" }}
          >
            <span className="arrow">&gt;&gt;&gt;</span>
            lawyers and docs are banned for life :|.
          </div>

        </footer>

      </div>

    </div>
  );
}

export default HowToPlay;
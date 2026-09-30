import "./AboutUs.css";

import logo from "../../assets/logo.png";

function AboutUs() {
  return (
    <div className="about-page">

      <div className="about-container">

        {/* Main Terminal Box */}
        <main className="terminal-card">

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            Hi, This is FAREED.
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            I will be introducing you to all the 4 idiots in this room
            who have come up with this earth shattering, uhm, excuse me,
            exoplanet shattering idea.
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            First and foremost, the team leader, our beloved PRC boy.
            Name is AKSHAL and by all measures of science, the most idiot
            among us. He is from EEE dept. and from HOSTEL B. He spends
            his free time sleeping though he says he doesn't have any
            free time.
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            Secondly and the second most, the guy who knows a guy or a
            thing or two. He is from ECE dept and was named Chetan a few
            years back. And is studying biology though neither him nor
            any of us know why. He spends his free time doom scrolling.
            Ouch, too honest?
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            Thirdly, the most disciplined and the only one from C Hostel
            among us, (for all 3 year olds, yes, among us mentioned] and
            is christened Darshan. Doing the back end of front end and
            front end of back end, he is the guy you call at 2 AM if your
            game play is broken. His number is X, [he removed it before
            publishing].
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            And there is me, Fareed. The most sane and comprehensible
            person among the one. And by now, you must know a lot about me.
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
          </div>

          <div className="terminal-line">
            <span className="arrow">&gt;&gt;&gt;</span>
          </div>

          <div className="terminal-line bold-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            Signing OFF,
          </div>

          <div className="terminal-line bold-line">
            <span className="arrow">&gt;&gt;&gt;</span>
            FAREED
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

          <div className="line">
            <span className="arrow">&gt;&gt;&gt;</span>
            or:{" "}
            <a href="mailto:akshal_b260226ee@nitc.ac.in">
              akshal_b260226ee@nitc.ac.in
            </a>
          </div>

          <div className="line colored">
            <span className="arrow">&gt;&gt;&gt;</span>
            COPYRIGHT © 2026 | ALL RIGHTS RESERVED | REFRAIN FROM bs
          </div>

          <div className="line colored">
            <span className="arrow">&gt;&gt;&gt;</span>
            lawyers and docs are banned for life :|.
          </div>

        </footer>

      </div>

    </div>
  );
}

export default AboutUs;
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import './App.css';

import Home from './components/layout/Home';
import Explore from './components/layout/Explore';
import AppLayout from './components/AppLayout';

import MissionIntro from './components/layout/MissionIntro';
import PlanetSelection from './components/layout/PlanetSelection';
import PlanetDetails from './components/layout/PlanetDetails';
import Mission from './components/layout/Mission';
import MissionResult from './components/layout/MissionResult';
import MissionSuccess from './components/layout/MissionSuccess';

import HowToPlay from './components/layout/HowToPlay';
import AboutUs from './components/layout/AboutUs';


const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,

    children: [

      // Home
      {
        path: "/",
        element: <Home />
      },

      // Explore
      {
        path: "/explore",
        element: <Explore />
      },

      // How To Play
      {
        path: "/howToPlay",
        element: <HowToPlay />
      },

      // About Us
      {
        path: "/aboutUs",
        element: <AboutUs />
      },

      // Mission Intro
      {
        path: "/missionIntro",
        element: <MissionIntro />
      },

      // Planet Selection
      {
        path: "/planetSelection",
        element: <PlanetSelection />
      },

      // Planet Details
      {
        path: "/planetDetails",
        element: <PlanetDetails />
      },

      // Mission
      {
        path: "/mission",
        element: <Mission />
      },

      // Mission Result
      {
        path: "/missionResult",
        element: <MissionResult />
      },

      // Mission Success
      {
        path: "/missionSuccess",
        element: <MissionSuccess />
      }

    ]
  }
]);


function App() {
  return <RouterProvider router={router} />;
}

export default App;
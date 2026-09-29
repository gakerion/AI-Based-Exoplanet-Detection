import { useState } from 'react'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Howl } from "howler";
import './App.css'
import Home from './components/layout/Home';
import Explore from './components/layout/Explore';
import AppLayout from './components/AppLayout';
import MissionIntro from './components/layout/MissionIntro';
import PlanetSelection from './components/layout/PlanetSelection';
import PlanetDetails from './components/layout/PlanetDetails';
import Mission from './components/layout/Mission';
import MissionResult from './components/layout/MissionResult';
import MissionSuccess from './components/layout/MissionSuccess';

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    children:[
      {
    path:"/",
    element:<Home />
  },
  {
    path: "/explore",
    element: <Explore />,
  },
  {
    path:"/missionIntro",
    element: <MissionIntro />
  },
  {
    path:"/planetSelection",
    element: <PlanetSelection />
  },
  {
    path:"/planetDetails",
    element: <PlanetDetails />
  },
  {
    path:"/mission",
    element: <Mission />
  },
  {
    path:"/missionResult",
    element: <MissionResult />
  },
  {
    path:"/missionSuccess",
    element: <MissionSuccess />
  }
    ]
  }
]);



function App() {
  return <RouterProvider router={router} />;
}

export default App

import logo from './logo.svg';
import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react';
import { useState } from 'react';
import DirectQueries from './Components/DirectQueries';
import NaturalLanguageQuery from './Components/NaturalLanguageQuery';
import MapSection from './Components/MapSection';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Components/Home';
import AreaAnalysis from './Components/AreaAnalysis';
import PredictiveAnalysis from './Components/PredictiveAnalysis.jsx';
import RealTimeTracking from './Components/RealTimeTracking';
import Header from './Components/Header';
import PositionDetails from './Components/PositionDetails';
import './App.css';
import Positions from './Components/Positions.jsx';


function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/area-analysis" element={<AreaAnalysis />} />
        <Route path="/predictive-analysis" element={<PredictiveAnalysis />} />
        <Route path="/real-time-tracking" element={<RealTimeTracking />} />
        <Route path="/position-details/:positionId" element={<PositionDetails />} />
        <Route path="/location" element={<Positions />} />
      </Routes>
    </Router>
    // <div>
    //   <h1>Mongo Intel</h1>
    //   <DirectQueries />
    //   <NaturalLanguageQuery />
    //   <MapSection />

    //   {/*other Components will go here */}
    // </div>
  );
}

export default App;

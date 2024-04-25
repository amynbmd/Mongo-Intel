import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import "bootstrap/dist/css/bootstrap.min.css";
import { Map, GoogleApiWrapper } from "google-maps-react";

const PositionDetails = (props) => {
  const { positionId } = useParams(); // Get positionId from URL
  const [position, setPosition] = useState(null);
  const REACT_APP_GOOGLE_MAPS_API_KEY =
    "AIzaSyCIGZxobctejYKdVTWmmN6olmBP4ZGSXe0";
  const mapStyles = {
    width: "100%",
    height: "80%",
  };
  const baseURL = process.env.REACT_APP_DB_SERVER_URL;
  const positionAPI = `${baseURL}/positions/`;

  useEffect(() => {
    console.log("Fetching datat for position ID:", positionId);
    const fetchPosition = async () => {
      try {
        const response = await axios.get(`${positionAPI}${positionId}`); // Fetch position data from API
        setPosition(response.data);
        console.log("Fetched position data:", response.data);
      } catch (error) {
        console.error("Error fetching position data", error);
        if (error.repsponse) {
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          console.log(error.request);
        } else {
          console.log("Error", error.mesage);
        }
      }
    };

    if (positionId) {
      fetchPosition();
    }
  }, [positionId]);
  const lat = position?.location?.coordinates?.[0];
  const lng = position?.location?.coordinates?.[1];

  const isPositionLoaded = lat != null && lng != null;
  return (
    <div className="container mt-4">
      {isPositionLoaded ? (
        <div>
          <h2 className="mb-3">Position Details</h2>
          <p>
            <strong>Name: </strong> {position.name}
          </p>
          <p>
            <strong>Description: </strong>
            {position.description}
          </p>
          <p>
            <strong>Latitude: </strong>
            {position.location.coordinates[0]}
          </p>
          <p>
            <strong>Longtitude: </strong>
            {position.location.coordinates[1]}
          </p>
          <p>
            <strong>Timestamp: </strong>
            {position.timestamp}
          </p>

          <Map
            google={props.google}
            zoom={14}
            style={mapStyles}
            initialCenter={{ lat: lat, lng: lng }}
          >
            <Marker position={{ lat: lat, lng: lng }} title={position.name} />
          </Map>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};
export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
})(PositionDetails);

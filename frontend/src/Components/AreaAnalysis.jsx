import React, { useState } from "react";
import axios from "axios";
import { TextareaAutosize as BaseTextareaAutosize } from "@mui/base/TextareaAutosize";
import { styled } from "@mui/system";
import { Button, FormControl, TextField, IconButton } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { Map, GoogleApiWrapper, Marker, Circle } from "google-maps-react";

function AreaAnalysis(props) {
  const baseURL = process.env.REACT_APP_BACKEND_URL;
  const nlpAPI = `${baseURL}/nlp`;

  const [formData, setFormData] = useState({
    query: null,
  });

  const mapStyles = {
    width: "100%",
    height: "80%",
  };

  let [positions, setPositions] = useState([]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.query != null && formData.query.trim() != "") {
      try {
        const response = await axios.get(`${nlpAPI}?text=${formData.query}`);

        if (response && response.data) {
          setPositions(response.data);
        }
      } catch (error) {
        console.error("Error submitting form", error);
      }
    }
  };

  const SearchButton = () => (
    <IconButton onClick={handleSubmit}>
      <SearchIcon />
    </IconButton>
  );

  return (
    <div style={{ paddingTop: "30px", margin: "auto" }}>
      <form
        style={{ paddingBottom: "30px", margin: "auto" }}
        onSubmit={handleSubmit}
        className="nlp-query-form"
      >
        <div style={{ maxWidth: "70%", margin: "auto" }}>
          <TextField
            onChange={handleChange}
            name="query"
            id="outlined-basic"
            variant="outlined"
            placeholder="Ask Mongo-Intel..."
            style={{ width: "100%" }}
            InputProps={{ endAdornment: <SearchButton /> }}
          />
        </div>
      </form>

      {positions && positions.length > 0 && (
        <Map
          google={props.google}
          zoom={11}
          style={mapStyles}
          initialCenter={{ lat: 38.8462, lng: -77.30637 }} // Default center is fairfax city
        >
          {positions.map((position) => {
            return (
              <Marker
                key={position._id}
                position={{
                  lat: position.location.coordinates[1],
                  lng: position.location.coordinates[0],
                }}
                title={
                  "Name: " +
                  position.name +
                  "\n" +
                  "Description: " +
                  position.description +
                  "\n" +
                  "Datetime: " +
                  position.timestamp +
                  "\n" +
                  "Longtitude: " +
                  position.location.coordinates[0] +
                  "\n" +
                  "Latitude: " +
                  position.location.coordinates[1] +
                  "\n" +
                  "Heading: " +
                  position.heading +
                  "\n" +
                  "Speed: " +
                  position.speed +
                  " km/h"
                }
              />
            );
          })}

          {positions.map((position) => {
            return (
              <Circle
                radius={2000}
                center={{
                  lat: position.location.coordinates[1],
                  lng: position.location.coordinates[0],
                }}
                // onMouseover={() => console.log('mouseover')}
                // onClick={() => console.log('click')}
                // onMouseout={() => console.log('mouseout')}
                strokeColor="transparent"
                strokeOpacity={0}
                strokeWeight={5}
                fillColor="#FF0000"
                fillOpacity={0.2}
              />
            );
          })}
        </Map>
      )}
    </div>
  );
}

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
})(AreaAnalysis);

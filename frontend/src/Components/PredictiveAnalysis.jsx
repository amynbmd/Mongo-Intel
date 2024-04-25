import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { Map, GoogleApiWrapper, Marker, Circle } from "google-maps-react";
import { useNavigate } from "react-router-dom";
import {
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
} from "@mui/material";
import InputLabel from "@mui/material/InputLabel";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormLabel from "@mui/material/FormLabel";

const PredictiveAnalysis = (props) => {
  const baseURL = process.env.REACT_APP_BACKEND_URL;
  const predictiveAPI = `${baseURL}/direct`;
  const predictiveTimeAPI = `${baseURL}/time`;

  const mapStyles = {
    width: "100%",
    height: "80%",
  };
  const options = [
    {
      label: "Name",
      value: 1,
    },
    {
      label: "Location",
      value: 2,
    },
    {
      label: "Timestamp",
      value: 3,
    },
  ];

  const [formData, setFormData] = useState({
    selectedOption: 0,
    name: "",
    description: "",
    lowerCoordinates: ["", ""], // Latitude and Longitude as an array
    upperCoordinates: ["", ""],
    timestamp: "",
    beforeOrAfter: "",
  });

  let [positions, setPositions] = useState([]);

  const handleChange = (e) => {
    if (
      e.target.name.includes("Latitude") ||
      e.target.name.includes("Longitude")
    ) {
      // Update coordinates array
      if (e.target.name.includes("lower")) {
        const newCoordinates = [...formData.lowerCoordinates];
        newCoordinates[e.target.name === "lowerLatitude" ? 0 : 1] =
          e.target.value;
        setFormData({ ...formData, lowerCoordinates: newCoordinates });
      } else {
        const newCoordinates = [...formData.upperCoordinates];
        newCoordinates[e.target.name === "upperLatitude" ? 0 : 1] =
          e.target.value;
        setFormData({ ...formData, upperCoordinates: newCoordinates });
      }
    } else {
      // Update other fields
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      let query = "";

      if (formData.selectedOption === 3) {
        // example name URL: http://localhost:8000/time?time=2023-10-15 10:00:00&before=true

        query =
          predictiveTimeAPI +
          `?time=${formData.timestamp}&before=${
            formData.beforeOrAfter == "before" ? true : false
          }`;
      } else {
        // example name URL: http://localhost:8000/direct?query={"name":"GMU"}
        // example location URL: http://localhost:8000/direct?query={"location":{"$geoWithin":{"$box":[[38.83178661625045,-77.31172257261196],[-60,50]]}}}
        query = predictiveAPI + "?query=";

        if (formData.selectedOption === 1) {
          const nameQuery = { name: formData.name };
          query += JSON.stringify(nameQuery);
        } else if (formData.selectedOption === 2) {
          query += `{"location":{"$geoWithin":{"$box":[[${formData.lowerCoordinates[0]},${formData.lowerCoordinates[1]}],[${formData.upperCoordinates[0]},${formData.upperCoordinates[1]}]]}}}`;
        }
      }

      const response = await axios.get(query);
      if (response && response.data) {
        setPositions(response.data);
      }
    } catch (error) {
      console.error("Error submitting form", error);
    }
  };

  return (
    <div>
      <div style={{ paddingTop: "30px", margin: "auto" }}>
        <form onSubmit={handleSubmit} className="area-analysis-form">
          <div style={{ maxWidth: "200px", margin: "auto" }}>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">
                Prediction Type
              </InputLabel>
              <Select
                labelId="demo-simple-select-label"
                name="selectedOption"
                value={formData.selectedOption}
                label="Prediction Type"
                onChange={handleChange}
              >
                {options.map((e) => {
                  return (
                    <MenuItem key={e.value} value={e.value}>
                      {e.label}
                    </MenuItem>
                  );
                })}
              </Select>
            </FormControl>
          </div>

          {formData.selectedOption === 1 ? (
            <div>
              <TextField
                size="small"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Name"
              />
            </div>
          ) : (
            ""
          )}
          {formData.selectedOption === 2 ? (
            <div>
              <span className="location-label">Lower: </span>
              <TextField
                size="small"
                name="lowerLatitude"
                type="number"
                value={formData.lowerCoordinates[0]}
                onChange={handleChange}
                placeholder="Latitude"
              />
              {"\u00A0"}
              <TextField
                size="small"
                name="lowerLongitude"
                type="number"
                value={formData.lowerCoordinates[1]}
                onChange={handleChange}
                placeholder="Longitude"
              />
            </div>
          ) : (
            ""
          )}
          {formData.selectedOption === 2 ? (
            <div>
              <span className="location-label">Upper: </span>
              <TextField
                size="small"
                name="upperLatitude"
                type="number"
                value={formData.upperCoordinates[0]}
                onChange={handleChange}
                placeholder="Latitude"
              />
              {"\u00A0"}
              <TextField
                size="small"
                name="upperLongitude"
                type="number"
                value={formData.upperCoordinates[1]}
                onChange={handleChange}
                placeholder="Longitude"
              />
            </div>
          ) : (
            ""
          )}
          {formData.selectedOption === 3 ? (
            <div>
              <FormControl>
                <RadioGroup
                  aria-labelledby="beforeOrAfter"
                  name="beforeOrAfter"
                  onChange={handleChange}
                  row
                >
                  <FormControlLabel
                    value="before"
                    control={<Radio />}
                    label="Before"
                  />
                  <FormControlLabel
                    value="after"
                    control={<Radio />}
                    label="After"
                  />
                </RadioGroup>
              </FormControl>
              <TextField
                size="small"
                name="timestamp"
                type="datetime-local"
                value={formData.timestamp}
                onChange={handleChange}
              />
            </div>
          ) : (
            ""
          )}

          <FormControl>
            <Button
              variant="contained"
              type="submit"
              size="large"
              disabled={formData.selectedOption < 0}
            >
              Find
            </Button>
          </FormControl>
        </form>
      </div>

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
};

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
})(PredictiveAnalysis);

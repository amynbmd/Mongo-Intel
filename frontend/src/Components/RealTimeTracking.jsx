import React, { useState } from "react";
import axios from "axios";
import { TextField, IconButton, colors } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";

const RealTimeTracking = (props) => {
  const baseURL = process.env.REACT_APP_BACKEND_URL;
  const nlpAPI = `${baseURL}/nlp`;
  const ollamaUrl = process.env.REACT_APP_OLLAMA_URL + "/api/generate";
  const geminiUrl =
    process.env.REACT_APP_GEMINI_URL + process.env.REACT_APP_GEMINI_API_KEY;

  let [loading, setLoading] = useState(false);
  let [ollamaResponse, setOllamaResponse] = useState(null);
  const [formData, setFormData] = useState({
    query: null,
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setOllamaResponse(null);

    if (formData.query != null && formData.query.trim() != "") {
      try {
        const response = await axios.get(`${nlpAPI}?text=${formData.query}`);

        if (response && response.data) {
          console.log(response);

          // callOllama(response.data);
          callGemini(response.data);
        }
      } catch (error) {
        console.error("Error submitting form", error);
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  };

  const SearchButton = () => (
    <IconButton onClick={handleSubmit} disabled={loading}>
      <SearchIcon />
    </IconButton>
  );

  async function callGemini(data) {
    const body = {
      contents: [
        {
          parts: [
            {
              text:
                "Provide a brief answer for the following question when given the JSON data, " +
                formData.query.trim() +
                "? JSON Data: " +
                JSON.stringify(data),
            },
          ],
        },
      ],
    };

    try {
      const response = await axios.post(geminiUrl, body);
      var responseText = response.data.candidates[0].content.parts[0].text;
      setOllamaResponse(responseText);
    } catch (ex) {
      setOllamaResponse(ex.message + ". Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function callOllama(data) {
    const body = {
      model: "mistral",
      prompt:
        "Provide a brief answer for the following question when given the JSON data, " +
        formData.query.trim() +
        "? JSON Data: " +
        JSON.stringify(data),
      stream: false,
    };

    try {
      const response = await axios.post(ollamaUrl, body);
      setOllamaResponse(response.data.response);
    } catch (ex) {
      setOllamaResponse(ex.message + ". Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        paddingTop: "30px",
        margin: "auto",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <div style={{ flex: "1", borderRight: "10px solid black" }}>
        <img
          src="https://thumbs.dreamstime.com/b/robot-icon-chat-bot-sign-support-service-concept-chatbot-character-flat-style-robot-icon-chat-bot-sign-support-service-138271515.jpg"
          alt="Your Image"
          style={{ height: "auto" }}
        />
      </div>
      <div style={{ flex: "2" }}>
        <form onSubmit={handleSubmit} className="nlp-query-form">
          <div style={{ maxWidth: "70%", margin: "auto" }}>
            <TextField
              onChange={handleChange}
              name="query"
              id="outlined-basic"
              variant="outlined"
              placeholder="Message Chatbot..."
              style={{ width: "100%" }}
              InputProps={{ endAdornment: <SearchButton /> }}
            />
          </div>
        </form>

        {loading ? (
          <div style={{ paddingTop: "20px" }}>
            <Box
              style={{
                margin: "auto",
                width: "100%",
                justifyContent: "center",
                display: "flex",
              }}
            >
              <CircularProgress />
            </Box>
          </div>
        ) : (
          ""
        )}

        {ollamaResponse != null ? (
          <div style={{ maxWidth: "70%", margin: "auto", paddingTop: "30px" }}>
            <div
              style={{
                border: "3px solid green",
                padding: "5px",
                borderRadius: "5px",
              }}
            >
              {ollamaResponse}
            </div>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};
export default RealTimeTracking;

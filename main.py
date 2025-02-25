from fastapi import FastAPI
const axios = require("axios");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

const fetchFootballData = async () => {
  try {
    const response = await axios.get("https://api.football-data.co.uk/matches");
    return response.data;
  } catch (error) {
    console.error("Error fetching Football-Data API:", error);
    return [];
  }
};

const fetchOddsData = async () => {
  try {
    const response = await axios.get("https://api.the-odds-api.com/v4/sports/soccer/odds", {
      params: { apiKey: process.env.ODDS_API_KEY }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching OddsAPI data:", error);
    return [];
  }
};

const fetchSportMonksData = async () => {
  try {
    const response = await axios.get("https://api.sportmonks.com/v3/football/fixtures", {
      params: { api_token: process.env.SPORTMONKS_API_KEY }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching SportMonks API:", error);
    return [];
  }
};

const fetchAPIFootballData = async () => {
  try {
    const response = await axios.get("https://api.api-football.com/v3/fixtures", {
      headers: { "x-apisports-key": process.env.API_FOOTBALL_KEY }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching API-Football data:", error);
    return [];
  }
};

app.get("/api/matches", async (req, res) => {
  try {
    const [footballData, oddsData, sportMonksData, apiFootballData] = await Promise.all([
      fetchFootballData(),
      fetchOddsData(),
      fetchSportMonksData(),
      fetchAPIFootballData()
    ]);

    const combinedData = footballData.concat(oddsData, sportMonksData, apiFootballData).slice(0, 3);
    res.json(combinedData);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch match data" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

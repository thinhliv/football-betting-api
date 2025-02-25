const express = require("express");
const axios = require("axios");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());

// Hàm lấy dữ liệu từ Football-Data API
const fetchFootballData = async () => {
  try {
    const response = await axios.get("https://api.football-data.org/v4/matches", {
      headers: { "X-Auth-Token": process.env.FOOTBALL_DATA_API_KEY },
    });
    return response.data.matches || [];
  } catch (error) {
    console.error("❌ Error fetching Football-Data API:", error.response?.data || error.message);
    return [];
  }
};

// Hàm lấy dữ liệu từ The Odds API
const fetchOddsData = async () => {
  if (!process.env.ODDS_API_KEY) {
    console.error("⚠️ Missing ODDS_API_KEY in .env file!");
    return [];
  }
  try {
    const response = await axios.get("https://api.the-odds-api.com/v4/sports/soccer/odds", {
      params: { apiKey: process.env.ODDS_API_KEY },
    });
    return response.data || [];
  } catch (error) {
    console.error("❌ Error fetching OddsAPI data:", error.response?.data || error.message);
    return [];
  }
};

// Hàm lấy dữ liệu từ SportMonks API
const fetchSportMonksData = async () => {
  if (!process.env.SPORTMONKS_API_KEY) {
    console.error("⚠️ Missing SPORTMONKS_API_KEY in .env file!");
    return [];
  }
  try {
    const response = await axios.get("https://api.sportmonks.com/v3/football/fixtures", {
      params: { api_token: process.env.SPORTMONKS_API_KEY },
    });
    return response.data.data || [];
  } catch (error) {
    console.error("❌ Error fetching SportMonks API:", error.response?.data || error.message);
    return [];
  }
};

// Hàm lấy dữ liệu từ API-Football
const fetchAPIFootballData = async () => {
  if (!process.env.API_FOOTBALL_KEY) {
    console.error("⚠️ Missing API_FOOTBALL_KEY in .env file!");
    return [];
  }
  try {
    const response = await axios.get("https://v3.football.api-sports.io/fixtures", {
      headers: { "x-apisports-key": process.env.API_FOOTBALL_KEY },
    });
    return response.data.response || [];
  } catch (error) {
    console.error("❌ Error fetching API-Football data:", error.response?.data || error.message);
    return [];
  }
};

// Endpoint API lấy dữ liệu từ tất cả các nguồn
app.get("/api/matches", async (req, res) => {
  try {
    const [footballData, oddsData, sportMonksData, apiFootballData] = await Promise.all([
      fetchFootballData(),
      fetchOddsData(),
      fetchSportMonksData(),
      fetchAPIFootballData(),
    ]);

    const combinedData = [...footballData, ...oddsData, ...sportMonksData, ...apiFootballData].slice(0, 3);
    
    res.json({
      message: "Success",
      matches: combinedData,
    });
  } catch (error) {
    console.error("❌ Error fetching match data:", error.message);
    res.status(500).json({ error: "Failed to fetch match data" });
  }
});

// Khởi động server
app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});

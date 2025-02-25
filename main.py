import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table } from "@/components/ui/table";
import axios from "axios";

export default function BettingDashboard() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMatches();
  }, []);

  const fetchMatches = async () => {
    try {
      const response = await axios.get("/api/matches");
      setMatches(response.data);
    } catch (error) {
      console.error("Error fetching matches:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Betting Prediction Dashboard</h1>
      <Button onClick={fetchMatches} disabled={loading}>
        {loading ? "Updating..." : "Refresh Matches"}
      </Button>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        {matches.map((match, index) => (
          <Card key={index}>
            <CardContent>
              <h2 className="text-lg font-semibold">{match.teams}</h2>
              <p>Odds: {match.odds}</p>
              <p>Handicap: {match.handicap}</p>
              <p>Predicted Score: {match.prediction}</p>
              <p>Risk Management: {match.risk_assessment}</p>
              <p>Data Source: {match.data_source}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

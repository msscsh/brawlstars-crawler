const { log } = require("console");
const express = require("express");
const { google } = require("googleapis");

const { getPlayers } = require('../dist/management/lineup/app');

const app = express();
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/", async (req, res) => {
  // const { request, name } = req.body;

  const auth = new google.auth.GoogleAuth({
    keyFile: "src/commons/files/credentials.json",
    scopes: "https://www.googleapis.com/auth/spreadsheets",
  });

  // Create client instance for auth
  const client = await auth.getClient();

  // Instance of Google Sheets API
  const googleSheets = google.sheets({ version: "v4", auth: client });
  const spreadsheetId = "10bxlToXdOLsyl2wER2W1TcA9auYmPPqg00RPhIysiZk";

  const players = getPlayers();
  const lines = [];
  players.forEach(objeto => {
    const columns = [objeto.name, objeto.trophies];
    lines.push(columns);
  });

  // Write row(s) to spreadsheet
  await googleSheets.spreadsheets.values.append({
    auth,
    spreadsheetId,
    range: "Sheet1!A:B",
    valueInputOption: "USER_ENTERED",
    resource: {
      values: lines,
    },
  });

  res.send("Successfully submitted! Thank you!");
});

app.listen(1337, (req, res) => console.log("running on 1337"));
const { log } = require("console");
const express = require("express");
const { google } = require("googleapis");

const { transformTwoDimensionalArrayToListOfPlayers, valueAlreadyExistsInThis } = require('../dist/commons/functions/utils');
const { getDataInSheetArea, addLinesInSheet, getPlayers, clearPlayersLines } = require('../dist/commons/functions/googlespreadsheet-operations');

const app = express();
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

app.get("/", async (req, res) => {
  res.render("index");
});

  // const { request, name } = req.body;
  // const getLines = await getDataInSheetArea(googleSheets, auth);
  // const playersInSheet = transformTwoDimensionalArrayToListOfPlayers(getLines.data.values);
  // console.log(playersInSheet);
app.post("/", async (req, res) => {
  const { googleSheets, auth } = await prepareCredentials();
  await clearPlayersLines(googleSheets, auth);

  const playersInFile = getPlayers();
  console.log('playersInFile------------------------------------');
  console.log(playersInFile);

  const playerToAdd = [];
  playersInFile.forEach(player => {
    const columns = [player.tag, player.expLevel, player.name, player.trophies, `=HIPERLINK("https://brawlstats.com/profile/${player.tag.substring(1)}"; "${player.tag}")`, player['3vs3Victories'], player.highestTrophies, player.isQualifiedFromChampionshipChallenge];
    playerToAdd.push(columns);
  });

  console.log('playerToAdd---------------------------------------');
  console.log(playerToAdd);

  setTimeout(() => {
    addLinesInSheet(googleSheets, auth, playerToAdd);
  }, 10000);

  res.send("Data has been updated! Thank you!");
});

app.listen(1337, (req, res) => console.log("running on 1337"));

async function prepareCredentials() {
  const auth = new google.auth.GoogleAuth({
    keyFile: "src/commons/files/credentials.json",
    scopes: "https://www.googleapis.com/auth/spreadsheets",
  });
  const client = await auth.getClient();
  const googleSheets = google.sheets({ version: "v4", auth: client });
  return { googleSheets, auth };
}
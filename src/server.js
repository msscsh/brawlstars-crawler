const express = require("express");
const favicon = require('serve-favicon');
const path = require('path');
const { google } = require("googleapis");

const { getTeamFromPlayerTag } = require('../dist/commons/functions/utils');
const { createPersistentFileWithJSONContent, createFileWithJSONContent, readJSONInFile } = require('../dist/commons/functions/files');
const { addLinesInSheet, getPlayers, clearPlayersLines } = require('../dist/commons/functions/googlespreadsheet-operations');

const app = express();
app.use(favicon(path.join(__dirname, 'commons/files', 'favicon.ico')));
app.use(express.static(path.join(__dirname, 'commons/files')));
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

app.get("/", async (req, res) => {
  res.render("index");
});

  // const { request, name } = req.body;
  // const getLines = await getDataInSheetArea(googleSheets, auth);
  // const playersInSheet = transformTwoDimensionalArrayToListOfPlayers(getLines.data.values);
  // console.log(playersInSheet);
app.post("/spreadsheet-data", async (req, res) => {
  const { googleSheets, auth } = await prepareCredentials();
  await clearPlayersLines(googleSheets, auth);

  const playersInFile = getPlayers();
  console.log('playersInFile------------------------------------');
  console.log(playersInFile);

  const playerToAdd = [];
  playersInFile.forEach(player => {
    const columns = [player.tag, player.expLevel, player.name, player.trophies, `=HIPERLINK("https://brawlstats.com/profile/${player.tag.substring(1)}"; "${player.tag}")`, player['3vs3Victories'], player.highestTrophies, player.isQualifiedFromChampionshipChallenge, getTeamFromPlayerTag(player.tag)];
    playerToAdd.push(columns);
  });

  console.log('playerToAdd---------------------------------------');
  console.log(playerToAdd);

  setTimeout(() => {
    addLinesInSheet(googleSheets, auth, playerToAdd);
  }, 5000);

  res.send("Data has been updated! Thank you!");
});

//Route teams
app.get('/teams', (req, res) => {

  const clubPlayers = getPlayers();

  let teams = readJSONInFile('team_relation.json');

  if(!teams) {
    teams = [
      { name: 'Team 1', players: [] },
      { name: 'Team 2', players: [] },
      { name: 'Team 3', players: [] },
      { name: 'Team 4', players: [] },
      { name: 'Team 5', players: [] },
      { name: 'Team 6', players: [] },
      { name: 'Team 7', players: [] },
      { name: 'Team 8', players: [] },
      { name: 'Team 9', players: [] },
      { name: 'Team 10', players: [] },
    ];
  }

  const availablePlayers = createAvaiblePlayersList(clubPlayers, teams);
  removeOldClubPlayers(clubPlayers, teams);

  res.render('teams',  {clubPlayers, availablePlayers, teams});
});

function createAvaiblePlayersList(clubPlayers, teams) {
  const playersInTeam = teams.reduce((acc, team) => {
    return [...acc, ...team.players];
  }, []);

  return clubPlayers.filter((clubPlayer) => !playersInTeam.includes(clubPlayer.tag));
}

function removeOldClubPlayers(clubPlayers, teams) {
  teams.forEach((team) => {
    team.players = team.players.filter((tag) => {
      const associatedClubPlayer = clubPlayers.some((clubPlayer) => clubPlayer.tag === tag);
      return associatedClubPlayer;
    });
  });
}

app.post("/teams", (req, res) => {

  let body = '';

  req.on('data', (chunk) => {
    body += chunk;
  });

  req.on('end', () => {
    try {
      const { teams } = JSON.parse(body);
      console.log(teams);
      createFileWithJSONContent('team_relation.json', teams);
      createPersistentFileWithJSONContent('team_relation.json', teams);
    } catch (error) {
      console.error('BAD REQUEST:', error);
      res.statusCode = 400;
      res.end('BAD REQUEST: 400 ' + error);
    }
  });
  
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
const express = require("express");
const { google } = require("googleapis");

const { getTeamFromPlayerTag } = require('../dist/commons/functions/utils');
const { addLinesInSheet, getPlayers, clearPlayersLines } = require('../dist/commons/functions/googlespreadsheet-operations');

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
  const data = {
  };
  res.render('teams', data); // 'index' é o nome do arquivo EJS que contém a tela da organização de times
});

// Inicie o servidor
const PORT = 3000; // ou qualquer outra porta que desejar
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
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
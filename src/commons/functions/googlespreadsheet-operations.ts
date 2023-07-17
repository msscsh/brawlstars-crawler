import { PlayersData } from 'src/commons/types/players-data';
import { readJSONInFile } from '../../commons/functions/files';

import dotenv from 'dotenv';
dotenv.config();

const spreadsheetId = process.env.SPREADSHEETID || "10bxlToXdOLsyl2wER2W1TcA9auYmPPqg00RPhIysiZk";
console.log(`The spreadsheetId ${spreadsheetId}`);
const spreadsheetTargetPlayerData = process.env.SPREADSHEETTAB+'!'+process.env.PLAYERCELLS;
console.log(`The players cells location  ${spreadsheetTargetPlayerData}`);

export function getPlayers(): any {
    const data: PlayersData = readJSONInFile('master.json');
    return data.members;
}

export async function addLinesInSheet(googleSheets, auth, lines) {
  await googleSheets.spreadsheets.values.append({
    auth,
    spreadsheetId,
    range: spreadsheetTargetPlayerData,
    valueInputOption: "USER_ENTERED",
    resource: {
      values: lines,
    },
  });
}

export async function getDataInSheetArea(googleSheets, auth) {
  const getRows = await googleSheets.spreadsheets.values.get({
    auth,
    spreadsheetId,
    range: spreadsheetTargetPlayerData,
  });
  return getRows;
}

export async function clearPlayersLines(googleSheets, auth) {
  await googleSheets.spreadsheets.values.clear(
    {
      auth,
      spreadsheetId,
      range: process.env.SPREADSHEETTAB+'!'+'A2:ZZ',
    },
    (err, response) => {
      if (err) {
        console.error('Something is wrong i can feel it:', err);
        return;
      }
      console.log("It's all gone!");
    });
}
import { PlayersData } from "src/commons/types/players-data";
import { readJSONInFile } from "../../commons/functions/files";

import dotenv from "dotenv";
dotenv.config();

const spreadsheetId = process.env.SPREADSHEETID;
console.log(`The spreadsheetId ${spreadsheetId}`);
const spreadsheetTargetPlayersData =
	process.env.PLAYERSTAB + "!" + process.env.PLAYERSCELLS;
console.log(`The players cells location  ${spreadsheetTargetPlayersData}`);

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function getPlayers(): any {
	const data: PlayersData = readJSONInFile("master.json");
	return data.members;
}

export async function addLinesInSheet(googleSheets, auth, lines) {
	await googleSheets.spreadsheets.values.append({
		auth,
		spreadsheetId,
		range: spreadsheetTargetPlayersData,
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
		range: spreadsheetTargetPlayersData,
	});
	return getRows;
}

export async function clearPlayersLines(googleSheets, auth) {
	await googleSheets.spreadsheets.values.clear(
		{
			auth,
			spreadsheetId,
			range: spreadsheetTargetPlayersData,
		},
		(err, _response) => {
			if (err) {
				console.error("Something is wrong i can feel it:", err);
				return;
			}
			console.log("It's all gone!");
		},
	);
}

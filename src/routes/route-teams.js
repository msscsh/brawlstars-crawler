/* eslint-disable @typescript-eslint/no-var-requires */
const express = require("express");
const router = express.Router();

const {
	createPersistentFileWithJSONContent,
	createFileWithJSONContent,
	readJSONInFile,
} = require("../../dist/commons/functions/files");

const {
	getPlayers,
} = require("../../dist/commons/functions/googlespreadsheet-operations");

router.get("/", (_req, res) => {
	const clubPlayers = getPlayers();
	let teams = readJSONInFile("team_relation.json");

	if (!teams) {
		teams = [
			{ name: "Team 1", players: [] },
			{ name: "Team 2", players: [] },
			{ name: "Team 3", players: [] },
			{ name: "Team 4", players: [] },
			{ name: "Team 5", players: [] },
			{ name: "Team 6", players: [] },
			{ name: "Team 7", players: [] },
			{ name: "Team 8", players: [] },
			{ name: "Team 9", players: [] },
			{ name: "Team 10", players: [] },
		];
	}

	const availablePlayers = createAvaiblePlayersList(clubPlayers, teams);
	removeOldClubPlayers(clubPlayers, teams);
	res.render("teams", { clubPlayers, availablePlayers, teams });
});

function createAvaiblePlayersList(clubPlayers, teams) {
	const playersInTeam = teams.reduce((acc, team) => {
		return [...acc, ...team.players];
	}, []);
	return clubPlayers.filter(
		(clubPlayer) => !playersInTeam.includes(clubPlayer.tag),
	);
}

function removeOldClubPlayers(clubPlayers, teams) {
	teams.forEach((team) => {
		team.players = team.players.filter((tag) => {
			const associatedClubPlayer = clubPlayers.some(
				(clubPlayer) => clubPlayer.tag === tag,
			);
			return associatedClubPlayer;
		});
	});
}

router.post("/", (req, res) => {
	let body = "";

	req.on("data", (chunk) => {
		body += chunk;
	});

	req.on("end", () => {
		try {
			const { teams } = JSON.parse(body);
			console.log(teams);
			createFileWithJSONContent("team_relation.json", teams);
			createPersistentFileWithJSONContent("team_relation.json", teams);
		} catch (error) {
			console.error("BAD REQUEST:", error);
			res.statusCode = 400;
			res.end("BAD REQUEST: 400 " + error);
		}
	});
});

module.exports = router;

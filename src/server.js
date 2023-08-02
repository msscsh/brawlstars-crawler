/* eslint-disable @typescript-eslint/no-var-requires */
const express = require("express");
const favicon = require("serve-favicon");
const path = require("path");

const app = express();
app.use(favicon(path.join(__dirname, "commons/files", "favicon.ico")));
app.use(express.static(path.join(__dirname, "commons/files")));
app.set("view engine", "ejs");
app.use(express.urlencoded({ extended: true }));

const routeSpreadsheet = require("./routes/route-spreadsheet");
const routeTeams = require("./routes/route-teams");

app.use("/spreadsheet-data", routeSpreadsheet);
app.use("/teams", routeTeams);

app.get("/", async (req, res) => {
	res.render("index");
});

app.listen(1337, (_req, _res) => console.log("running on 1337"));

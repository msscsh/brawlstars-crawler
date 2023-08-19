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

let relationData = readJSONInFile('player_info_relation.json');

router.get('/', async (req, res) => {
	const masterData = getPlayers();
    res.render('players-info', { masterData, relationData });
});

router.post('/addAttribute', (req, res) => {

    const { tag, attributeName, attributeValue } = req.body;

    if (!relationData[tag]) {
      relationData[tag] = { attributes: {} };
    }
  
    relationData[tag].attributes[attributeName] = attributeValue;
    console.log(relationData);

    // Save merged data back to the file
    createFileWithJSONContent("player_info_relation.json", relationData);
    createPersistentFileWithJSONContent("player_info_relation.json", relationData);
  
    res.redirect('/');
});

module.exports = router;

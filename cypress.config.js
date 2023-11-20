const { defineConfig } = require('cypress');

module.exports = defineConfig({
	e2e: {
		hideXHRInCommandLog: true,
	},
	fixturesFolder: false,
	experimentalModifyObstructiveThirdPartyCode: true,
});
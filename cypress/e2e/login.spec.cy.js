const fs = require("fs");

describe("Generate API Key", () => {
	it("Generate API Key", () => {
		//Visit
		cy.visit("https://developer.brawlstars.com/#/login");
		cy.wait(4000);

		//Coockies settings
		// cy.get('#onetrust-accept-btn-handler').click()

		//Login
		cy.get("#email").type(Cypress.env("BS_EMAIL"));
		cy.get("#password").type(Cypress.env("BS_PASSWORD"));
		cy.contains("button", "Log In").click();

		//Navigation to Form
		cy.contains("button", "Bruno").click();
		cy.wait(1000);
		cy.contains("a", "My Account").click({ force: true });

		//Delete
		cy.wait(2000);
		cy.contains("h4", "IP TODAY").click();
		cy.wait(2000);
		cy.contains("span", "Delete Key").click();

		//Create
		cy.wait(2000);
		cy.contains("span", "Create New Key").click();
		cy.get("#name").type("IP TODAY");
		cy.get("#description").type("Ip today");
		cy.get("#range-0").type(Cypress.env("EXTERNAL_IP"));
		cy.contains("span", "Create Key").click();
		cy.wait(2000);

		//Detail
		cy.contains("h4", "IP TODAY").click();
		cy.get("samp")
			.invoke("text")
			.then((text) => {
				cy.writeFile("shell.json", `{"BSAPIKEY":"${text}"}`);
			});
	});
});

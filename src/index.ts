import BrawlStarsAPICaller from "brawlstars-api-sdk";

const client = new BrawlStarsAPICaller({
	apiKey: "AAAA",
});

client.getPlayer("#2QPVJ099C").then((player) => {
	console.log(player);
});

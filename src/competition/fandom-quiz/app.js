var fs = require('fs');
function main() {
    var rawData = fs.readFileSync('informacoes.json', 'utf8');
    var data = JSON.parse(rawData);
    var brawlers = data.brawlers;
    var question = generateRandomQuestion(brawlers);
    console.log('Tipo de Pergunta:', question.type);
    console.log('Pergunta:', question.question);
    var shuffledOptions = question.options.sort(function () { return 0.5 - Math.random(); });
    var incorrectAnswer = getRandomOption(brawlers
        .filter(function (brawler) { return brawler.name !== question.answer; })
        .map(function (brawler) { return brawler.name; }));
    shuffledOptions.splice(1, 0, incorrectAnswer);
    console.log('Opções:', shuffledOptions);
    console.log('Resposta:', question.answer);
}
main();
function generateRandomQuestion(brawlers) {
    var randomType = Math.random() < 0.5 ? 'attribute' : 'directInfo';
    if (randomType === 'attribute') {
        return generateAttributeQuestion(brawlers);
    }
    else {
        return generateDirectInfoQuestion(brawlers);
    }
}
function getRandomOption(options) {
    var randomIndex = Math.floor(Math.random() * options.length);
    return options[randomIndex];
}
function generateAttributeQuestion(brawlers) {
    var attributes = getBrawlerAttributes(brawlers[0]);
    var attribute = getRandomOption(attributes);
    var selectedBrawlers = getRandomBrawlers(brawlers, 2);
    var question = "Qual brawler possui ".concat(attribute, " maior?");
    var options = selectedBrawlers.map(function (brawler) { return brawler.name; });
    var answer = selectedBrawlers.reduce(function (a, b) { return (a[attribute] > b[attribute] ? a : b); }).name;
    return {
        type: 'Perguntas de cruzamento de informação de atributos do brawler',
        question: question,
        options: options,
        answer: answer,
    };
}
function getBrawlerAttributes(brawler) {
    return Object.keys(brawler);
}
function generateDirectInfoQuestion(brawlers) {
    var selectedBrawlers = getRandomBrawlers(brawlers, 1);
    var brawler = selectedBrawlers[0];
    var question = "Qual \u00E9 a habilidade Super do brawler ".concat(brawler.name, "?");
    var options = [brawler.super];
    var answer = brawler.super;
    return {
        type: 'Perguntas de informação direta do brawler',
        question: question,
        options: options,
        answer: answer,
    };
}
function getRandomBrawlers(brawlers, count) {
    var shuffled = brawlers.sort(function () { return 0.5 - Math.random(); });
    return shuffled.slice(0, count);
}

import fs from 'fs';
import path from 'path';

interface Brawler {
  nome: string;
  vida: number;
  ataque: number;
  velocidade: string;
  super: string;
}

interface Question {
  type: string;
  question: string;
  options: string[];
  answer: Brawler;
  attribute: string
}

//Leitura do arquivo
const pasta = '';
const nomeArquivo = 'informacoes.json';
const caminhoArquivo = path.join(__dirname, pasta, nomeArquivo);

//conversão para objeto
const rawData = fs.readFileSync(caminhoArquivo, 'utf8');
const brawlers: Brawler[] = JSON.parse(rawData).brawlers;

//Lista de valores para super
const valoresAtributosSuper = [];
for (const brawler of brawlers) {
  const valor = brawler['super'];
  valoresAtributosSuper.push(valor);
}

//lista de atributos válidos para perguntas
const brawlersValidAttributesList = getBrawlerAttributes(brawlers[0])
                    .filter(item => (item !== 'nome') && (item !== 'super') );

const brawlersDirectValuesList = getBrawlerAttributes(brawlers[0])
                    .filter(item => item === 'super');


// Variáveis globais para controlar as combinações já utilizadas
let usedBrawlerGroups: Brawler[] = [];
let usedQuestionTypes: string[] = [];
let usedAttributes: string[] = [];

const questions: Question[] = [];
function main() {
    const numQuestions = 5; // Número de perguntas desejado
    
  
    for (let i = 0; i < numQuestions; i++) {
      const question = generateUniqueQuestion();
      questions.push(question);
    }
  
    // Iterar sobre a lista de perguntas
    for (const question of questions) {
      console.log('Tipo de Pergunta:', question.type);
      console.log('Atributo alvo da pergunta:', question.attribute);
      console.log('Pergunta:', question.question);
      console.log('Opções:', question.options);
      console.log('Resposta:', question.answer);
      console.log('----------------------');
    }
}

main();

function generateUniqueQuestion(): Question {
    let question: Question;

    do {
        question = generateRandomQuestion();
    }
    while (isCombinationUsed(question.answer, question.type, question.attribute));

    markCombinationAsUsed(question.answer, question.type, question.attribute);

    return question;
}
  
function isCombinationUsed(selectedBrawler: Brawler, type: string, attribute: string): boolean {
    const hasUsedBrawlerGroup = usedBrawlerGroups.includes(selectedBrawler);  
    const hasUsedQuestionType = usedQuestionTypes.includes(type);
    const hasUsedAttribute = usedAttributes.includes(attribute);

    console.log(selectedBrawler + ' = ' + hasUsedBrawlerGroup );
    console.log(type + ' = ' + hasUsedQuestionType);
    console.log(attribute + ' = ' + hasUsedAttribute );

    console.log(questions)

    return hasUsedBrawlerGroup;
}
  
function markCombinationAsUsed(selectedBrawler: Brawler, type: string, attribute: string) {
    usedBrawlerGroups.push(selectedBrawler);
    usedQuestionTypes.push(type);
    usedAttributes.push(attribute);
}

function generateRandomQuestion(): Question {
    const randomType = Math.random() < 0.5 ? 'attribute' : 'directInfo';

    if (randomType === 'attribute') {
        return generateAttributeQuestion(getRandomOption(brawlersValidAttributesList));
    }
    else {
        return generateDirectInfoQuestion(getRandomOption(brawlersDirectValuesList));
    }
}

function getRandomOption(options: string[]): string {
  const randomIndex = Math.floor(Math.random() * options.length);
  return options[randomIndex];
}

function generateAttributeQuestion(attribute): Question {

  const selectedBrawlers = gerarListaDeBrawlersComBrawlerAlvo();

  const question = `Qual brawler possui maior ${attribute}?`;
  const answer = selectedBrawlers.reduce((a, b) => (a[attribute] > b[attribute] ? a : b)).nome;
  const options = gerarOpcoesComValoresDosAtributosDosBrawlers(selectedBrawlers, 'nome');

  return {
    type: 'Perguntas de cruzamento de informação de atributos do brawler',
    question,
    options,
    answer,
    attribute
  };
}

function getBrawlerAttributes(brawler: Brawler): string[] {
  return Object.keys(brawler);
}

function generateDirectInfoQuestion(attribute): Question {
  const selectedBrawlers = gerarListaDeBrawlersComBrawlerAlvo();
  const brawler = selectedBrawlers[0];
  const question = `Qual é a habilidade Super do brawler ${brawler.nome}?`;
  const options = gerarOpcoesComValoresDosAtributosDosBrawlers(selectedBrawlers, attribute);
  const answer = brawler.super;

  return {
    type: 'Perguntas de informação direta do brawler',
    question,
    options,
    answer,
    attribute
  };
}

function shuffle(array: any[]) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function gerarOpcoesComValoresDosAtributosDosBrawlers(brawlersSelecionados, atributo) {
    return brawlersSelecionados.map(brawler => brawler[atributo]);
}

function gerarListaDeBrawlersComBrawlerAlvo() {

    const brawlersEmbaralhados = shuffle(brawlers);
    const brawlersSelecionados = [];

    for (const opcao of brawlersEmbaralhados) {
        if (!brawlersSelecionados.includes(opcao)) {
            brawlersSelecionados.push(opcao);
        }

        if (brawlersSelecionados.length === 4) {
            break; // Já foram selecionadas as 4 opções (1 correta e 3 erradas)
        }
    }

    return shuffle(brawlersSelecionados);
}

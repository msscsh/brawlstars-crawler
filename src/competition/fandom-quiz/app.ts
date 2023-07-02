import fs from 'fs';
import path from 'path';

interface Brawler {
    'nome': string;
    'vida': number;
    'Dano máximo por munição': number;
    'Raridade': string;
    'Range': string;
    'Velocidade de carregamento': string;
    'Velocidade de movimento': string;
    'Tipo': string;
  }

interface Question {
  type: string;
  question: string;
  options: string[];
  answer: Brawler;
  attribute: string
}

// Variáveis globais para controlar as combinações já utilizadas
let usedBrawlerGroups: Brawler[] = [];
let usedQuestionTypes: string[] = [];
let usedAttributes: string[] = [];
const questions: Question[] = [];

let brawlers: Brawler[] = [];
let valoresAtributosSuper = [];
let brawlersValidAttributesList = [];
let brawlersDirectValuesList = [];

function main() {
    const numQuestions = 20; // Número de perguntas desejado
    
    for (let i = 0; i < numQuestions; i++) {
      const question = generateUniqueQuestion();
      questions.push(question);
    }
  
    // Iterar sobre a lista de perguntas
    for (const question of questions) {
      console.log('----------------------');
      console.log('Pergunta:', question.question);
      console.log('Opções:', question.options);
      console.log('Resposta:', question.answer);
      console.log('----------------------');
    }
}

createBrawlersFromFile();
inicializarGlobais();
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
  const options = gerarOpcoesComValoresDosAtributosDosBrawlers(selectedBrawlers, 'nome', answer);

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
  const question = `Qual é o/a ${attribute} do brawler ${brawler.nome}?`;
  const answer = brawler[attribute];
  const options = gerarOpcoesComValoresDosAtributosDosBrawlers(undefined, attribute, answer);

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

function gerarOpcoesComValoresDosAtributosDosBrawlers(brawlersSelecionados, attribute, answer) {
    
    if(brawlersSelecionados) {
        return brawlersSelecionados.map(brawler => brawler[attribute]);
    }

    const distinctValues = new Set<string>();
    distinctValues.add(answer);

    while (distinctValues.size < 4) {
      const randomBrawler = brawlers[Math.floor(Math.random() * brawlers.length)];
      const attributeValue = randomBrawler[attribute];
  
      if (!distinctValues.has(attributeValue)) {
        distinctValues.add(attributeValue);
      }
    }
  
    return Array.from(distinctValues);

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


function createBrawlersFromFile(): void {
  const brawlers: Brawler[] = [];
  

//Leitura do arquivo
const pasta1 = '';
const nomeArquivo1 = 'dados_brawlers.txt';
const caminhoArquivo1 = path.join(__dirname, pasta1, nomeArquivo1);
  const lines = fs.readFileSync(caminhoArquivo1, 'utf8').split('\n');
  
  for (const line of lines) {
    const values = line.trim().split('\t');

    if(values[0] === 'Nome') {
        continue;
    }

    if (values.length === 8) {
      let brawler2 = {
        'nome': values[0],
        'vida': parseInt(values[1], 10),
        'Dano máximo por munição': parseInt(values[2], 10),
        'Raridade': values[3],
        'Range': values[4],
        'Velocidade de carregamento': values[5],
        'Velocidade de movimento': values[6],
        'Tipo': values[7],
      };
      
      brawlers.push(brawler2);
    }
  }
  
  //Leitura do arquivo
  const pasta = '';
  const nomeArquivo = 'informacoes.json';
  const caminhoArquivo = path.join(__dirname, pasta, nomeArquivo);
  fs.writeFileSync(caminhoArquivo, JSON.stringify(brawlers, null, 2));
}

function inicializarGlobais() {    

    //Leitura do arquivo
    const pasta = '';
    const nomeArquivo = 'informacoes.json';
    const caminhoArquivo = path.join(__dirname, pasta, nomeArquivo);

    //conversão para objeto
    const rawData = fs.readFileSync(caminhoArquivo, 'utf8');
    brawlers = JSON.parse(rawData);

    //Lista de valores para super
    valoresAtributosSuper = [];
    for (const brawler of brawlers) {
        const valor = brawler['super'];
        valoresAtributosSuper.push(valor);
    }

    //lista de atributos válidos para perguntas
    brawlersValidAttributesList = getBrawlerAttributes(brawlers[0])
                        .filter(item => (item === 'vida') || (item === 'Dano máximo por munição') );

    brawlersDirectValuesList = getBrawlerAttributes(brawlers[0])
                        .filter(item => (item === 'Velocidade de movimento') || (item === 'Velocidade de carregamento') || (item === 'Range') || (item === 'Tipo') || (item === 'Raridade'));

}


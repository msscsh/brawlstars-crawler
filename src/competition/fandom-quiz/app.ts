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
  answer: string;
}

//Leitura do arquivo
const pasta = '';
const nomeArquivo = 'informacoes.json';
const caminhoArquivo = path.join(__dirname, pasta, nomeArquivo);
console.log(caminhoArquivo);

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
const attributes = getBrawlerAttributes(brawlers[0])
                    .filter(item => (item !== 'nome') && (item !== 'super') );

function main() {

  const question = generateRandomQuestion(brawlers);

  console.log('Tipo de Pergunta:', question.type);
  console.log('Pergunta:', question.question);

  const shuffledOptions = question.options.sort(() => 0.5 - Math.random());
  const incorrectAnswer = getRandomOption(
    brawlers
        .filter(brawler => brawler.nome !== question.answer)
        .map(brawler => brawler.nome)
  );
  shuffledOptions.splice(1, 0, incorrectAnswer);

  console.log('Opções:', shuffledOptions);
  console.log('Resposta:', question.answer);
}

main();

function generateRandomQuestion(brawlers: Brawler[]): Question {
  const randomType = Math.random() < 0.5 ? 'attribute' : 'directInfo';

  if (randomType === 'attribute') {
      return generateAttributeQuestion(brawlers);
  }
  else {
      return generateDirectInfoQuestion(brawlers);
  }
}

function getRandomOption(options: string[]): string {
  const randomIndex = Math.floor(Math.random() * options.length);
  return options[randomIndex];
}

function generateAttributeQuestion(brawlers: Brawler[]): Question {
  const attribute = getRandomOption(attributes);
  const selectedBrawlers = getRandomBrawlers(brawlers, 3);

  const question = `Qual brawler possui ${attribute} maior?`;
  const options = selectedBrawlers.map(brawler => brawler.nome);
  const answer = selectedBrawlers.reduce((a, b) => (a[attribute] > b[attribute] ? a : b)).nome;

  return {
    type: 'Perguntas de cruzamento de informação de atributos do brawler',
    question,
    options,
    answer,
  };
}

function getBrawlerAttributes(brawler: Brawler): string[] {
  return Object.keys(brawler);
}

function generateDirectInfoQuestion(brawlers: Brawler[]): Question {

  const selectedBrawlers = getRandomBrawlers(brawlers, 1);
  const brawler = selectedBrawlers[0];
  const question = `Qual é a habilidade Super do brawler ${brawler.nome}?`;

  const opcoes = [];
  opcoes.push(brawler.super); // Adiciona a resposta correta
  const opcoesErradas = valoresAtributosSuper.slice(1).sort(() => 0.5 - Math.random()).slice(0, 3); // Seleciona 3 opções erradas aleatórias
  opcoes.push(...opcoesErradas); // Adiciona as opções erradas

  // Embaralha as opções corretas e erradas
  const opcoesEmbaralhadas = shuffle(opcoes);

  // Seleciona as primeiras opções não repetidas
  const opcoesSelecionadas = [];
  for (const opcao of opcoesEmbaralhadas) {
    if (!opcoesSelecionadas.includes(opcao)) {
      opcoesSelecionadas.push(opcao);
    }

    if (opcoesSelecionadas.length === 4) {
      break; // Já foram selecionadas as 4 opções (1 correta e 3 erradas)
    }
  }

  const options = opcoesSelecionadas;
  const answer = brawler.super;

  return {
    type: 'Perguntas de informação direta do brawler',
    question,
    options,
    answer,
  };
}

function shuffle(array: any[]) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}  

function getRandomBrawlers(brawlers: Brawler[], count: number): Brawler[] {
  const shuffled = brawlers.sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}
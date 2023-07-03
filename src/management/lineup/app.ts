import fs from 'fs';
import path from 'path';
import { PlayersData } from 'src/types/players-data';


// Ler o arquivo JSON
const pasta1 = '';
const nomeArquivo1 = 'club_data.json';
const caminhoArquivo1 = path.join(__dirname, pasta1, nomeArquivo1);

const jsonContent = fs.readFileSync(caminhoArquivo1, 'utf-8');
const jsonData = JSON.parse(jsonContent);
const data: PlayersData = jsonData;

function main() {
    // Iterar sobre a lista
    for (const player of data.players) {
      console.log('----------------------');
      console.log('Name:', player.name);
      console.log('Trophies:', player.trophies);
      console.log('----------------------');
    }
}

main();

import { PlayersData } from 'src/commons/types/players-data';
import { readJSONInFile } from '../../commons/functions/files';

function main() {

    const data: PlayersData = readJSONInFile('club_data.json');

    for (const player of data.players) {
      console.log('----------------------');
      console.log('Name:', player.name);
      console.log('Trophies:', player.trophies);
      console.log('----------------------');
    }
}

main();

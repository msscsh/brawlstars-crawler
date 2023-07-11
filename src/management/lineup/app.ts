import { PlayersData } from 'src/commons/types/players-data';
import { readJSONInFile } from '../../commons/functions/files';

export function getPlayers(): any {
    const data: PlayersData = readJSONInFile('club_data.json');
    return data.players;
}
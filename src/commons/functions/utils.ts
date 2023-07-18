import { readLinesInFile } from '../../commons/functions/files';

export function transformListOfPlayersToTwoDimensionalArray(players) {
    const lines = [];
    players.forEach(player => {
        const columns = [player.name, player.trophies, player.tag];
        lines.push(columns);
    });
    return lines;
}

export function transformTwoDimensionalArrayToListOfPlayers(arrayBidimensional) {
    const [header, ...data] = arrayBidimensional;
    const result = data.map(row => {
        return row.reduce((obj, value, index) => {
        obj[header[index]] = value;
        return obj;
        }, {});
    });
    return result
}

export function valueAlreadyExistsInThis(array, propriedade, valor) {
    return array.some(objeto => objeto[propriedade] === valor);
}

export function getTeamFromPlayerTag(playerTag) {
    
    const lines = readLinesInFile('team_relation.txt');

    for (let i = 0; i < lines.length; i++) {
        const [team, players] = lines[i].split(':');
        const playerList = players.split(';').map(player => player.trim());
        
        if (playerList.includes(playerTag)) {
        return team;
        }
    }

    return 'Time não encontrado';
}
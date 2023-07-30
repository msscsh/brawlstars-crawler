import { readJSONInFile } from '../../commons/functions/files';

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
    
    const times = readJSONInFile('team_relation.json');

    if(times) {
        for (const time of times) {
            if (time.players.includes(playerTag)) {
                return time.name;
            }
        }
        return 'Player is not associated with any team';
    }
    else {
        return 'Teams file not yet created';
    }

}
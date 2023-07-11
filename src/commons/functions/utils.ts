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
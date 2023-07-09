import fs from 'fs';
import path from 'path';

export function readStringInFile(fileName: string) : string {
    const previousFolder = path.resolve(__dirname, '..');
    const filePath = path.join(previousFolder, 'files', fileName);
    return fs.readFileSync(filePath, 'utf-8');
}

export function readJSONInFile(fileName: string) : any {
    return JSON.parse(readStringInFile(fileName))
}

export function readLinesInFile(fileName: string) : string[] {
    return readStringInFile(fileName).split('\n')
}

export function createFileWithContent(fileName: string, content: any) : string {
    const previousFolder = path.resolve(__dirname, '..');
    const filePath = path.join(previousFolder, 'files', fileName);
    fs.writeFileSync(filePath, JSON.stringify(content, null, 2));
    return fs.readFileSync(filePath, 'utf-8');
}

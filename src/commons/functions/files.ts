import fs from "fs";
import path from "path";

export function readStringInFile(fileName: string): string {
	const previousFolder = path.resolve(__dirname, "..");
	const filePath = path.join(previousFolder, "files", fileName);
	try {
		return fs.readFileSync(filePath, "utf-8");
	} catch (error) {
		console.error(`File not found: ${error.message}`);
		return undefined;
	}
}

export function readJSONInFile(fileName: string): any {
	const readedFile = readStringInFile(fileName);
	return readedFile ? JSON.parse(readedFile) : undefined;
}

export function readLinesInFile(fileName: string): string[] {
	const readedFile = readStringInFile(fileName);
	return readedFile ? readedFile.split("\n") : undefined;
}

export function createFileWithJSONContent(
	fileName: string,
	content: any,
): string {
	const previousFolder = path.resolve(__dirname, "..");
	const filePath = path.join(previousFolder, "files", fileName);
	fs.writeFileSync(filePath, JSON.stringify(content, null, 2));
	return fs.readFileSync(filePath, "utf-8");
}

export function createPersistentFileWithJSONContent(
	fileName: string,
	content: any,
): string {
	const previousFolder = path.resolve(__dirname, "../../../src/commons/");
	const filePath = path.join(previousFolder, "files", fileName);
	fs.writeFileSync(filePath, JSON.stringify(content, null, 2));
	return fs.readFileSync(filePath, "utf-8");
}

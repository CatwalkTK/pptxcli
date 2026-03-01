import { writeFileSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import { CsvRow } from '../types';

type WriteOptions = {
  readonly pretty: boolean;
};

export const writeJsonFile = (
  outputPath: string,
  data: ReadonlyArray<CsvRow>,
  options: WriteOptions,
): number => {
  const dir = dirname(outputPath);
  mkdirSync(dir, { recursive: true });

  const jsonContent = options.pretty
    ? JSON.stringify(data, null, 2)
    : JSON.stringify(data);

  writeFileSync(outputPath, jsonContent, { encoding: 'utf-8' });

  return Buffer.byteLength(jsonContent, 'utf-8');
};

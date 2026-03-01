import type { CsvRow, CsvParseOptions } from '../types.js';

const DEFAULT_OPTIONS: CsvParseOptions = {
  delimiter: ',',
  hasHeader: true,
  encoding: 'utf-8',
};

const parseCsvLine = (line: string, delimiter: string): string[] => {
  const fields: string[] = [];
  let current = '';
  let inQuotes = false;
  let i = 0;

  while (i < line.length) {
    const char = line[i];

    if (inQuotes) {
      if (char === '"') {
        if (i + 1 < line.length && line[i + 1] === '"') {
          current += '"';
          i += 2;
          continue;
        }
        inQuotes = false;
        i++;
        continue;
      }
      current += char;
      i++;
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      i++;
      continue;
    }

    if (char === delimiter) {
      fields.push(current.trim());
      current = '';
      i++;
      continue;
    }

    current += char;
    i++;
  }

  fields.push(current.trim());
  return fields;
};

export const parseCsvContent = (
  content: string,
  options: Partial<CsvParseOptions> = {},
): { headers: string[]; rows: CsvRow[]; totalLines: number } => {
  const opts: CsvParseOptions = { ...DEFAULT_OPTIONS, ...options };

  const lines = content
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split('\n')
    .filter((line) => line.trim().length > 0);

  if (lines.length === 0) {
    return { headers: [], rows: [], totalLines: 0 };
  }

  const headers = opts.hasHeader
    ? parseCsvLine(lines[0], opts.delimiter)
    : parseCsvLine(lines[0], opts.delimiter).map((_, index) => `column_${index + 1}`);

  const dataLines = opts.hasHeader ? lines.slice(1) : lines;
  const totalLines = dataLines.length;

  const rows: CsvRow[] = dataLines.map((line) => {
    const values = parseCsvLine(line, opts.delimiter);
    const row: CsvRow = {};

    for (const [index, header] of headers.entries()) {
      row[header] = index < values.length ? values[index] : '';
    }

    return row;
  });

  return { headers, rows, totalLines };
};

export const countLines = (content: string): number => {
  const lines = content
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .split('\n')
    .filter((line) => line.trim().length > 0);

  return Math.max(0, lines.length - 1);
};

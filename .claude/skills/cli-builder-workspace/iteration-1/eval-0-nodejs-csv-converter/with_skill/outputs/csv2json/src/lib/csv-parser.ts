import type { CsvParseOptions, ParsedCsv } from '../types.js';

const DEFAULT_OPTIONS: Required<CsvParseOptions> = {
  delimiter: ',',
  hasHeader: true,
  trimValues: true,
  skipEmptyLines: true,
};

/**
 * Parse a raw CSV string into structured data.
 * Handles quoted fields, escaped quotes, and multi-line values within quotes.
 * Business logic only -- no UI imports.
 */
export const parseCsv = (raw: string, opts: CsvParseOptions = {}): ParsedCsv => {
  const options = { ...DEFAULT_OPTIONS, ...opts };
  const lines = splitCsvLines(raw, options.delimiter);

  const filteredLines = options.skipEmptyLines
    ? lines.filter((line) => line.some((cell) => cell.length > 0))
    : lines;

  if (filteredLines.length === 0) {
    return { headers: [], rows: [] };
  }

  const processedLines = options.trimValues
    ? filteredLines.map((line) => line.map((cell) => cell.trim()))
    : filteredLines;

  if (options.hasHeader) {
    const [headerRow, ...dataRows] = processedLines;
    const headers = headerRow ?? [];
    return { headers, rows: dataRows };
  }

  const columnCount = processedLines[0]?.length ?? 0;
  const headers = Array.from({ length: columnCount }, (_, i) => `column_${i + 1}`);
  return { headers, rows: processedLines };
};

/**
 * Convert parsed CSV data to an array of record objects.
 */
export const toRecords = (
  parsed: ParsedCsv,
): ReadonlyArray<Record<string, string>> => {
  const { headers, rows } = parsed;

  return rows.map((row) => {
    const record: Record<string, string> = {};
    for (let i = 0; i < headers.length; i++) {
      const key = headers[i] ?? `column_${i + 1}`;
      record[key] = row[i] ?? '';
    }
    return record;
  });
};

/**
 * Split a CSV string into lines of fields, respecting quoted values.
 */
const splitCsvLines = (raw: string, delimiter: string): ReadonlyArray<ReadonlyArray<string>> => {
  const lines: string[][] = [];
  let currentLine: string[] = [];
  let currentField = '';
  let inQuotes = false;
  let i = 0;

  while (i < raw.length) {
    const char = raw[i];

    if (inQuotes) {
      if (char === '"') {
        if (i + 1 < raw.length && raw[i + 1] === '"') {
          // Escaped quote
          currentField += '"';
          i += 2;
          continue;
        }
        // End of quoted field
        inQuotes = false;
        i++;
        continue;
      }
      currentField += char;
      i++;
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      i++;
      continue;
    }

    if (char === delimiter) {
      currentLine.push(currentField);
      currentField = '';
      i++;
      continue;
    }

    if (char === '\r') {
      if (i + 1 < raw.length && raw[i + 1] === '\n') {
        i++; // skip \r, \n handled next
      }
      currentLine.push(currentField);
      currentField = '';
      lines.push(currentLine);
      currentLine = [];
      i++;
      continue;
    }

    if (char === '\n') {
      currentLine.push(currentField);
      currentField = '';
      lines.push(currentLine);
      currentLine = [];
      i++;
      continue;
    }

    currentField += char;
    i++;
  }

  // Handle last field/line
  if (currentField.length > 0 || currentLine.length > 0) {
    currentLine.push(currentField);
    lines.push(currentLine);
  }

  return lines;
};

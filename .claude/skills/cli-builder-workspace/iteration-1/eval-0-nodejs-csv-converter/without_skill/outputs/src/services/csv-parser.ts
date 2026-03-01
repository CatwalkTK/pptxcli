import { createReadStream, statSync } from 'fs';
import { parse } from 'csv-parse';
import { CsvRow } from '../types';
import { createProgressBar, ProgressBar } from '../ui/progress';

type ParseOptions = {
  readonly delimiter: string;
  readonly useHeader: boolean;
};

const countLines = (filePath: string): Promise<number> => {
  return new Promise((resolve, reject) => {
    let lineCount = 0;
    const stream = createReadStream(filePath, { encoding: 'utf-8' });

    stream.on('data', (chunk: string) => {
      for (let i = 0; i < chunk.length; i++) {
        if (chunk[i] === '\n') {
          lineCount++;
        }
      }
    });

    stream.on('end', () => {
      resolve(lineCount);
    });

    stream.on('error', (err) => {
      reject(err);
    });
  });
};

export const parseCsvFile = (
  filePath: string,
  options: ParseOptions,
): Promise<ReadonlyArray<CsvRow>> => {
  return new Promise(async (resolve, reject) => {
    const rows: CsvRow[] = [];
    let progressBar: ProgressBar | null = null;
    let rowCount = 0;

    try {
      const totalLines = await countLines(filePath);
      const dataLines = options.useHeader ? Math.max(totalLines - 1, 0) : totalLines;

      if (dataLines > 0) {
        progressBar = createProgressBar();
        progressBar.start(dataLines, 0);
      }

      const parser = createReadStream(filePath, { encoding: 'utf-8' }).pipe(
        parse({
          columns: options.useHeader ? true : false,
          delimiter: options.delimiter,
          skip_empty_lines: true,
          trim: true,
          relax_column_count: true,
        }),
      );

      parser.on('data', (row: CsvRow) => {
        rows.push(row);
        rowCount++;
        if (progressBar) {
          progressBar.update(rowCount);
        }
      });

      parser.on('end', () => {
        if (progressBar) {
          progressBar.update(dataLines);
          progressBar.stop();
        }
        resolve(rows);
      });

      parser.on('error', (err: Error) => {
        if (progressBar) {
          progressBar.stop();
        }
        reject(err);
      });
    } catch (err) {
      reject(err);
    }
  });
};

export const getFileSize = (filePath: string): number => {
  const stats = statSync(filePath);
  return stats.size;
};

import { existsSync } from 'fs';
import { extname } from 'path';

export const validateInputFile = (filePath: string): void => {
  if (!existsSync(filePath)) {
    throw new Error(`Input file not found: ${filePath}`);
  }

  const ext = extname(filePath).toLowerCase();
  if (ext !== '.csv') {
    throw new Error(
      `Invalid file extension "${ext}". Expected ".csv" file.`,
    );
  }
};

export const validateDelimiter = (delimiter: string): void => {
  if (delimiter.length !== 1) {
    throw new Error(
      `Delimiter must be a single character. Got "${delimiter}" (length: ${delimiter.length}).`,
    );
  }
};

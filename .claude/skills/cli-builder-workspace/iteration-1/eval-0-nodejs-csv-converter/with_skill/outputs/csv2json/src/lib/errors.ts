export class CliError extends Error {
  constructor(
    message: string,
    public readonly exitCode: number = 1,
    public readonly hint?: string,
  ) {
    super(message);
    this.name = 'CliError';
  }
}

export class FileNotFoundError extends CliError {
  constructor(filePath: string) {
    super(
      `File not found: ${filePath}`,
      1,
      'Check the file path and try again.',
    );
    this.name = 'FileNotFoundError';
  }
}

export class InvalidCsvError extends CliError {
  constructor(detail: string) {
    super(
      `Invalid CSV: ${detail}`,
      1,
      'Ensure the file is a valid CSV with consistent columns.',
    );
    this.name = 'InvalidCsvError';
  }
}

export class OutputWriteError extends CliError {
  constructor(filePath: string, reason: string) {
    super(
      `Cannot write output to ${filePath}: ${reason}`,
      1,
      'Check directory permissions and available disk space.',
    );
    this.name = 'OutputWriteError';
  }
}

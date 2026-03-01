export type CsvParseOptions = {
  readonly delimiter: string;
  readonly hasHeader: boolean;
  readonly encoding: BufferEncoding;
};

export type ConvertOptions = {
  readonly input: string;
  readonly output?: string;
  readonly delimiter: string;
  readonly pretty: boolean;
  readonly noHeader: boolean;
  readonly encoding: BufferEncoding;
};

export type ConvertResult = {
  readonly rowCount: number;
  readonly outputPath: string;
  readonly durationMs: number;
};

export type CsvRow = Record<string, string>;

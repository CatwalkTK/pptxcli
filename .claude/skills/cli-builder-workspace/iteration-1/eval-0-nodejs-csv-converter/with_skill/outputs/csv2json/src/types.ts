export type CsvParseOptions = {
  readonly delimiter?: string;
  readonly hasHeader?: boolean;
  readonly trimValues?: boolean;
  readonly skipEmptyLines?: boolean;
};

export type ConvertOptions = {
  readonly input: string;
  readonly output?: string;
  readonly delimiter?: string;
  readonly pretty?: boolean;
  readonly array?: boolean;
  readonly noHeader?: boolean;
  readonly verbose?: boolean;
};

export type ConvertResult = {
  readonly records: ReadonlyArray<Record<string, string>>;
  readonly rowCount: number;
  readonly headers: ReadonlyArray<string>;
  readonly outputPath: string;
  readonly inputSizeBytes: number;
  readonly outputSizeBytes: number;
  readonly durationMs: number;
};

export type ParsedCsv = {
  readonly headers: ReadonlyArray<string>;
  readonly rows: ReadonlyArray<ReadonlyArray<string>>;
};

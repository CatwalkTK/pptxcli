export type CsvRow = Record<string, string>;

export type ConvertOptions = {
  readonly output?: string;
  readonly delimiter: string;
  readonly pretty: boolean;
  readonly header: boolean;
};

export type ConversionResult = {
  readonly rowCount: number;
  readonly outputPath: string;
  readonly fileSize: number;
};

export type ParsedCsvData = {
  readonly rows: ReadonlyArray<CsvRow>;
  readonly totalRows: number;
};

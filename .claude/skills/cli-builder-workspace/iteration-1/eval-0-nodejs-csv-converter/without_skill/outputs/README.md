# csv2json

A CLI tool to convert CSV files to JSON format, built with TypeScript.

## Features

- ASCII banner display on launch
- Progress bar during conversion
- Configurable output path with `--output` option
- Custom delimiter support
- Pretty-print or compact JSON output
- File size and timing statistics

## Setup

```bash
npm install
npm run build
```

## Usage

### Basic conversion

```bash
csv2json convert input.csv
```

This will create `input.json` in the same directory as the input file.

### Specify output path

```bash
csv2json convert input.csv --output ./output/result.json
csv2json convert input.csv -o ./output/result.json
```

### Custom delimiter

```bash
csv2json convert data.csv --delimiter ";"
csv2json convert data.csv -d "\t"
```

### Compact JSON (no pretty-printing)

```bash
csv2json convert data.csv --no-pretty
```

### No header row

```bash
csv2json convert data.csv --no-header
```

### Full example

```bash
csv2json convert sample.csv -o output.json -d "," --pretty
```

## Development

```bash
# Run directly with ts-node
npm run dev -- convert sample.csv -o output.json

# Build and run
npm run build
node dist/index.js convert sample.csv -o output.json
```

## Project Structure

```
csv2json/
├── src/
│   ├── index.ts              # Entry point & CLI setup
│   ├── commands/
│   │   └── convert.ts        # Convert command handler
│   ├── services/
│   │   ├── csv-parser.ts     # CSV parsing logic
│   │   └── json-writer.ts    # JSON output logic
│   ├── types/
│   │   └── index.ts          # Type definitions
│   ├── ui/
│   │   ├── banner.ts         # ASCII banner display
│   │   └── progress.ts       # Progress bar & spinner
│   └── utils/
│       ├── format.ts         # Formatting utilities
│       └── validate.ts       # Input validation
├── sample.csv                # Sample data for testing
├── package.json
├── tsconfig.json
└── README.md
```

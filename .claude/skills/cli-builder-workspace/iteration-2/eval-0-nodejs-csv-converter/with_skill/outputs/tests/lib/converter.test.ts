import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { writeFile, readFile, mkdir, rm } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';
import { convertCsvToJson } from '../../src/lib/converter.js';

describe('convertCsvToJson', () => {
  let testDir: string;

  beforeEach(async () => {
    testDir = join(tmpdir(), `csv2json-test-${Date.now()}`);
    await mkdir(testDir, { recursive: true });
  });

  afterEach(async () => {
    await rm(testDir, { recursive: true, force: true });
  });

  it('should convert a simple CSV to JSON', async () => {
    const csvPath = join(testDir, 'test.csv');
    await writeFile(csvPath, 'name,age,city\nAlice,30,Tokyo\nBob,25,Osaka');

    const result = await convertCsvToJson({
      input: csvPath,
      delimiter: ',',
      pretty: true,
      noHeader: false,
      encoding: 'utf-8',
    });

    expect(result.rowCount).toBe(2);
    expect(result.outputPath).toContain('test.json');
    expect(result.durationMs).toBeGreaterThanOrEqual(0);

    const jsonContent = await readFile(result.outputPath, 'utf-8');
    const parsed = JSON.parse(jsonContent);
    expect(parsed).toHaveLength(2);
    expect(parsed[0]).toEqual({ name: 'Alice', age: '30', city: 'Tokyo' });
  });

  it('should write to custom output path', async () => {
    const csvPath = join(testDir, 'input.csv');
    const outputPath = join(testDir, 'custom-output.json');
    await writeFile(csvPath, 'id,value\n1,hello\n2,world');

    const result = await convertCsvToJson({
      input: csvPath,
      output: outputPath,
      delimiter: ',',
      pretty: true,
      noHeader: false,
      encoding: 'utf-8',
    });

    expect(result.outputPath).toBe(outputPath);

    const jsonContent = await readFile(outputPath, 'utf-8');
    const parsed = JSON.parse(jsonContent);
    expect(parsed).toHaveLength(2);
  });

  it('should produce minified JSON when pretty is false', async () => {
    const csvPath = join(testDir, 'test.csv');
    await writeFile(csvPath, 'name,age\nAlice,30');

    const result = await convertCsvToJson({
      input: csvPath,
      delimiter: ',',
      pretty: false,
      noHeader: false,
      encoding: 'utf-8',
    });

    const jsonContent = await readFile(result.outputPath, 'utf-8');
    expect(jsonContent).not.toContain('\n');
  });

  it('should throw error for non-existent file', async () => {
    await expect(
      convertCsvToJson({
        input: join(testDir, 'nonexistent.csv'),
        delimiter: ',',
        pretty: true,
        noHeader: false,
        encoding: 'utf-8',
      }),
    ).rejects.toThrow('Input file not found');
  });

  it('should throw error for empty file', async () => {
    const csvPath = join(testDir, 'empty.csv');
    await writeFile(csvPath, '');

    await expect(
      convertCsvToJson({
        input: csvPath,
        delimiter: ',',
        pretty: true,
        noHeader: false,
        encoding: 'utf-8',
      }),
    ).rejects.toThrow('Input file is empty');
  });

  it('should call onProgress callback during conversion', async () => {
    const csvPath = join(testDir, 'progress.csv');
    await writeFile(csvPath, 'name,age\nAlice,30\nBob,25\nCharlie,35');

    const progressCalls: Array<{ current: number; total: number }> = [];

    await convertCsvToJson(
      {
        input: csvPath,
        delimiter: ',',
        pretty: true,
        noHeader: false,
        encoding: 'utf-8',
      },
      (current, total) => {
        progressCalls.push({ current, total });
      },
    );

    expect(progressCalls.length).toBe(3);
    expect(progressCalls[0]).toEqual({ current: 1, total: 3 });
    expect(progressCalls[2]).toEqual({ current: 3, total: 3 });
  });

  it('should handle semicolon delimiter', async () => {
    const csvPath = join(testDir, 'semicolon.csv');
    await writeFile(csvPath, 'name;age;city\nAlice;30;Tokyo\nBob;25;Osaka');

    const result = await convertCsvToJson({
      input: csvPath,
      delimiter: ';',
      pretty: true,
      noHeader: false,
      encoding: 'utf-8',
    });

    const jsonContent = await readFile(result.outputPath, 'utf-8');
    const parsed = JSON.parse(jsonContent);
    expect(parsed[0]).toEqual({ name: 'Alice', age: '30', city: 'Tokyo' });
  });
});

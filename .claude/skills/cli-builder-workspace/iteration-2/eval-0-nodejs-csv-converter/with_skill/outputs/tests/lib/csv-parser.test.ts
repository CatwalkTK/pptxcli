import { describe, it, expect } from 'vitest';
import { parseCsvContent, countLines } from '../../src/lib/csv-parser.js';

describe('parseCsvContent', () => {
  it('should parse simple CSV with headers', () => {
    const csv = 'name,age,city\nAlice,30,Tokyo\nBob,25,Osaka';
    const { headers, rows } = parseCsvContent(csv);

    expect(headers).toEqual(['name', 'age', 'city']);
    expect(rows).toHaveLength(2);
    expect(rows[0]).toEqual({ name: 'Alice', age: '30', city: 'Tokyo' });
    expect(rows[1]).toEqual({ name: 'Bob', age: '25', city: 'Osaka' });
  });

  it('should handle quoted fields with commas', () => {
    const csv = 'name,description\nAlice,"Hello, World"\nBob,"Nice, day"';
    const { rows } = parseCsvContent(csv);

    expect(rows[0]).toEqual({ name: 'Alice', description: 'Hello, World' });
    expect(rows[1]).toEqual({ name: 'Bob', description: 'Nice, day' });
  });

  it('should handle escaped quotes within quoted fields', () => {
    const csv = 'name,quote\nAlice,"She said ""hello"""\nBob,"Test"';
    const { rows } = parseCsvContent(csv);

    expect(rows[0]).toEqual({ name: 'Alice', quote: 'She said "hello"' });
    expect(rows[1]).toEqual({ name: 'Bob', quote: 'Test' });
  });

  it('should handle custom delimiter', () => {
    const csv = 'name;age;city\nAlice;30;Tokyo\nBob;25;Osaka';
    const { headers, rows } = parseCsvContent(csv, { delimiter: ';' });

    expect(headers).toEqual(['name', 'age', 'city']);
    expect(rows).toHaveLength(2);
    expect(rows[0]).toEqual({ name: 'Alice', age: '30', city: 'Tokyo' });
  });

  it('should generate column names when hasHeader is false', () => {
    const csv = 'Alice,30,Tokyo\nBob,25,Osaka';
    const { headers, rows } = parseCsvContent(csv, { hasHeader: false });

    expect(headers).toEqual(['column_1', 'column_2', 'column_3']);
    expect(rows).toHaveLength(2);
    expect(rows[0]).toEqual({ column_1: 'Alice', column_2: '30', column_3: 'Tokyo' });
  });

  it('should return empty result for empty content', () => {
    const { headers, rows, totalLines } = parseCsvContent('');
    expect(headers).toEqual([]);
    expect(rows).toEqual([]);
    expect(totalLines).toBe(0);
  });

  it('should handle Windows-style line endings (CRLF)', () => {
    const csv = 'name,age\r\nAlice,30\r\nBob,25';
    const { rows } = parseCsvContent(csv);

    expect(rows).toHaveLength(2);
    expect(rows[0]).toEqual({ name: 'Alice', age: '30' });
  });

  it('should handle missing values with empty strings', () => {
    const csv = 'name,age,city\nAlice,30\nBob,,Osaka';
    const { rows } = parseCsvContent(csv);

    expect(rows[0]).toEqual({ name: 'Alice', age: '30', city: '' });
    expect(rows[1]).toEqual({ name: 'Bob', age: '', city: 'Osaka' });
  });

  it('should skip blank lines', () => {
    const csv = 'name,age\nAlice,30\n\nBob,25\n';
    const { rows } = parseCsvContent(csv);

    expect(rows).toHaveLength(2);
  });
});

describe('countLines', () => {
  it('should count data lines excluding header', () => {
    const csv = 'name,age\nAlice,30\nBob,25';
    expect(countLines(csv)).toBe(2);
  });

  it('should return 0 for empty content', () => {
    expect(countLines('')).toBe(0);
  });

  it('should return 0 for header-only content', () => {
    expect(countLines('name,age')).toBe(0);
  });
});

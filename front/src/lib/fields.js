import { fromInputDateTime, toInputDateTime } from './format.js';

// Conversões entre os campos do formulário (strings) e o JSON da API.

export function emptyValues(fields) {
  return Object.fromEntries(fields.map((f) => [f.key, '']));
}

export function valuesFromRecord(fields, record) {
  const values = {};
  for (const f of fields) {
    const raw = record?.[f.key];
    if (f.type === 'datetime') values[f.key] = toInputDateTime(raw);
    else values[f.key] = raw === null || raw === undefined ? '' : String(raw);
  }
  return values;
}

export function toPayload(fields, values) {
  const payload = {};
  for (const f of fields) {
    const raw = values[f.key];
    if (f.type === 'number') {
      payload[f.key] = raw === '' || raw == null ? null : Number(raw);
    } else if (f.type === 'datetime') {
      payload[f.key] = fromInputDateTime(raw);
    } else if (f.type === 'select') {
      payload[f.key] = raw || null;
    } else {
      const text = String(raw ?? '').trim();
      payload[f.key] = text === '' && !f.required ? null : text;
    }
  }
  return payload;
}

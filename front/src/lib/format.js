const pad = (n) => String(n).padStart(2, '0');

export function formatDateTime(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '—';
  return d.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
}

export function dateParts(iso) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return { day: '--', month: '---', time: '--:--' };
  return {
    day: pad(d.getDate()),
    month: d.toLocaleString('pt-BR', { month: 'short' }).replace('.', ''),
    time: `${pad(d.getHours())}:${pad(d.getMinutes())}`,
  };
}

// ISO -> valor de <input type="datetime-local">
export function toInputDateTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return '';
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// valor de <input type="datetime-local"> -> ISO
export function fromInputDateTime(value) {
  if (!value) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

export function shortId(id) {
  return id ? String(id).slice(0, 8) : '—';
}

export function displayName(user) {
  if (!user?.email) return 'atleta';
  return user.email.split('@')[0];
}

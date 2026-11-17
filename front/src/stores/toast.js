import { writable } from 'svelte/store';

export const toasts = writable([]);

let counter = 0;

function push(tone, message, timeout = 4200) {
  const id = ++counter;
  toasts.update((list) => [...list, { id, tone, message }]);
  setTimeout(() => dismiss(id), timeout);
}

export function dismiss(id) {
  toasts.update((list) => list.filter((t) => t.id !== id));
}

export const toast = {
  success: (message) => push('success', message),
  error: (message) => push('error', message, 6000),
};

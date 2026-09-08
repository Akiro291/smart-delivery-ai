// Единая мета статусов заказов: подписи + классы бейджей
export const ORDER_STATUS_META: Record<string, { label: string; class: string }> = {
  PENDING: { label: 'Ожидает', class: 'bg-amber-100 text-amber-800' },
  CONFIRMED: { label: 'Подтверждён', class: 'bg-blue-100 text-blue-800' },
  ASSIGNED: { label: 'Назначен', class: 'bg-indigo-100 text-indigo-800' },
  IN_PROGRESS: { label: 'В пути', class: 'bg-cyan-100 text-cyan-800' },
  COMPLETED: { label: 'Доставлен', class: 'bg-emerald-100 text-emerald-800' },
  CANCELLED: { label: 'Отменён', class: 'bg-red-100 text-red-800' },
}

export const ORDER_STATUS_LABELS = Object.fromEntries(
  Object.entries(ORDER_STATUS_META).map(([key, meta]) => [key, meta.label]),
) as Record<string, string>

export function statusLabel(status: string): string {
  return ORDER_STATUS_LABELS[status] || status
}

export function statusClass(status: string): string {
  return ORDER_STATUS_META[status]?.class || 'bg-gray-100 text-gray-700'
}

export function formatMoney(value: number | string | null | undefined): string {
  return Number(value || 0).toLocaleString('ru-RU', { maximumFractionDigits: 2 })
}

export function formatDate(value: string | null | undefined): string {
  if (!value) return '-'
  return new Date(value).toLocaleString('ru-RU', { dateStyle: 'short', timeStyle: 'short' })
}

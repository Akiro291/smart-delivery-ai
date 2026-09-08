// Тесты Pinia-стора корзины (локальная логика геттеров)
import { describe, it, expect } from 'vitest'

interface CartItem {
  id: number
  product_id: number
  product_name?: string
  product_price?: number
  subtotal?: number
  quantity: number
}

function totalQuantity(items: CartItem[]): number {
  return items.reduce((sum, i) => sum + i.quantity, 0)
}

function totalAmount(items: CartItem[]): number {
  return items.reduce((sum, i) => sum + (i.subtotal ?? (i.product_price || 0) * i.quantity), 0)
}

describe('Корзина: локальные расчёты', () => {
  it('считает общее количество', () => {
    const items: CartItem[] = [
      { id: 1, product_id: 1, quantity: 2, subtotal: 600 },
      { id: 2, product_id: 2, quantity: 1, subtotal: 299 },
    ]
    expect(totalQuantity(items)).toBe(3)
  })

  it('считает сумму по subtotal', () => {
    const items: CartItem[] = [
      { id: 1, product_id: 1, quantity: 2, subtotal: 600 },
      { id: 2, product_id: 2, quantity: 1, subtotal: 299 },
    ]
    expect(totalAmount(items)).toBe(899)
  })

  it('использует price*quantity когда subtotal отсутствует', () => {
    const items: CartItem[] = [{ id: 1, product_id: 1, quantity: 3, product_price: 100 }]
    expect(totalAmount(items)).toBe(300)
  })

  it('пустая корзина равна нулю', () => {
    expect(totalQuantity([])).toBe(0)
    expect(totalAmount([])).toBe(0)
  })
})

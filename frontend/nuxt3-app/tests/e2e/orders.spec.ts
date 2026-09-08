import { test, expect } from '@playwright/test'

test.describe('Заказы', () => {
  test('неавторизованный пользователь перенаправляется на логин', async ({ page }) => {
    await page.goto('/orders')
    await expect(page).toHaveURL(/\/auth\/login/, { timeout: 10_000 })
  })
})

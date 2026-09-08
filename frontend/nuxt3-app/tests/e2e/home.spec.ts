import { test, expect } from '@playwright/test'

test.describe('Главная страница', () => {
  test('открывается и содержит заголовок проекта', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Smart Delivery/)
  })
})

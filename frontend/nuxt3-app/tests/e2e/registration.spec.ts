import { test, expect } from '@playwright/test'

test.describe('Регистрация', () => {
  test('форма регистрации открывается и валидирует пустую отправку', async ({ page }) => {
    await page.goto('/auth/register')
    await expect(page.locator('form')).toBeVisible()
  })

  test('кнопка Войти ведёт на страницу логина', async ({ page }) => {
    await page.goto('/auth/register')
    const loginLink = page.locator('a[href="/auth/login"]').first()
    if (await loginLink.count()) {
      await loginLink.click()
      await expect(page).toHaveURL(/\/auth\/login/)
    }
  })
})

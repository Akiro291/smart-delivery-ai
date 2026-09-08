import { describe, it, expect } from 'vitest'

describe('Страница /', () => {
  it('файл страницы существует и корректен', async () => {
    const fs = await import('node:fs')
    const path = await import('node:path')
    const pagePath = path.resolve(__dirname, '../../pages/index.vue')
    expect(fs.existsSync(pagePath)).toBe(true)
    const content = fs.readFileSync(pagePath, 'utf-8')
    expect(content).toContain('<script')
    expect(content).toContain('<template>')
  })
})

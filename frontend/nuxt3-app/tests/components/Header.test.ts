import { describe, it, expect } from 'vitest'

describe('Компонент Header', () => {
  it('файл компонента существует и использует script setup', async () => {
    const fs = await import('node:fs')
    const path = await import('node:path')
    const componentPath = path.resolve(__dirname, '../../components/Header.vue')
    expect(fs.existsSync(componentPath)).toBe(true)
    const content = fs.readFileSync(componentPath, 'utf-8')
    expect(content).toContain('<script setup')
    expect(content).toContain('<template>')
  })
})

import { describe, it, expect } from 'vitest'
import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

describe('Компоненты layout', () => {
  it('AppHeader существует и использует script setup', () => {
    const componentPath = resolve(__dirname, '../../components/layout/AppHeader.vue')
    expect(existsSync(componentPath)).toBe(true)
    const content = readFileSync(componentPath, 'utf-8')
    expect(content).toContain('<script setup')
    expect(content).toContain('<template>')
  })

  it('AppSidebar существует и поддерживает сворачивание', () => {
    const componentPath = resolve(__dirname, '../../components/layout/AppSidebar.vue')
    expect(existsSync(componentPath)).toBe(true)
    const content = readFileSync(componentPath, 'utf-8')
    expect(content).toContain('collapsed')
  })

  it('UiStat принимает тон градиента', () => {
    const componentPath = resolve(__dirname, '../../components/ui/UiStat.vue')
    expect(existsSync(componentPath)).toBe(true)
    const content = readFileSync(componentPath, 'utf-8')
    expect(content).toContain('tone')
  })
})

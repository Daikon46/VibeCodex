import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest'

import App from './App'

describe('App', () => {
  beforeEach(() => {
    localStorage.clear()
    vi.restoreAllMocks()
  })

  afterEach(() => {
    cleanup()
  })

  test('shows validation when no muscle groups are selected', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => [{ key: 'chest', label: 'Chest' }],
    })

    render(<App />)

    await screen.findByText('Chest')
    fireEvent.click(screen.getByRole('button', { name: /generate workout/i }))

    expect(await screen.findByText('Select at least one muscle group.')).toBeInTheDocument()
  })

  test('persists theme selection', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => [{ key: 'chest', label: 'Chest' }],
    })

    render(<App />)
    await screen.findByText('Chest')

    fireEvent.click(screen.getByRole('button', { name: /switch to light theme/i }))

    await waitFor(() => {
      expect(localStorage.getItem('workout-planner-theme')).toBe('light')
    })
  })

  test('switches interface language to chinese', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => [{ key: 'chest', label: 'Chest' }],
    })

    render(<App />)

    await screen.findByText('Chest')
    fireEvent.click(screen.getByRole('button', { name: 'Language' }))
    fireEvent.click(screen.getByRole('button', { name: /🇨🇳zh/i }))

    expect(await screen.findByText('胸部')).toBeInTheDocument()
    expect(screen.getByText('自适应训练计划生成器')).toBeInTheDocument()
  })

  test('switches interface language to english', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => [{ key: 'chest', label: 'Chest' }],
    })

    render(<App />)

    await screen.findByText('Chest')
    fireEvent.click(screen.getByRole('button', { name: 'Language' }))
    fireEvent.click(screen.getByRole('button', { name: /🇷🇺ru/i }))

    expect(await screen.findByText('Грудь')).toBeInTheDocument()
    expect(screen.getByText('Адаптивный конструктор тренировок')).toBeInTheDocument()
  })
})

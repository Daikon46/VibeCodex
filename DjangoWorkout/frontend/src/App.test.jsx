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
})

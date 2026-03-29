import React, { useEffect, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const THEME_STORAGE_KEY = 'workout-planner-theme'

function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_STORAGE_KEY) || 'dark')
  const [muscleGroups, setMuscleGroups] = useState([])
  const [selectedGroups, setSelectedGroups] = useState([])
  const [duration, setDuration] = useState(30)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  }, [theme])

  useEffect(() => {
    async function loadMuscleGroups() {
      try {
        const response = await fetch(`${API_BASE_URL}/muscle-groups/`)
        if (!response.ok) {
          throw new Error('Failed to load muscle groups.')
        }
        const data = await response.json()
        setMuscleGroups(data)
      } catch (fetchError) {
        setError(fetchError.message)
      }
    }

    loadMuscleGroups()
  }, [])

  function toggleGroup(groupKey) {
    setSelectedGroups((current) =>
      current.includes(groupKey)
        ? current.filter((item) => item !== groupKey)
        : [...current, groupKey]
    )
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)

    if (selectedGroups.length === 0) {
      setError('Select at least one muscle group.')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/workouts/generate/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          muscle_groups: selectedGroups,
          target_duration_minutes: Number(duration),
        }),
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Could not generate workout.')
      }
      setResult(data)
    } catch (submitError) {
      setError(submitError.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <div className="hero-copy">
          <h1>Adaptive session builder</h1>
          <div className="hero-instruction">
            <p className="eyebrow">Instruction</p>
            <p className="hero-text">
              Pick the muscle groups you want to train, set your available
              time, and the app builds a sequence that starts easy, hits hard,
              and fills remaining space with medium effort work.
            </p>
          </div>
        </div>
        <button
          type="button"
          className="theme-toggle"
          onClick={() => setTheme((current) => (current === 'dark' ? 'light' : 'dark'))}
        >
          Switch to {theme === 'dark' ? 'light' : 'dark'} theme
        </button>
      </section>

      <section className="planner-grid">
        <form className="planner-card" onSubmit={handleSubmit}>
          <div className="section-heading">
            <p className="section-label">Build request</p>
            <h2>Workout inputs</h2>
          </div>

          <div className="group-grid">
            {muscleGroups.map((group) => (
              <button
                key={group.key}
                type="button"
                className={`muscle-chip ${selectedGroups.includes(group.key) ? 'selected' : ''}`}
                onClick={() => toggleGroup(group.key)}
              >
                {group.label}
              </button>
            ))}
          </div>

          <label className="duration-field">
            <span>Target duration</span>
            <div className="duration-input">
              <input
                type="number"
                min="5"
                max="180"
                value={duration}
                onChange={(event) => setDuration(event.target.value)}
              />
              <span>minutes</span>
            </div>
          </label>

          <button className="submit-button" type="submit" disabled={loading}>
            {loading ? 'Building workout...' : 'Generate workout'}
          </button>

          {error ? <p className="status-message error">{error}</p> : null}
        </form>

        <section className="result-card">
          <div className="section-heading">
            <p className="section-label">Generated session</p>
            <h2>{result ? 'Workout plan' : 'Waiting for input'}</h2>
          </div>

          {result ? (
            <>
              <div className="result-summary">
                <div>
                  <span className="summary-label">Status</span>
                  <strong>{result.feasible ? 'Fits target' : 'Needs more time'}</strong>
                </div>
                <div>
                  <span className="summary-label">Planned time</span>
                  <strong>{result.total_duration_minutes} min</strong>
                </div>
                <div>
                  <span className="summary-label">Focus</span>
                  <strong>{result.muscle_groups.join(', ')}</strong>
                </div>
              </div>

              {result.message ? (
                <p className="status-message warning">
                  {result.message} Minimum: {result.minimum_duration_minutes} min.
                </p>
              ) : null}

              <ol className="exercise-list">
                {result.items.map((item) => (
                  <li key={`${item.order}-${item.exercise_name}`} className="exercise-item">
                    <div>
                      <p className="exercise-name">{item.exercise_name}</p>
                      <p className="exercise-meta">
                        {item.muscle_group} · {item.difficulty}
                      </p>
                    </div>
                    <div className="exercise-times">
                      <span>{item.duration_seconds}s work</span>
                      <span>{item.rest_seconds}s rest</span>
                    </div>
                  </li>
                ))}
              </ol>
            </>
          ) : (
            <p className="empty-state">
              Generate a session to see the ordered exercise list, timing, and
              any minimum-duration guidance.
            </p>
          )}
        </section>
      </section>
    </main>
  )
}

export default App

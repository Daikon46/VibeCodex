import React, { useEffect, useRef, useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const THEME_STORAGE_KEY = 'workout-planner-theme'
const LANGUAGE_STORAGE_KEY = 'workout-planner-language'
const DEFAULT_LANGUAGE = 'en'

const languages = [
  { key: 'en', flag: '🇬🇧', abbr: 'EN' },
  { key: 'ru', flag: '🇷🇺', abbr: 'RU' },
  { key: 'zh', flag: '🇨🇳', abbr: 'ZH' },
]

const translations = {
  ru: {
    title: 'Адаптивный конструктор тренировок',
    instructionLabel: 'Инструкция',
    instructionText:
      'Выберите группы мышц, которые хотите тренировать, укажите доступное время, и приложение соберет последовательность с легким стартом, интенсивным пиком и средними упражнениями на оставшееся время.',
    buildRequest: 'Параметры запроса',
    workoutInputs: 'Параметры тренировки',
    targetDuration: 'Длительность',
    minutes: 'минут',
    generateWorkout: 'Сгенерировать тренировку',
    buildingWorkout: 'Собираем тренировку...',
    generatedSession: 'Сгенерированная сессия',
    workoutPlan: 'План тренировки',
    waitingForInput: 'Ожидание параметров',
    status: 'Статус',
    fitsTarget: 'Укладывается во время',
    needsMoreTime: 'Нужно больше времени',
    plannedTime: 'Длительность',
    focus: 'Фокус',
    minimum: 'Минимум',
    work: 'работа',
    rest: 'отдых',
    emptyState:
      'Сгенерируйте сессию, чтобы увидеть порядок упражнений, тайминг и подсказку по минимальной длительности.',
    selectMuscleGroup: 'Выберите хотя бы одну группу мышц.',
    failedToLoadMuscleGroups: 'Не удалось загрузить группы мышц.',
    couldNotGenerateWorkout: 'Не удалось сгенерировать тренировку.',
    switchToLightTheme: 'Переключить на светлую тему',
    switchToDarkTheme: 'Переключить на тёмную тему',
    language: 'Язык',
    muscleGroups: {
      chest: 'Грудь',
      back: 'Спина',
      shoulders: 'Плечи',
      hands: 'Руки',
      legs: 'Ноги',
    },
    difficulties: {
      easy: 'легко',
      medium: 'средне',
      hard: 'сложно',
    },
    apiMessages: {
      'No exercises are available for the selected muscle groups.':
        'Для выбранных групп мышц нет доступных упражнений.',
      'The selected duration is too short. Use the minimum duration shown to keep the easy-then-hard pattern.':
        'Выбранное время слишком короткое. Используйте указанную минимальную длительность, чтобы сохранить схему от легкого к сложному.',
      'Not enough exercise data to create a valid workout. Add at least one easy and one hard exercise.':
        'Недостаточно упражнений для построения корректной тренировки. Добавьте хотя бы одно легкое и одно сложное упражнение.',
    },
  },
  en: {
    title: 'Adaptive session builder',
    instructionLabel: 'Instruction',
    instructionText:
      'Pick the muscle groups you want to train, set your available time, and the app builds a sequence that starts easy, hits hard, and fills remaining space with medium effort work.',
    buildRequest: 'Build request',
    workoutInputs: 'Workout inputs',
    targetDuration: 'Target duration',
    minutes: 'minutes',
    generateWorkout: 'Generate workout',
    buildingWorkout: 'Building workout...',
    generatedSession: 'Generated session',
    workoutPlan: 'Workout plan',
    waitingForInput: 'Waiting for input',
    status: 'Status',
    fitsTarget: 'Fits target',
    needsMoreTime: 'Needs more time',
    plannedTime: 'Planned time',
    focus: 'Focus',
    minimum: 'Minimum',
    work: 'work',
    rest: 'rest',
    emptyState:
      'Generate a session to see the ordered exercise list, timing, and any minimum-duration guidance.',
    selectMuscleGroup: 'Select at least one muscle group.',
    failedToLoadMuscleGroups: 'Failed to load muscle groups.',
    couldNotGenerateWorkout: 'Could not generate workout.',
    switchToLightTheme: 'Switch to light theme',
    switchToDarkTheme: 'Switch to dark theme',
    language: 'Language',
    muscleGroups: {
      chest: 'Chest',
      back: 'Back',
      shoulders: 'Shoulders',
      hands: 'Hands',
      legs: 'Legs',
    },
    difficulties: {
      easy: 'easy',
      medium: 'medium',
      hard: 'hard',
    },
    apiMessages: {
      'No exercises are available for the selected muscle groups.':
        'No exercises are available for the selected muscle groups.',
      'The selected duration is too short. Use the minimum duration shown to keep the easy-then-hard pattern.':
        'The selected duration is too short. Use the minimum duration shown to keep the easy-then-hard pattern.',
      'Not enough exercise data to create a valid workout. Add at least one easy and one hard exercise.':
        'Not enough exercise data to create a valid workout. Add at least one easy and one hard exercise.',
    },
  },
  zh: {
    title: '自适应训练计划生成器',
    instructionLabel: '使用说明',
    instructionText:
      '选择你想训练的肌群，设置可用时间，应用会生成一个先轻后强、并用中等强度动作补足剩余时间的训练序列。',
    buildRequest: '创建请求',
    workoutInputs: '训练参数',
    targetDuration: '目标时长',
    minutes: '分钟',
    generateWorkout: '生成训练计划',
    buildingWorkout: '正在生成训练计划...',
    generatedSession: '已生成的训练',
    workoutPlan: '训练计划',
    waitingForInput: '等待输入',
    status: '状态',
    fitsTarget: '符合目标时长',
    needsMoreTime: '需要更多时间',
    plannedTime: '计划时长',
    focus: '重点肌群',
    minimum: '最少',
    work: '训练',
    rest: '休息',
    emptyState:
      '生成训练后，这里会显示动作顺序、时间安排以及最短时长提示。',
    selectMuscleGroup: '请至少选择一个肌群。',
    failedToLoadMuscleGroups: '无法加载肌群列表。',
    couldNotGenerateWorkout: '无法生成训练计划。',
    switchToLightTheme: '切换到浅色主题',
    switchToDarkTheme: '切换到深色主题',
    language: '语言',
    muscleGroups: {
      chest: '胸部',
      back: '背部',
      shoulders: '肩部',
      hands: '手臂',
      legs: '腿部',
    },
    difficulties: {
      easy: '简单',
      medium: '中等',
      hard: '困难',
    },
    apiMessages: {
      'No exercises are available for the selected muscle groups.':
        '所选肌群没有可用的训练动作。',
      'The selected duration is too short. Use the minimum duration shown to keep the easy-then-hard pattern.':
        '所选时间太短。请使用显示的最短时长以保持先易后难的节奏。',
      'Not enough exercise data to create a valid workout. Add at least one easy and one hard exercise.':
        '训练数据不足，无法生成有效计划。请至少添加一个简单动作和一个高难度动作。',
    },
  },
}

function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem(THEME_STORAGE_KEY) || 'dark')
  const [language, setLanguage] = useState(
    () => localStorage.getItem(LANGUAGE_STORAGE_KEY) || DEFAULT_LANGUAGE
  )
  const [languageMenuOpen, setLanguageMenuOpen] = useState(false)
  const [muscleGroups, setMuscleGroups] = useState([])
  const [selectedGroups, setSelectedGroups] = useState([])
  const [duration, setDuration] = useState(30)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const languageMenuRef = useRef(null)
  const t = translations[language]
  const currentLanguage = languages.find((item) => item.key === language) || languages[0]

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  }, [theme])

  useEffect(() => {
    localStorage.setItem(LANGUAGE_STORAGE_KEY, language)
  }, [language])

  useEffect(() => {
    function handleClickOutside(event) {
      if (languageMenuRef.current && !languageMenuRef.current.contains(event.target)) {
        setLanguageMenuOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  useEffect(() => {
    async function loadMuscleGroups() {
      try {
        const response = await fetch(`${API_BASE_URL}/muscle-groups/`)
        if (!response.ok) {
          throw new Error(t.failedToLoadMuscleGroups)
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

  function translateMuscleGroup(groupKey, fallbackLabel = groupKey) {
    return t.muscleGroups[groupKey] || fallbackLabel
  }

  function translateDifficulty(difficultyKey) {
    return t.difficulties[difficultyKey] || difficultyKey
  }

  function translateApiMessage(message) {
    return t.apiMessages[message] || message
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setResult(null)

    if (selectedGroups.length === 0) {
      setError(t.selectMuscleGroup)
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
        throw new Error(translateApiMessage(data.detail || t.couldNotGenerateWorkout))
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
          <h1>{t.title}</h1>
          <div className="hero-instruction">
            <p className="eyebrow">{t.instructionLabel}</p>
            <p className="hero-text">{t.instructionText}</p>
          </div>
        </div>

        <div className="hero-controls">
          <div className="language-menu" ref={languageMenuRef}>
            <button
              type="button"
              className="language-toggle"
              aria-haspopup="menu"
              aria-expanded={languageMenuOpen}
              aria-label={t.language}
              onClick={() => setLanguageMenuOpen((current) => !current)}
            >
              <span>{currentLanguage.flag}</span>
              <span>{currentLanguage.abbr}</span>
            </button>

            {languageMenuOpen ? (
              <div className="language-dropdown" role="menu" aria-label={t.language}>
                {languages.map((item) => (
                  <button
                    key={item.key}
                    type="button"
                    className={`language-option ${item.key === language ? 'active' : ''}`}
                    onClick={() => {
                      setLanguage(item.key)
                      setLanguageMenuOpen(false)
                    }}
                  >
                    <span>{item.flag}</span>
                    <span>{item.abbr}</span>
                  </button>
                ))}
              </div>
            ) : null}
          </div>

          <button
            type="button"
            className="theme-toggle"
            onClick={() => setTheme((current) => (current === 'dark' ? 'light' : 'dark'))}
          >
            {theme === 'dark' ? t.switchToLightTheme : t.switchToDarkTheme}
          </button>
        </div>
      </section>

      <section className="planner-grid">
        <form className="planner-card" onSubmit={handleSubmit}>
          <div className="section-heading">
            <p className="section-label">{t.buildRequest}</p>
            <h2>{t.workoutInputs}</h2>
          </div>

          <div className="group-grid">
            {muscleGroups.map((group) => (
              <button
                key={group.key}
                type="button"
                className={`muscle-chip ${selectedGroups.includes(group.key) ? 'selected' : ''}`}
                onClick={() => toggleGroup(group.key)}
              >
                {translateMuscleGroup(group.key, group.label)}
              </button>
            ))}
          </div>

          <label className="duration-field">
            <span>{t.targetDuration}</span>
            <div className="duration-input">
              <input
                type="number"
                min="5"
                max="180"
                value={duration}
                onChange={(event) => setDuration(event.target.value)}
              />
              <span>{t.minutes}</span>
            </div>
          </label>

          <button className="submit-button" type="submit" disabled={loading}>
            {loading ? t.buildingWorkout : t.generateWorkout}
          </button>

          {error ? <p className="status-message error">{error}</p> : null}
        </form>

        <section className="result-card">
          <div className="section-heading">
            <p className="section-label">{t.generatedSession}</p>
            <h2>{result ? t.workoutPlan : t.waitingForInput}</h2>
          </div>

          {result ? (
            <>
              <div className="result-summary">
                <div>
                  <span className="summary-label">{t.status}</span>
                  <strong>{result.feasible ? t.fitsTarget : t.needsMoreTime}</strong>
                </div>
                <div>
                  <span className="summary-label">{t.plannedTime}</span>
                  <strong>
                    {result.total_duration_minutes} {t.minutes}
                  </strong>
                </div>
                <div>
                  <span className="summary-label">{t.focus}</span>
                  <strong>
                    {result.muscle_groups.map((group) => translateMuscleGroup(group)).join(', ')}
                  </strong>
                </div>
              </div>

              {result.message ? (
                <p className="status-message warning">
                  {translateApiMessage(result.message)} {t.minimum}: {result.minimum_duration_minutes}{' '}
                  {t.minutes}.
                </p>
              ) : null}

              <ol className="exercise-list">
                {result.items.map((item) => (
                  <li key={`${item.order}-${item.exercise_name}`} className="exercise-item">
                    <div>
                      <p className="exercise-name">{item.exercise_name}</p>
                      <p className="exercise-meta">
                        {translateMuscleGroup(item.muscle_group)} ·{' '}
                        {translateDifficulty(item.difficulty)}
                      </p>
                    </div>
                    <div className="exercise-times">
                      <span>
                        {item.duration_seconds}s {t.work}
                      </span>
                      <span>
                        {item.rest_seconds}s {t.rest}
                      </span>
                    </div>
                  </li>
                ))}
              </ol>
            </>
          ) : (
            <p className="empty-state">{t.emptyState}</p>
          )}
        </section>
      </section>
    </main>
  )
}

export default App

import './App.css'
import { Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'

import HomePage from './pages/HomePage'
import SettingsPage from './pages/SettingsPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProtectedLayout from './layouts/ProtectedLayout'
import apiFetch from './lib/api'


function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)

  // useEffect gets called once (deps = []) right after the dom finished rendering but
  // before being presented to the user; i.e. it's called the first time the user tries to
  // reach the app, not every time they refresh the page
  useEffect(() => {
    (async () => {
      // get user object from response json
      const response = await apiFetch('/auth/me')
      // assign user object to session state
      setSession(response.ok ? await response.json() : null)
      // set loading to false so we can render the app
      setLoading(false)
    })()
  }, [])

  // called by LoginPage after a successful login, so App's session state reflects it
  async function refreshSession() {
    const response = await apiFetch('/auth/me')
    setSession(response.ok ? await response.json() : null)
  }

  if (loading) return null

  return (
    <Routes>
      <Route element={<ProtectedLayout session={session} onLogout={() => setSession(null)} />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>

      <Route path="/login" element={<LoginPage onLoginSuccess={refreshSession} />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  )
}

export default App

import './App.css'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'

import HomePage from './pages/HomePage'
import SettingsPage from './pages/SettingsPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import apiFetch from './lib/api'


function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const location = useLocation()

  // AUTH FLOW: check for an existing session once, when the app first loads

  useEffect(() => {
    apiFetch('/auth/me')
      // get user object from response json
      .then((response) => (response.ok ? response.json() : null))
      // assign user object to session state
      .then(setSession)
      // set loading to false so we can render the app
      .finally(() => setLoading(false))
  }, [])

  // called by LoginPage after a successful login, so App's session state reflects it
  async function refreshSession() {
    const response = await apiFetch('/auth/me')
    setSession(response.ok ? await response.json() : null)
  }

  if (loading) return null

  return (
    <Routes>
      <Route
        path="/"
        element={session ? <HomePage /> : <Navigate to="/login" replace state={{ from: location }} />}
      />
      <Route
        path="/settings"
        element={session ? <SettingsPage /> : <Navigate to="/login" replace state={{ from: location }} />}
      />
      <Route path="/login" element={<LoginPage onLoginSuccess={refreshSession} />} />
      <Route path="/register" element={<RegisterPage />} />
    </Routes>
  )
}

export default App

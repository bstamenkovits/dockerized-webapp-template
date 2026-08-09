import './App.css'
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'

import HomePage from './pages/HomePage'
import SettingsPage from './pages/SettingsPage'
import LoginPage from './pages/LoginPage'


function App() {
  const [session, setSession] = useState({})

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
      <Route path="/login" element={<LoginPage />} />
    </Routes>
  )
}

export default App

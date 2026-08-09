import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import apiFetch from '../lib/api'

function LoginPage({ onLoginSuccess = () => {} }) {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()
    const location = useLocation()

    async function handleSubmit(event) {
        event.preventDefault()
        setError('')

        const response = await apiFetch('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password }),
        })

        if (!response.ok) {
            setError('Invalid email or password.')
            return
        }

        // in App.jsx this function is assigned to a refresh of session state
        await onLoginSuccess()
        // navigate to page user was trying to access before login redirect
        navigate(location.state?.from?.pathname ?? '/', { replace: true })
    }

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="email">Email</label>
                <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                />

                <label htmlFor="password">Password</label>
                <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                />

                <button type="submit">Log in</button>
            </form>
            {error && <p role="alert">{error}</p>}
            <p>
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </div>
    )
}

export default LoginPage

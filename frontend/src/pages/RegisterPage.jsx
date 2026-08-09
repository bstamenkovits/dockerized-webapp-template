import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import apiFetch from '../lib/api'

function RegisterPage() {
    const [displayName, setDisplayName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()

    async function handleSubmit(event) {
        event.preventDefault()
        setError('')

        const response = await apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ display_name: displayName, email, password }),
        })

        if (!response.ok) {
            setError('Could not create account. Email may already be registered.')
            return
        }

        // registering does not start a session, so send the user to log in
        navigate('/login', { replace: true })
    }

    return (
        <div>
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="displayName">Display name</label>
                <input
                    id="displayName"
                    type="text"
                    value={displayName}
                    onChange={(event) => setDisplayName(event.target.value)}
                    required
                />

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

                <button type="submit">Create account</button>
            </form>
            {error && <p role="alert">{error}</p>}
            <p>
                Already have an account? <Link to="/login">Log in</Link>
            </p>
        </div>
    )
}

export default RegisterPage

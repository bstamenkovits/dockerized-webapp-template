import { Link, useNavigate } from 'react-router-dom'
import apiFetch from '../lib/api'
import './Nav.css'


function Nav({ onLogout = () => {} }) {
    const navigate = useNavigate()

    async function handleLogout() {
        await apiFetch('/auth/logout', { method: 'POST' })
        onLogout()
        navigate('/login', { replace: true })
    }

    return (
        <nav>
            <Link to="/">Home</Link>
            <Link to="/settings">Settings</Link>
            <button type="button" onClick={handleLogout}>Log out</button>
        </nav>
    )
}

export default Nav
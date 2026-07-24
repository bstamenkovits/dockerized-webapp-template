import { Link } from 'react-router-dom'
import './Nav.css'


function Nav() {
    return (
        <nav>
            <Link to="/">Home</Link>
            <Link to="/settings">Settings</Link>
        </nav>
    )
}

export default Nav
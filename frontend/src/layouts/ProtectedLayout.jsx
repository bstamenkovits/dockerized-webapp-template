import { Navigate, Outlet, useLocation } from 'react-router-dom'
import Nav from '../components/Nav'

function ProtectedLayout({ session, onLogout }) {
    const location = useLocation()

    if (!session) {
        return <Navigate to="/login" replace state={{ from: location }} />
    }

    return (
        <div>
            <Nav onLogout={onLogout} />
            <Outlet />
        </div>
    )
}

export default ProtectedLayout

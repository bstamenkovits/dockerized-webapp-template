import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
import ProtectedLayout from './ProtectedLayout'

function LoginStub() {
    const location = useLocation()
    return <h1>Login (from {location.state?.from?.pathname ?? 'nowhere'})</h1>
}

function renderAt(path, session) {
    render(
        <MemoryRouter initialEntries={[path]}>
            <Routes>
                <Route element={<ProtectedLayout session={session} />}>
                    <Route path="/settings" element={<h1>Settings</h1>} />
                </Route>
                <Route path="/login" element={<LoginStub />} />
            </Routes>
        </MemoryRouter>
    )
}

test('redirects to /login, remembering the page that was requested', () => {
    renderAt('/settings', null)

    expect(screen.getByRole('heading', { name: 'Login (from /settings)' })).toBeInTheDocument()
})

test('renders Nav and the requested page when authenticated', () => {
    renderAt('/settings', { id: 1, email: 'user@example.com' })

    expect(screen.getByRole('heading', { name: 'Settings' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Home' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Settings' })).toBeInTheDocument()
})

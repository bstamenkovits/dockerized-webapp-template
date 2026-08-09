import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi } from 'vitest'
import LoginPage from './LoginPage'

function fillAndSubmit() {
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Log in' }))
}

test('renders the login form', () => {
    render(<LoginPage />, { wrapper: MemoryRouter })

    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument()
})

test('submits credentials to POST /api/auth/login', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })
    render(<LoginPage />, { wrapper: MemoryRouter })

    fillAndSubmit()

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/auth/login', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'user@example.com', password: 'password123' }),
    })))
})

test('shows an error message when login fails', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false })
    render(<LoginPage />, { wrapper: MemoryRouter })

    fillAndSubmit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password.')
})

test('awaits onLoginSuccess before navigating away', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })
    const onLoginSuccess = vi.fn().mockResolvedValue()
    render(<LoginPage onLoginSuccess={onLoginSuccess} />, { wrapper: MemoryRouter })

    fillAndSubmit()

    await waitFor(() => expect(onLoginSuccess).toHaveBeenCalled())
})

test('redirects back to the originally requested page after login', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })

    render(
        <MemoryRouter initialEntries={[{ pathname: '/login', state: { from: { pathname: '/settings' } } }]}>
            <Routes>
                <Route path="/login" element={<LoginPage />} />
                <Route path="/settings" element={<h1>Settings</h1>} />
            </Routes>
        </MemoryRouter>
    )

    fillAndSubmit()

    expect(await screen.findByRole('heading', { name: 'Settings' })).toBeInTheDocument()
})

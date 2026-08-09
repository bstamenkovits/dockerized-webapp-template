import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { vi } from 'vitest'
import App from './App'

test('redirects to /login when the session check fails', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false })

    render(
        <MemoryRouter initialEntries={['/']}>
            <App />
        </MemoryRouter>
    )

    expect(await screen.findByRole('heading', { name: 'Login' })).toBeInTheDocument()
})

test('renders the requested page when the session check succeeds', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ id: 1, email: 'user@example.com' }) })

    render(
        <MemoryRouter initialEntries={['/']}>
            <App />
        </MemoryRouter>
    )

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/auth/me', expect.objectContaining({ credentials: 'include' })))
    expect(await screen.findByRole('heading', { name: 'Home' })).toBeInTheDocument()
})

test('lands on the originally requested page after logging in', async () => {
    global.fetch = vi.fn().mockImplementation((url) => {
        if (url === '/api/auth/me') {
            // unauthenticated on first load, authenticated once refreshSession runs after login
            const authenticated = global.fetch.mock.calls.filter((call) => call[0] === '/api/auth/me').length > 1
            return Promise.resolve({ ok: authenticated, json: async () => ({ id: 1, email: 'user@example.com' }) })
        }
        return Promise.resolve({ ok: true })
    })

    render(
        <MemoryRouter initialEntries={['/settings']}>
            <App />
        </MemoryRouter>
    )

    expect(await screen.findByRole('heading', { name: 'Login' })).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Log in' }))

    expect(await screen.findByRole('heading', { name: 'Settings' })).toBeInTheDocument()
})

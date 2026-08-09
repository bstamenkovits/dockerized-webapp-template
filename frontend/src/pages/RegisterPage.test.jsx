import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { vi } from 'vitest'
import RegisterPage from './RegisterPage'

function fillAndSubmit() {
    fireEvent.change(screen.getByLabelText('Display name'), { target: { value: 'New User' } })
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create account' }))
}

test('renders the register form', () => {
    render(<RegisterPage />, { wrapper: MemoryRouter })

    expect(screen.getByLabelText('Display name')).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Create account' })).toBeInTheDocument()
})

test('submits details to POST /api/auth/register', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })
    render(<RegisterPage />, { wrapper: MemoryRouter })

    fillAndSubmit()

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/auth/register', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ display_name: 'New User', email: 'user@example.com', password: 'password123' }),
    })))
})

test('shows an error message when registration fails', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false })
    render(<RegisterPage />, { wrapper: MemoryRouter })

    fillAndSubmit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Could not create account. Email may already be registered.')
})

test('redirects to /login after successful registration', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })

    render(
        <MemoryRouter initialEntries={['/register']}>
            <Routes>
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/login" element={<h1>Login</h1>} />
            </Routes>
        </MemoryRouter>
    )

    fillAndSubmit()

    expect(await screen.findByRole('heading', { name: 'Login' })).toBeInTheDocument()
})

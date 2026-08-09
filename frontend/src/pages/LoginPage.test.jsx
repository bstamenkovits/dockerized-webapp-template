import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import LoginPage from './LoginPage'

function fillAndSubmit() {
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } })
    fireEvent.click(screen.getByRole('button', { name: 'Log in' }))
}

test('renders the login form', () => {
    render(<LoginPage />)

    expect(screen.getByLabelText('Email')).toBeInTheDocument()
    expect(screen.getByLabelText('Password')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Log in' })).toBeInTheDocument()
})

test('submits credentials to POST /api/auth/login', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })
    render(<LoginPage />)

    fillAndSubmit()

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/auth/login', expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ email: 'user@example.com', password: 'password123' }),
    })))
})

test('shows an error message when login fails', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false })
    render(<LoginPage />)

    fillAndSubmit()

    expect(await screen.findByRole('alert')).toHaveTextContent('Invalid email or password.')
})

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Nav from './Nav'

test('renders links to Home and Settings', () => {
    render(
        <MemoryRouter>
            <Nav />
        </MemoryRouter>
    )

    expect(screen.getByRole('link', { name: 'Home' })).toHaveAttribute('href', '/')
    expect(screen.getByRole('link', { name: 'Settings' })).toHaveAttribute('href', '/settings')
})

test('logging out calls the logout endpoint and onLogout', async () => {
    const onLogout = vi.fn()
    global.fetch = vi.fn().mockResolvedValue({ ok: true })

    render(
        <MemoryRouter>
            <Nav onLogout={onLogout} />
        </MemoryRouter>
    )

    fireEvent.click(screen.getByRole('button', { name: 'Log out' }))

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith('/api/auth/logout', expect.objectContaining({ method: 'POST' })))
    expect(onLogout).toHaveBeenCalled()
})

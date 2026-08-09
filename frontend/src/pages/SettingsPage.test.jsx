import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import SettingsPage from './SettingsPage'

test('renders the Settings heading', () => {
    render(
        <MemoryRouter>
            <SettingsPage />
        </MemoryRouter>
    )

    expect(screen.getByRole('heading', { name: 'Settings' })).toBeInTheDocument()
})

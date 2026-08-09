import { vi } from 'vitest'
import apiFetch from './api'

test('prefixes the path with /api and includes credentials', () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true })

    apiFetch('/auth/login', { method: 'POST', body: JSON.stringify({ email: 'a@b.com' }) })

    expect(global.fetch).toHaveBeenCalledWith('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: 'a@b.com' }),
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
    })
})

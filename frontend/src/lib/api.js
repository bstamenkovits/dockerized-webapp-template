/** Centralizes `credentials: 'include'` so callers can't forget to send the session cookie. */
function apiFetch(path, options = {}) {
    return fetch(`/api${path}`, {
        ...options,
        credentials: 'include',
        headers: { 'Content-Type': 'application/json', ...options.headers },
    })
}

export default apiFetch

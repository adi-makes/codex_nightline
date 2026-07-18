export type GroundedAnswer = {
  answer: string
  evidence_status: 'source_metadata_present' | 'insufficient_evidence'
  generation_mode: 'gemini_general' | 'abstained'
  citations: Record<string, unknown>[]
  suggested_followups: string[]
  request_id: string
}

export class ApiError extends Error {
  constructor(public readonly status: number, message: string) {
    super(message)
  }
}

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '/api/v1').replace(/\/$/, '')

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  headers.set('Accept', 'application/json')
  if (init.body) headers.set('Content-Type', 'application/json')

  let response: Response
  try {
    response = await fetch(`${apiBaseUrl}${path}`, { ...init, headers })
  } catch {
    throw new ApiError(0, 'Ask Kochi is unavailable. Check that the API is running and try again.')
  }

  if (!response.ok) {
    const payload = await response.json().catch(() => null) as { detail?: string } | null
    throw new ApiError(response.status, payload?.detail || 'Something went wrong. Please try again.')
  }
  return response.json() as Promise<T>
}

export const api = {
  chat: (query: string) => request<GroundedAnswer>('/chat', {
    method: 'POST',
    body: JSON.stringify({ query }),
  }),
}

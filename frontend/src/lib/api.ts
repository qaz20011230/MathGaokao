const API_BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

async function requestForm<T>(path: string, formData: FormData, method: 'POST' | 'PUT' = 'POST'): Promise<T> {
  const token = localStorage.getItem('admin_token')
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: formData,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '请求失败' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export interface DocumentListItem {
  id: number
  title: string
  year: number
  period: string
  doc_type: string
  province: string | null
  exam_category: string | null
  file_format: string
  page_count: number | null
  file_size: number
  view_count: number
  created_at: string
}

export interface DocumentDetail extends DocumentListItem {
  description: string | null
  source: string | null
  year_title: string | null
  file_md5: string | null
  download_count: number
  updated_at: string
}

export interface DocumentListOut {
  total: number
  items: DocumentListItem[]
  page: number
  page_size: number
}

export interface YearStat {
  year: number
  count: number
}

export interface ProvinceStat {
  province: string
  count: number
}

export interface StatsOut {
  total_documents: number
  total_size_bytes: number
  years_covered: number[]
  periods: Record<string, number>
  doc_types: Record<string, number>
}

export interface TokenOut {
  access_token: string
  token_type: string
}

export interface DocumentFilter {
  page?: number
  page_size?: number
  year?: number
  period?: string
  doc_type?: string
  province?: string
  exam_category?: string
  search?: string
}

function buildQuery(params: Record<string, string | number | undefined>): string {
  const parts: string[] = []
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '' && v !== null) {
      parts.push(`${k}=${encodeURIComponent(String(v))}`)
    }
  }
  return parts.length ? '?' + parts.join('&') : ''
}

export const api = {
  getStats: () => request<StatsOut>('/stats'),
  getYears: () => request<YearStat[]>('/years'),
  getProvinces: () => request<ProvinceStat[]>('/provinces'),

  getDocuments: (filter: DocumentFilter) =>
    request<DocumentListOut>(`/documents${buildQuery(filter as Record<string, string | number | undefined>)}`),

  getDocument: (id: number) => request<DocumentDetail>(`/documents/${id}`),

  getViewUrl: (id: number) => `${API_BASE}/documents/${id}/view`,

  adminLogin: (username: string, password: string) =>
    request<TokenOut>('/admin/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),

  checkAuth: (token: string) =>
    request<{ authenticated: boolean }>('/admin/auth/check', {
      headers: { Authorization: `Bearer ${token}` },
    }),

  adminGetDocuments: (page = 1, pageSize = 50) =>
    request<DocumentListOut>(`/admin/documents?page=${page}&page_size=${pageSize}`),

  createDocument: (formData: FormData) =>
    requestForm<DocumentDetail>('/admin/documents', formData, 'POST'),

  updateDocument: (id: number, data: Record<string, unknown>, token: string) =>
    request<DocumentDetail>(`/admin/documents/${id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(data),
    }),

  deleteDocument: (id: number, token: string) =>
    request<{ detail: string }>(`/admin/documents/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    }),

  getDownloadUrl: (id: number) => `${API_BASE}/admin/documents/${id}/download`,
}

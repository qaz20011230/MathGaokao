'use client'

import { useEffect, useState, useCallback } from 'react'
import { api, DocumentListItem } from '@/lib/api'
import { docTypeLabel, categoryLabel, provinceLabel, periodLabel, formatFileSize, formatDate } from '@/lib/utils'

export default function AdminPage() {
  const [token, setToken] = useState<string | null>(null)
  const [authenticated, setAuthenticated] = useState(false)
  const [authLoading, setAuthLoading] = useState(true)

  useEffect(() => {
    const saved = localStorage.getItem('admin_token')
    if (saved) {
      setToken(saved)
      api.checkAuth(saved)
        .then(() => setAuthenticated(true))
        .catch(() => localStorage.removeItem('admin_token'))
        .finally(() => setAuthLoading(false))
    } else {
      setAuthLoading(false)
    }
  }, [])

  const handleLogin = async (username: string, password: string) => {
    const result = await api.adminLogin(username, password)
    localStorage.setItem('admin_token', result.access_token)
    setToken(result.access_token)
    setAuthenticated(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('admin_token')
    setToken(null)
    setAuthenticated(false)
  }

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-muted text-lg animate-pulse">加载中…</div>
      </div>
    )
  }

  if (!authenticated || !token) {
    return <LoginPage onLogin={handleLogin} />
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-serif font-bold text-ink">管理后台</h1>
          <p className="text-muted text-sm mt-1">文档上传、编辑与删除</p>
        </div>
        <button onClick={handleLogout} className="btn-secondary text-sm">
          退出登录
        </button>
      </div>

      <UploadSection token={token} />
      <hr className="my-10 border-border" />
      <DocumentListSection token={token} />
    </div>
  )
}

function LoginPage({ onLogin }: { onLogin: (u: string, p: string) => Promise<void> }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await onLogin(username, password)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : '登录失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto px-4 py-20">
      <div className="card p-8">
        <h1 className="text-2xl font-serif font-bold text-ink mb-2 text-center">管理员登录</h1>
        <p className="text-sm text-muted mb-8 text-center">mathgaokao.top 管理后台</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">用户名</label>
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              className="input-field"
              required
              autoComplete="username"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">密码</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="input-field"
              required
              autoComplete="current-password"
            />
          </div>
          {error && <p className="text-red-600 text-sm">{error}</p>}
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? '登录中…' : '登录'}
          </button>
        </form>
      </div>
    </div>
  )
}

function UploadSection({ token }: { token: string }) {
  const [title, setTitle] = useState('')
  const [year, setYear] = useState(new Date().getFullYear())
  const [period, setPeriod] = useState('1977_now')
  const [docType, setDocType] = useState('exam_paper')
  const [province, setProvince] = useState('')
  const [examCategory, setExamCategory] = useState('')
  const [description, setDescription] = useState('')
  const [source, setSource] = useState('')
  const [yearTitle, setYearTitle] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [collapsed, setCollapsed] = useState(false)

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) { setMessage('请选择文件'); return }
    setUploading(true)
    setMessage('')
    try {
      const fd = new FormData()
      fd.append('title', title)
      fd.append('year', String(year))
      fd.append('period', period)
      fd.append('doc_type', docType)
      if (province) fd.append('province', province)
      if (examCategory) fd.append('exam_category', examCategory)
      if (description) fd.append('description', description)
      if (source) fd.append('source', source)
      if (yearTitle) fd.append('year_title', yearTitle)
      fd.append('is_published', '1')
      fd.append('file', file)
      await api.createDocument(fd)
      setMessage('上传成功！')
      setTitle(''); setProvince(''); setExamCategory(''); setDescription(''); setSource(''); setYearTitle(''); setFile(null)
      setTimeout(() => setMessage(''), 3000)
    } catch (err: unknown) {
      setMessage(err instanceof Error ? err.message : '上传失败')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4 cursor-pointer" onClick={() => setCollapsed(!collapsed)}>
        <h2 className="font-serif font-bold text-lg text-ink">上传新文档</h2>
        <span className="text-muted text-sm">{collapsed ? '展开' : '收起'}</span>
      </div>
      {!collapsed && (
        <form onSubmit={handleUpload} className="space-y-4">
          <div className="grid sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">标题 *</label>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="input-field" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">年份 *</label>
              <input type="number" value={year} onChange={e => setYear(Number(e.target.value))} className="input-field" min={1905} max={2026} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">时期 *</label>
              <select value={period} onChange={e => setPeriod(e.target.value)} className="select-field">
                <option value="pre_1952">1905—1951</option>
                <option value="1952_1965">1952—1965</option>
                <option value="1977_now">1977—至今</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">文档类型 *</label>
              <select value={docType} onChange={e => setDocType(e.target.value)} className="select-field">
                <option value="exam_paper">试卷</option>
                <option value="answer_sheet">答题卡</option>
                <option value="answer_key">参考答案</option>
                <option value="other">其他文档</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">命题单位</label>
              <input type="text" value={province} onChange={e => setProvince(e.target.value)} className="input-field" placeholder="留空表示全国卷" />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">考试类别</label>
              <input type="text" value={examCategory} onChange={e => setExamCategory(e.target.value)} className="input-field" placeholder="理科/文科/新高考" />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">来源</label>
              <input type="text" value={source} onChange={e => setSource(e.target.value)} className="input-field" />
            </div>
            <div>
              <label className="block text-sm font-medium text-ink mb-1.5">补充信息</label>
              <input type="text" value={yearTitle} onChange={e => setYearTitle(e.target.value)} className="input-field" placeholder="早期资料的高校名等" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">描述</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="input-field" rows={2} />
          </div>
          <div>
            <label className="block text-sm font-medium text-ink mb-1.5">文件 *（PDF）</label>
            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={e => setFile(e.target.files?.[0] || null)}
              className="input-field"
              required={!file}
            />
            {file && <p className="text-xs text-muted mt-1">{file.name}（{formatFileSize(file.size)}）</p>}
          </div>
          {message && (
            <div className={`text-sm px-4 py-2 rounded ${message.includes('成功') ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600'}`}>
              {message}
            </div>
          )}
          <button type="submit" disabled={uploading} className="btn-primary">
            {uploading ? '上传中…' : '上传文档'}
          </button>
        </form>
      )}
    </div>
  )
}

function DocumentListSection({ token }: { token: string }) {
  const [docs, setDocs] = useState<DocumentListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState<number | null>(null)
  const [editForm, setEditForm] = useState<Record<string, string>>({})

  const fetchDocs = useCallback(() => {
    setLoading(true)
    fetch(`/api/admin/documents?page=${page}&page_size=30`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json())
      .then(data => { setDocs(data.items); setTotal(data.total) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [page, token])

  useEffect(() => { fetchDocs() }, [fetchDocs])

  const handleDelete = async (id: number) => {
    if (!confirm('确认删除此文档？此操作不可撤销。')) return
    try {
      await api.deleteDocument(id, token)
      fetchDocs()
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : '删除失败')
    }
  }

  const handleEdit = (doc: DocumentListItem) => {
    setEditing(doc.id)
    setEditForm({
      title: doc.title,
      year: String(doc.year),
      province: doc.province || '',
      exam_category: doc.exam_category || '',
    })
  }

  const handleSave = async (id: number) => {
    try {
      await api.updateDocument(id, {
        ...editForm,
        year: parseInt(editForm.year) || undefined,
      }, token)
      setEditing(null)
      fetchDocs()
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : '保存失败')
    }
  }

  const totalPages = Math.ceil(total / 30)

  return (
    <div>
      <h2 className="font-serif font-bold text-lg text-ink mb-4">文档列表 {total > 0 && <span className="text-muted text-sm font-normal">（{total}份）</span>}</h2>

      {loading ? (
        <div className="text-center py-12 text-muted animate-pulse">加载中…</div>
      ) : (
        <div className="space-y-2">
          {docs.map(doc => (
            <div key={doc.id} className="card p-4">
              {editing === doc.id ? (
                <div className="space-y-3">
                  <input type="text" value={editForm.title} onChange={e => setEditForm(f => ({ ...f, title: e.target.value }))} className="input-field" />
                  <div className="flex gap-3">
                    <input type="number" value={editForm.year} onChange={e => setEditForm(f => ({ ...f, year: e.target.value }))} className="input-field w-24" />
                    <input type="text" value={editForm.province} onChange={e => setEditForm(f => ({ ...f, province: e.target.value }))} className="input-field" placeholder="命题单位" />
                    <input type="text" value={editForm.exam_category} onChange={e => setEditForm(f => ({ ...f, exam_category: e.target.value }))} className="input-field w-28" placeholder="类别" />
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => handleSave(doc.id)} className="btn-primary text-sm px-3 py-1">保存</button>
                    <button onClick={() => setEditing(null)} className="btn-secondary text-sm px-3 py-1">取消</button>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-between gap-3">
                  <div className="min-w-0 flex-1">
                    <div className="font-serif font-bold text-ink text-sm truncate">{doc.title}</div>
                    <div className="flex gap-2 text-xs text-muted mt-1">
                      <span className="bg-accent/10 text-accent px-1.5 py-0.5 rounded">{doc.year}</span>
                      <span>{docTypeLabel(doc.doc_type)}</span>
                      <span>{categoryLabel(doc.exam_category)}</span>
                      <span>{provinceLabel(doc.province)}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <span className="text-xs text-muted">{doc.view_count}次</span>
                    <span className="text-xs text-muted">{formatFileSize(doc.file_size)}</span>
                    <button onClick={() => handleEdit(doc)} className="text-xs text-blue-600 hover:underline">编辑</button>
                    <a
                      href={api.getDownloadUrl(doc.id)}
                      className="text-xs text-green-600 hover:underline"
                      onClick={(e: React.MouseEvent) => {
                        const href = api.getDownloadUrl(doc.id)
                        fetch(href, { headers: { Authorization: `Bearer ${token}` } })
                          .then(r => r.blob())
                          .then(blob => {
                            const url = URL.createObjectURL(blob)
                            const a = document.createElement('a')
                            a.href = url; a.download = `${doc.title}.pdf`; a.click()
                            URL.revokeObjectURL(url)
                          })
                        e.preventDefault()
                      }}
                    >
                      下载
                    </a>
                    <button onClick={() => handleDelete(doc.id)} className="text-xs text-red-600 hover:underline">删除</button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 mt-6">
          <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page <= 1} className="btn-secondary px-3 py-1.5 text-sm">上一页</button>
          <span className="text-sm text-muted px-4">{page} / {totalPages}</span>
          <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page >= totalPages} className="btn-secondary px-3 py-1.5 text-sm">下一页</button>
        </div>
      )}
    </div>
  )
}

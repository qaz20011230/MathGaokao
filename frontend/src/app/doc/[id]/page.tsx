'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { api, DocumentDetail } from '@/lib/api'
import { docTypeLabel, categoryLabel, provinceLabel, periodLabel, formatDate, formatFileSize } from '@/lib/utils'

export default function DocumentPage() {
  const params = useParams()
  const id = Number(params.id)
  const [doc, setDoc] = useState<DocumentDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [viewerMode, setViewerMode] = useState<'viewer' | 'pdf'>('viewer')

  useEffect(() => {
    if (!id) return
    api.getDocument(id)
      .then(setDoc)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-muted text-lg animate-pulse">加载中…</div>
      </div>
    )
  }

  if (error || !doc) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <p className="text-lg text-muted mb-4">文档不存在或已被移除</p>
        <Link href="/browse" className="btn-primary">返回浏览</Link>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="bg-ink text-white px-4 py-2 flex items-center justify-between text-sm flex-shrink-0 border-b-4 border-accent">
        <div className="flex items-center gap-4">
          <Link href="/browse" className="text-gray-400 hover:text-white transition-colors">
            ← 返回
          </Link>
          <span className="font-serif font-bold truncate max-w-md">{doc.title}</span>
          <span className="text-gray-500 text-xs">{doc.year}</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewerMode('viewer')}
            className={`px-3 py-1 rounded text-xs ${viewerMode === 'viewer' ? 'bg-accent text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
          >
            图片模式
          </button>
          <button
            onClick={() => setViewerMode('pdf')}
            className={`px-3 py-1 rounded text-xs ${viewerMode === 'pdf' ? 'bg-accent text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
          >
            PDF 模式
          </button>
        </div>
      </div>

      {viewerMode === 'viewer' ? (
        <iframe
          src={`/api/documents/${doc.id}/viewer`}
          className="w-full flex-1 border-0"
          title={doc.title}
          sandbox="allow-scripts allow-same-origin"
        />
      ) : (
        <iframe
          src={api.getViewUrl(doc.id)}
          className="w-full flex-1 border-0"
          title={doc.title}
          sandbox="allow-scripts allow-same-origin"
        />
      )}
    </div>
  )
}

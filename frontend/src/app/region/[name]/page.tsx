'use client'

import { useEffect, useState } from 'react'
import { useParams, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { api, ProvinceStat, DocumentListItem } from '@/lib/api'
import { docTypeLabel, categoryLabel, periodLabel, formatDate, formatFileSize } from '@/lib/utils'

export default function RegionPage() {
  const params = useParams()
  const regionName = decodeURIComponent(params.name as string)

  const [documents, setDocuments] = useState<DocumentListItem[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)

  useEffect(() => {
    setLoading(true)
    api.getDocuments({ province: regionName, page, page_size: 50 })
      .then(data => {
        setDocuments(data.items)
        setTotal(data.total)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [regionName, page])

  const totalPages = Math.ceil(total / 50)

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <div className="mb-6">
        <Link href="/browse" className="text-sm text-muted hover:text-accent transition-colors">
          ← 返回浏览
        </Link>
      </div>

      <h1 className="text-3xl font-serif font-bold text-ink mb-2">{regionName}</h1>
      <p className="text-muted mb-8">共 {total} 份文档</p>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="text-muted text-lg animate-pulse">加载中…</div>
        </div>
      ) : documents.length === 0 ? (
        <div className="card p-16 text-center text-muted">
          <p className="text-lg mb-2">暂无文档</p>
          <p className="text-sm">该地区暂无已收录的文档</p>
        </div>
      ) : (
        <>
          <div className="space-y-3">
            {documents.map(doc => (
              <DocRow key={doc.id} doc={doc} />
            ))}
          </div>
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-8">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page <= 1}
                className="btn-secondary px-3 py-1.5 text-sm"
              >
                上一页
              </button>
              <span className="text-sm text-muted px-4">{page} / {totalPages}</span>
              <button
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages}
                className="btn-secondary px-3 py-1.5 text-sm"
              >
                下一页
              </button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

function DocRow({ doc }: { doc: DocumentListItem }) {
  return (
    <Link href={`/doc/${doc.id}`} className="card p-5 block group">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h3 className="font-serif font-bold text-ink group-hover:text-accent transition-colors leading-snug">
            {doc.title}
          </h3>
          <div className="flex flex-wrap gap-2 text-xs mt-2">
            <span className="bg-accent/10 text-accent px-2 py-0.5 rounded-full font-medium">{doc.year}</span>
            <span className="bg-gray-100 text-muted px-2 py-0.5 rounded-full">{docTypeLabel(doc.doc_type)}</span>
            {doc.exam_category && (
              <span className="bg-gray-100 text-muted px-2 py-0.5 rounded-full">{doc.exam_category}</span>
            )}
          </div>
        </div>
        <div className="flex-shrink-0 text-right text-xs text-muted space-y-1">
          <div>{formatFileSize(doc.file_size)}</div>
          <div>{doc.view_count} 次浏览</div>
        </div>
      </div>
    </Link>
  )
}

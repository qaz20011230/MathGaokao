'use client'

import { useEffect, useState, useCallback, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { api, DocumentListItem, YearStat, ProvinceStat, StatsOut } from '@/lib/api'
import { periodLabel, docTypeLabel, categoryLabel, provinceLabel, formatDate, formatFileSize } from '@/lib/utils'

export default function BrowsePage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-[60vh]"><div className="text-muted text-lg animate-pulse">加载中…</div></div>}>
      <BrowseContent />
    </Suspense>
  )
}

function BrowseContent() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const [documents, setDocuments] = useState<DocumentListItem[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [years, setYears] = useState<YearStat[]>([])
  const [provinces, setProvinces] = useState<ProvinceStat[]>([])

  const [filterYear, setFilterYear] = useState<number | undefined>()
  const [filterPeriod, setFilterPeriod] = useState<string | undefined>()
  const [filterDocType, setFilterDocType] = useState<string | undefined>()
  const [filterProvince, setFilterProvince] = useState<string | undefined>()
  const [filterCategory, setFilterCategory] = useState<string | undefined>()
  const [filterSearch, setFilterSearch] = useState<string | undefined>()

  useEffect(() => {
    Promise.all([api.getYears(), api.getProvinces()]).then(([y, p]) => {
      setYears(y); setProvinces(p)
    })
  }, [])

  useEffect(() => {
    setFilterYear(searchParams.get('year') ? Number(searchParams.get('year')) : undefined)
    setFilterSearch(searchParams.get('search') || undefined)
    setFilterPeriod(searchParams.get('period') || undefined)
    setFilterDocType(searchParams.get('doc_type') || undefined)
    setFilterProvince(searchParams.get('province') || undefined)
    setFilterCategory(searchParams.get('exam_category') || undefined)
  }, [searchParams])

  const fetchDocuments = useCallback(() => {
    setLoading(true)
    api.getDocuments({
      page, page_size: 50,
      year: filterYear, period: filterPeriod, doc_type: filterDocType,
      province: filterProvince, exam_category: filterCategory, search: filterSearch,
    }).then(data => {
      setDocuments(data.items)
      setTotal(data.total)
    }).catch(console.error).finally(() => setLoading(false))
  }, [page, filterYear, filterPeriod, filterDocType, filterProvince, filterCategory, filterSearch])

  useEffect(() => {
    fetchDocuments()
  }, [fetchDocuments])

  const totalPages = Math.ceil(total / 50)

  const clearFilters = () => {
    setFilterYear(undefined); setFilterPeriod(undefined); setFilterDocType(undefined)
    setFilterProvince(undefined); setFilterCategory(undefined); setFilterSearch(undefined)
    setPage(1)
  }

  const hasFilters = filterYear || filterPeriod || filterDocType || filterProvince || filterCategory || filterSearch

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-serif font-bold text-ink mb-2">浏览文档</h1>
      <p className="text-muted mb-8">按年份、时期、类型、地区筛选查看全部高考数学文档</p>

      <div className="flex flex-col md:flex-row gap-8">
        <aside className="w-full md:w-56 flex-shrink-0">
          <div className="md:sticky md:top-8 space-y-6">
            <div className="card p-4">
              <h3 className="font-serif font-bold text-sm mb-3 text-ink">年份</h3>
              <div className="max-h-64 overflow-y-auto space-y-0.5">
                <button
                  onClick={() => { setFilterYear(undefined); setPage(1) }}
                  className={`block w-full text-left px-2 py-1 rounded text-sm ${!filterYear ? 'bg-accent text-white' : 'hover:bg-gray-100'}`}
                >
                  全部年份
                </button>
                {years.map(y => (
                  <button
                    key={y.year}
                    onClick={() => { setFilterYear(y.year); setPage(1) }}
                    className={`block w-full text-left px-2 py-1 rounded text-sm flex justify-between ${filterYear === y.year ? 'bg-accent text-white' : 'hover:bg-gray-100'}`}
                  >
                    <span>{y.year}</span>
                    <span className="text-xs opacity-70">{y.count}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="card p-4">
              <h3 className="font-serif font-bold text-sm mb-3 text-ink">时期</h3>
              <div className="space-y-1">
                <FilterBtn label="全部时期" active={!filterPeriod} onClick={() => { setFilterPeriod(undefined); setPage(1) }} />
                <FilterBtn label="1905—1951" active={filterPeriod === 'pre_1952'} onClick={() => { setFilterPeriod('pre_1952'); setPage(1) }} />
                <FilterBtn label="1952—1965" active={filterPeriod === '1952_1965'} onClick={() => { setFilterPeriod('1952_1965'); setPage(1) }} />
                <FilterBtn label="1977—至今" active={filterPeriod === '1977_now'} onClick={() => { setFilterPeriod('1977_now'); setPage(1) }} />
              </div>
            </div>

            <div className="card p-4">
              <h3 className="font-serif font-bold text-sm mb-3 text-ink">文档类型</h3>
              <div className="space-y-1">
                <FilterBtn label="全部类型" active={!filterDocType} onClick={() => { setFilterDocType(undefined); setPage(1) }} />
                <FilterBtn label="试卷" active={filterDocType === 'exam_paper'} onClick={() => { setFilterDocType('exam_paper'); setPage(1) }} />
                <FilterBtn label="答题卡" active={filterDocType === 'answer_sheet'} onClick={() => { setFilterDocType('answer_sheet'); setPage(1) }} />
                <FilterBtn label="参考答案" active={filterDocType === 'answer_key'} onClick={() => { setFilterDocType('answer_key'); setPage(1) }} />
                <FilterBtn label="其他文档" active={filterDocType === 'other'} onClick={() => { setFilterDocType('other'); setPage(1) }} />
              </div>
            </div>

            <div className="card p-4">
              <h3 className="font-serif font-bold text-sm mb-3 text-ink">命题单位</h3>
              <div className="max-h-48 overflow-y-auto space-y-1">
                <FilterBtn label="全部地区" active={!filterProvince} onClick={() => { setFilterProvince(undefined); setPage(1) }} />
                {provinces.map(p => (
                  <FilterBtn
                    key={p.province}
                    label={`${p.province} (${p.count})`}
                    active={filterProvince === p.province}
                    onClick={() => { setFilterProvince(p.province); setPage(1) }}
                  />
                ))}
              </div>
            </div>

            {hasFilters && (
              <button onClick={clearFilters} className="text-sm text-accent hover:text-accent-dark underline">
                清除所有筛选
              </button>
            )}
          </div>
        </aside>

        <div className="flex-1 min-w-0">
          {filterSearch && (
            <div className="mb-4 text-sm text-muted">
              搜索：<span className="text-ink font-medium">&quot;{filterSearch}&quot;</span> 共 {total} 个结果
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="text-muted text-lg animate-pulse">加载中…</div>
            </div>
          ) : documents.length === 0 ? (
            <div className="card p-16 text-center text-muted">
              <p className="text-lg mb-2">暂无文档</p>
              <p className="text-sm">当前条件下没有找到相关文档</p>
            </div>
          ) : (
            <>
              <div className="mb-2 text-sm text-muted">共 {total} 份文档</div>
              <div className="space-y-3">
                {documents.map(doc => (
                  <DocCard key={doc.id} doc={doc} />
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
                  <span className="text-sm text-muted px-4">
                    {page} / {totalPages}
                  </span>
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
      </div>
    </div>
  )
}

function FilterBtn({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`block w-full text-left px-2 py-1 rounded text-sm ${active ? 'bg-accent text-white' : 'hover:bg-gray-100'}`}
    >
      {label}
    </button>
  )
}

function DocCard({ doc }: { doc: DocumentListItem }) {
  return (
    <Link href={`/doc/${doc.id}`} className="card p-5 block group">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0 flex-1">
          <h3 className="font-serif font-bold text-ink group-hover:text-accent transition-colors leading-snug mb-2">
            {doc.title}
          </h3>
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="bg-accent/10 text-accent px-2 py-0.5 rounded-full font-medium">
              {doc.year}
            </span>
            <span className="bg-gray-100 text-muted px-2 py-0.5 rounded-full">
              {docTypeLabel(doc.doc_type)}
            </span>
            {doc.exam_category && (
              <span className="bg-gray-100 text-muted px-2 py-0.5 rounded-full">
                {doc.exam_category}
              </span>
            )}
            <span className="bg-gray-100 text-muted px-2 py-0.5 rounded-full">
              {provinceLabel(doc.province)}
            </span>
          </div>
        </div>
        <div className="flex-shrink-0 text-right text-xs text-muted space-y-1">
          <div>{doc.file_format.toUpperCase()}</div>
          <div>{formatFileSize(doc.file_size)}</div>
          {doc.view_count > 0 && <div>{doc.view_count} 次浏览</div>}
        </div>
      </div>
    </Link>
  )
}

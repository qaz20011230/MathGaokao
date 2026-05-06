'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { api, StatsOut, YearStat } from '@/lib/api'
import { periodLabel, docTypeLabel, formatFileSize } from '@/lib/utils'

export default function HomePage() {
  const [stats, setStats] = useState<StatsOut | null>(null)
  const [years, setYears] = useState<YearStat[]>([])
  const [searchText, setSearchText] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([api.getStats(), api.getYears()])
      .then(([s, y]) => { setStats(s); setYears(y) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-muted text-lg animate-pulse">加载中…</div>
      </div>
    )
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (searchText.trim()) {
      window.location.href = `/browse?search=${encodeURIComponent(searchText.trim())}`
    }
  }

  return (
    <div>
      <section className="bg-gradient-to-b from-ink to-gray-800 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-3xl md:text-5xl font-serif font-bold leading-tight mb-6">
            高考数学试题档案馆
          </h1>
          <p className="text-lg md:text-xl text-gray-300 font-serif mb-8 leading-relaxed">
            收录科举制度废除至今一切高考数学试卷<br />
            1905—2025，跨越一百二十年的数学教育记忆
          </p>
          <form onSubmit={handleSearch} className="max-w-xl mx-auto flex gap-3">
            <input
              type="text"
              value={searchText}
              onChange={e => setSearchText(e.target.value)}
              placeholder="搜索年份、地区或试卷名称…"
              className="flex-1 px-5 py-3 rounded-md text-ink bg-white border-0 focus:outline-none focus:ring-2 focus:ring-accent-light text-base"
            />
            <button type="submit" className="btn-primary px-7 py-3 text-base">
              搜索
            </button>
          </form>
        </div>
      </section>

      {stats && (
        <section className="max-w-7xl mx-auto px-4 -mt-8 grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <StatCard label="收录文档" value={stats.total_documents} unit="份" />
          <StatCard label="总数据量" value={formatFileSize(stats.total_size_bytes)} unit="" />
          <StatCard label="覆盖年份" value={stats.years_covered.length} unit="年" />
          <StatCard
            label="最早年份"
            value={stats.years_covered.length > 0 ? stats.years_covered[0] : '—'}
            unit=""
          />
        </section>
      )}

      <section className="max-w-7xl mx-auto px-4 mb-16">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-serif font-bold text-ink">按年份浏览</h2>
          <Link href="/browse" className="text-accent hover:text-accent-dark font-medium text-sm">
            查看全部 →
          </Link>
        </div>
        <div className="card p-6 overflow-hidden">
          <div className="w-full overflow-x-auto pb-2">
            <div className="flex gap-1 flex-nowrap min-w-max">
              {years.map(y => (
                <Link
                  key={y.year}
                  href={`/browse?year=${y.year}`}
                  className="flex-shrink-0 w-20 py-2 text-center rounded hover:bg-accent hover:text-white transition-colors cursor-pointer group"
                >
                  <div className="text-xs font-mono font-bold group-hover:text-white">{y.year}</div>
                  <div className="text-[10px] text-muted group-hover:text-white/70">{y.count}份</div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {stats && (
        <section className="max-w-7xl mx-auto px-4 mb-16">
          <h2 className="text-2xl font-serif font-bold text-ink mb-8">文档总览</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card p-6">
              <h3 className="font-serif font-bold text-lg mb-4 text-ink">按时期</h3>
              <div className="space-y-3">
                {Object.entries(stats.periods).map(([k, v]) => (
                  <div key={k} className="flex justify-between items-center">
                    <span className="text-sm">{periodLabel(k)}</span>
                    <span className="text-sm font-mono text-accent">{v} 份</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="card p-6">
              <h3 className="font-serif font-bold text-lg mb-4 text-ink">按类型</h3>
              <div className="space-y-3">
                {Object.entries(stats.doc_types).map(([k, v]) => (
                  <div key={k} className="flex justify-between items-center">
                    <span className="text-sm">{docTypeLabel(k)}</span>
                    <span className="text-sm font-mono text-accent">{v} 份</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

function StatCard({ label, value, unit }: { label: string; value: string | number; unit: string }) {
  return (
    <div className="card p-5 text-center">
      <div className="text-2xl font-bold font-mono text-accent">{value}<span className="text-sm font-normal text-muted ml-1">{unit}</span></div>
      <div className="text-sm text-muted mt-1">{label}</div>
    </div>
  )
}

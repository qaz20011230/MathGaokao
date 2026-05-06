'use client'

import { usePathname } from 'next/navigation'

export function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isDocPage = pathname.startsWith('/doc/')

  return (
    <>
      {!isDocPage && <Header />}
      <main className={isDocPage ? 'flex-1 flex flex-col' : 'flex-1'}>{children}</main>
      {!isDocPage && <Footer />}
    </>
  )
}

function Header() {
  return (
    <header className="bg-ink text-white border-b-4 border-accent">
      <div className="max-w-7xl mx-auto px-4 py-5 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-accent rounded-lg flex items-center justify-center font-serif font-bold text-lg">
            ∑
          </div>
          <div>
            <a href="/" className="text-xl font-serif font-bold tracking-wide hover:text-accent-light transition-colors">
              mathgaokao.top
            </a>
            <p className="text-xs text-gray-400 mt-0.5 font-serif">高考数学试题档案馆 1905—2025</p>
          </div>
        </div>
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium">
          <a href="/" className="hover:text-accent-light transition-colors">首页</a>
          <a href="/browse" className="hover:text-accent-light transition-colors">浏览文档</a>
          <a href="/about" className="hover:text-accent-light transition-colors">关于本站</a>
        </nav>
      </div>
    </header>
  )
}

function Footer() {
  return (
    <footer className="bg-ink text-gray-400 text-sm py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 text-center space-y-2">
        <p>mathgaokao.top · 高考数学试题档案馆</p>
        <p>收录科举制度废除至今一切高考数学试卷与相关文档</p>
        <p className="text-xs mt-3">
          本站所有文档仅供学术研究与历史保存之用，请勿用于商业用途
        </p>
        <p className="text-xs">
          &copy; {new Date().getFullYear()} 广州菲娜睿特人工智能科技有限责任公司
        </p>
      </div>
    </footer>
  )
}

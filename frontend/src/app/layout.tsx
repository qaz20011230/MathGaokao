import './globals.css'
import type { Metadata } from 'next'
import { LayoutWrapper } from './layout-wrapper'

export const metadata: Metadata = {
  title: 'mathgaokao.top — 高考数学试题档案馆',
  description: '收录科举制度废除至今一切高考数学试卷、答题卡及相关文档。1905—2025，跨越120年的数学教育记忆。',
  keywords: '高考数学, 数学试卷, 高考真题, 数学答题卡, 中国高考, 数学教育',
  robots: { index: true, follow: true },
  icons: { icon: '/favicon.svg', type: 'image/svg+xml' },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen flex flex-col bg-bg-page">
        <LayoutWrapper>
          {children}
        </LayoutWrapper>
      </body>
    </html>
  )
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

export function periodLabel(period: string): string {
  const map: Record<string, string> = {
    pre_1952: '1905—1951',
    '1952_1965': '1952—1965',
    '1977_now': '1977—至今',
  }
  return map[period] || period
}

export function docTypeLabel(docType: string): string {
  const map: Record<string, string> = {
    exam_paper: '试卷',
    answer_sheet: '答题卡',
    answer_key: '参考答案',
    other: '其他文档',
  }
  return map[docType] || docType
}

export function categoryLabel(cat: string | null | undefined): string {
  return cat || '通用'
}

export function provinceLabel(p: string | null | undefined): string {
  return p || '全国卷'
}

export function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

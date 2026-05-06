export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-serif font-bold text-ink mb-8">关于本站</h1>

      <div className="prose prose-stone max-w-none">
        <section className="card p-8 mb-8">
          <h2 className="font-serif font-bold text-xl text-ink mb-4">项目缘起</h2>
          <div className="space-y-4 text-muted leading-relaxed">
            <p>
              清光绪三十一年（1905年），延续一千三百余年的科举制度正式废除，中国教育自此进入了全新的时代。
              从民国时期的大学独立招生，到1952年全国统一高等学校招生考试的建立，
              再到1977年恢复高考至今，数学作为核心考试科目，其试题变迁本身就是一部浓缩的中国近现代教育史。
            </p>
            <p>
              mathgaokao.top 致力于系统性地收录、保存和展示自科举制度废除以来所有高考数学试卷、
              答题卡及相关文档资料。我们希望通过这些承载了无数人青春记忆与命运转折的试题，
              为中国的数学教育史留下完整、可追溯的数字档案。
            </p>
          </div>
        </section>

        <section className="card p-8 mb-8">
          <h2 className="font-serif font-bold text-xl text-ink mb-4">收录范围</h2>
          <div className="space-y-4 text-muted leading-relaxed">
            <div className="flex gap-4 items-start">
              <span className="text-accent font-serif font-bold text-lg flex-shrink-0">1905—1951</span>
              <div>
                <p className="font-medium text-ink mb-1">各大学独立招生时期</p>
                <p>包括北京大学、清华大学、燕京大学、交通大学、中央大学等高校自命题数学试卷。此时期无统一考试标准，各校命题风格迥异，极具历史研究价值。</p>
              </div>
            </div>
            <div className="flex gap-4 items-start">
              <span className="text-accent font-serif font-bold text-lg flex-shrink-0">1952—1965</span>
              <div>
                <p className="font-medium text-ink mb-1">全国统一高考初期</p>
                <p>1952年新中国建立全国统一高考制度，至1966年停办前的数学试卷。涵盖理工类与文史类两类试卷。</p>
              </div>
            </div>
            <div className="flex gap-4 items-start">
              <span className="text-accent font-serif font-bold text-lg flex-shrink-0">1977—至今</span>
              <div>
                <p className="font-medium text-ink mb-1">恢复高考至今</p>
                <p>1977年恢复高考以来的全部数学试卷，包括全国卷、各省自主命题卷、新高考卷等全类型。是本站当前重点收录的部分。</p>
              </div>
            </div>
          </div>
        </section>

        <section className="card p-8 mb-8">
          <h2 className="font-serif font-bold text-xl text-ink mb-4">文档类型</h2>
          <div className="grid sm:grid-cols-2 gap-4 text-sm">
            <div className="border border-border rounded-lg p-4">
              <div className="font-medium text-ink mb-1">试卷</div>
              <div className="text-muted">正式考试使用的数学试卷原题</div>
            </div>
            <div className="border border-border rounded-lg p-4">
              <div className="font-medium text-ink mb-1">答题卡</div>
              <div className="text-muted">标准化考试答题卡样式</div>
            </div>
            <div className="border border-border rounded-lg p-4">
              <div className="font-medium text-ink mb-1">参考答案</div>
              <div className="text-muted">官方或权威来源提供的参考答案与评分标准</div>
            </div>
            <div className="border border-border rounded-lg p-4">
              <div className="font-medium text-ink mb-1">其他文档</div>
              <div className="text-muted">考纲、命题说明、统计分析等辅助材料</div>
            </div>
          </div>
        </section>

        <section className="card p-8">
          <h2 className="font-serif font-bold text-xl text-ink mb-4">使用说明</h2>
          <div className="space-y-3 text-muted leading-relaxed text-sm">
            <p><span className="font-medium text-ink">浏览：</span>通过顶部导航或首页入口按年份、时期、类型、地区浏览全部文档。</p>
            <p><span className="font-medium text-ink">搜索：</span>在首页搜索框输入年份、省份、试卷名称等关键词进行检索。</p>
            <p><span className="font-medium text-ink">在线阅读：</span>点击任意文档即可在线浏览PDF全文，无需下载。</p>
            <p><span className="font-medium text-ink">下载：</span>出于版权与历史保护考虑，仅管理员可下载文档。普通访客仅可在线阅读。</p>
            <p><span className="font-medium text-ink">贡献：</span>如果您拥有本站尚未收录的历史资料，欢迎通过合适渠道联系我们。</p>
          </div>
        </section>
      </div>
    </div>
  )
}

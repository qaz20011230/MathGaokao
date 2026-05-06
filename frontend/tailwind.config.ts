/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        parchment: '#faf8f5',
        ink: '#1a1a2e',
        accent: '#8b4513',
        'accent-light': '#d4a574',
        'accent-dark': '#5c2d0a',
        muted: '#6b7280',
        border: '#e5e7eb',
        'bg-card': '#ffffff',
        'bg-page': '#f5f3ee',
      },
      fontFamily: {
        serif: ['"Noto Serif SC"', '"Source Han Serif SC"', 'serif'],
        sans: ['"Noto Sans SC"', '"PingFang SC"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

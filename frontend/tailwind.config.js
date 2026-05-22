/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        parchment: { 50:'#fdf8ee', 100:'#f5e6c8', 200:'#e8cc96', 300:'#d4a85c', 400:'#c9903a' },
        gold:      { 300:'#e8c96e', 400:'#c9a84c', 500:'#a8892e', 600:'#8b6914' },
        stone:     { 400:'#7a5030', 500:'#5a3820', 600:'#3d2414', 700:'#2e1a0e', 800:'#241408', 900:'#1a0f0a' },
        forest:    { 400:'#5a9a42', 500:'#3d7a2a', 600:'#2d5a1e', 700:'#234a16', 800:'#1a3410', 900:'#0f1f08' },
        gem:       { blue:'#4a90d9', purple:'#8b4adb', red:'#d94a4a' },
      },
      fontFamily: {
        cinzel: ['Cinzel', 'Georgia', 'serif'],
        lato:   ['Lato', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'gold-glow':  '0 0 12px rgba(201,168,76,0.4), inset 0 0 6px rgba(201,168,76,0.1)',
        'green-glow': '0 0 10px rgba(61,122,42,0.5), inset 0 0 4px rgba(61,122,42,0.15)',
      },
    },
  },
  plugins: [],
}

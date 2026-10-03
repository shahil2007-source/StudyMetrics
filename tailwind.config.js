/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#070A11',
          900: '#0F172A',
          800: '#1E293B',
          700: '#334155',
        },
        brand: {
          indigo: '#6366F1',
          blue: '#3B82F6',
          purple: '#8B5CF6',
        }
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#000000',
        terminal: {
          DEFAULT: '#00ff88',
          dark: '#00cc66',
        },
      },
    },
  },
  plugins: [],
}

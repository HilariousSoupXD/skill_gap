/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        hand: ['"Patrick Hand"', 'cursive'],
        sans: ['Nunito', 'sans-serif'],
      },
      colors: {
        paper: '#FDFBF7',
        // The Highlighter Palette
        highlighter: {
          yellow: '#FEF08A',
          pink: '#FBCFE8',
          blue: '#BAE6FD',
        }
      },
      // The "Hard" shadow for the cutout look
      boxShadow: {
        'hard': '4px 4px 0px 0px rgba(0,0,0,0.2)',
      }
    },
  },
  plugins: [],
}
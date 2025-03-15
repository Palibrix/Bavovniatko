/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Main theme colors
        primary: '#5d6e89',
        secondary: '#a4a0c8',
        'light-bg': '#f8f7f4',
        'dark-bg': '#1d2b3a',
        'text-color': '#3d3d3d',
        'light-text': '#f8f7f4',

        // Component category colors
        propulsion: {
          DEFAULT: '#f09177',
          light: '#f6b8a7',
          dark: '#d37057'
        },
        control: {
          DEFAULT: '#6bbfba',
          light: '#9dd4d1',
          dark: '#4a9993'
        },
        frame: {
          DEFAULT: '#8d8178',
          light: '#b0a79f',
          dark: '#6a5f56'
        },
        video: {
          DEFAULT: '#e095a6',
          light: '#edbac5',
          dark: '#c7677e'
        },
        antenna: {
          DEFAULT: '#9cc298',
          light: '#c0dbbe',
          dark: '#76a571'
        }
      }
    }
  },
  plugins: [],
}
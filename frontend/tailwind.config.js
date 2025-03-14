/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#5d6e89',
        'secondary': '#a4a0c8',
        'light-bg': '#f8f7f4',
        'dark-bg': '#1d2b3a',
        'text-color': '#3d3d3d',
        'light-text': '#f8f7f4',
        'propulsion-color': '#f09177', /* Coral/orange for motors and propellers */
        'control-color': '#6bbfba',    /* Teal for flight controllers and related items */
        'frame-color': '#8d8178',      /* Brown/taupe for frames */
        'video-color': '#e095a6',      /* Pink for cameras and video transmitters */
        'antenna-color': '#9cc298',    /* Green for antennas */
        'drone-color': '#a4a0c8',      /* Purple for complete drones */
      },
      animation: {
        'hover-lift': 'hover-lift 0.3s ease-out forwards',
      },
      keyframes: {
        'hover-lift': {
          '0%': { transform: 'translateY(0)', boxShadow: '0 4px 8px rgba(0,0,0,0.05)' },
          '100%': { transform: 'translateY(-5px)', boxShadow: '0 10px 20px rgba(0,0,0,0.1)' },
        }
      }
    },
  },
  plugins: [],
}
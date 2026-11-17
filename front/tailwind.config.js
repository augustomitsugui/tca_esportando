/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{svelte,js}'],
  theme: {
    extend: {
      colors: {
        // verde institucional
        brand: {
          50: '#EEF8EE',
          100: '#D9F0DA',
          200: '#B4E1B7',
          300: '#84CC8A',
          400: '#4FB45A',
          500: '#2E9E3F',
          600: '#23822F',
          700: '#1D6A28',
          800: '#185522',
          900: '#123F1A',
        },
        // vermelho de destaque
        accent: {
          50: '#FFF1F1',
          100: '#FFE0E0',
          200: '#FFC2C2',
          300: '#FF9494',
          400: '#F55F5F',
          500: '#E23636',
          600: '#CC2229',
          700: '#A9181F',
          800: '#8A171C',
        },
        cream: { 50: '#F7FBF4', 100: '#EFF7EA' },
        ink: {
          300: '#9AAA9D',
          500: '#5B6B5E',
          600: '#46554A',
          700: '#2C3A2F',
          900: '#14201A',
        },
      },
      fontFamily: {
        display: ['"Barlow Condensed"', 'Impact', 'sans-serif'],
        sans: ['Barlow', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 6px 20px -8px rgba(35, 130, 47, 0.25)',
        lift: '0 18px 36px -14px rgba(35, 130, 47, 0.4)',
      },
      keyframes: {
        pop: {
          '0%': { opacity: '0', transform: 'scale(.94) translateY(8px)' },
          '100%': { opacity: '1', transform: 'scale(1) translateY(0)' },
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateX(24px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
          '50%': { transform: 'translateY(-14px) rotate(6deg)' },
        },
      },
      animation: {
        pop: 'pop .22s ease-out',
        'slide-in': 'slideIn .25s ease-out',
        float: 'float 6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};

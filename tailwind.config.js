/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './wallpapers/templates/**/*.html',
    '!./**/stitch_enhanced_page_redesign/**',
  ],
  safelist: [
    // JS classList.add classes (not in HTML attributes)
    'border-primary', 'scale-[1.02]', 'text-primary', 'animate-in', 'revealed',
    'opacity-0', 'opacity-100', 'transition-opacity', 'duration-500',
    'page-exit', 'loaded', 'hidden',
    // Group/peer variants used in conditional template logic
    'group-hover:scale-105', 'group-hover:scale-110', 'group-hover:opacity-100',
    'group-hover:text-primary', 'group-hover:text-on-surface',
    'group-hover:border-primary/50', 'group-hover:translate-y-0',
    'group-hover:bg-transparent', 'group-open:rotate-180',
    'peer-checked:bg-primary', 'peer-checked:after:translate-x-full',
    'peer-checked:after:border-white', 'peer-focus:outline-none',
    'rtl:peer-checked:after:-translate-x-full',
    // Variants used in template conditionals (not always present in HTML)
    'hover:bg-primary/10', 'hover:bg-primary/20', 'hover:bg-primary/30',
    'hover:bg-primary/50', 'hover:bg-error/10', 'hover:bg-surface-bright',
    'hover:opacity-90', 'hover:opacity-100', 'hover:brightness-110',
    'hover:shadow-lg', 'hover:shadow-primary/20',
    'hover:translate-x-1', 'hover:-translate-y-0.5',
    'active:scale-[0.98]', 'active:scale-90', 'active:scale-95',
    'active:opacity-80', 'focus:border-primary-container', 'focus:ring-0',
  ],
  theme: {
    extend: {
      colors: {
        surface: '#151317', 'surface-dim': '#151317', 'surface-bright': '#3b383d',
        'surface-container-lowest': '#0f0d11', 'surface-container-low': '#1d1b1f',
        'surface-container': '#211f23', 'surface-container-high': '#2c292d',
        'surface-container-highest': '#373438', 'on-surface': '#e7e1e6',
        'on-surface-variant': '#cbc4ce', outline: '#948f98', 'outline-variant': '#49454d',
        'surface-tint': '#d0bfec', primary: '#d0bfec', 'on-primary': '#362a4d',
        'primary-container': '#7e7098', 'on-primary-container': '#ffffff',
        'inverse-primary': '#65587e', secondary: '#cbc4ce', 'on-secondary': '#322f36',
        'secondary-container': '#49454d', 'on-secondary-container': '#b9b3bc',
        tertiary: '#c7c5cc', 'on-tertiary': '#303035', 'tertiary-container': '#76767c',
        'on-tertiary-container': '#ffffff', error: '#ffb4ab', 'on-error': '#690005',
        'error-container': '#93000a', 'on-error-container': '#ffdad6',
        background: '#151317', 'on-background': '#e7e1e6', 'surface-variant': '#373438',
      },
      fontFamily: { display: ['Manrope'], body: ['Manrope'], label: ['Manrope'] },
      fontSize: {
        'display-lg': ['48px', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '700' }],
        'display-md': ['36px', { lineHeight: '1.2', letterSpacing: '-0.02em', fontWeight: '700' }],
        'headline-lg': ['32px', { lineHeight: '1.2', fontWeight: '600' }],
        'headline-md': ['24px', { lineHeight: '1.3', fontWeight: '600' }],
        'body-lg': ['18px', { lineHeight: '1.6', fontWeight: '400' }],
        'body-md': ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        'label-md': ['14px', { lineHeight: '1.4', letterSpacing: '0.05em', fontWeight: '500' }],
        'label-sm': ['12px', { lineHeight: '1.4', fontWeight: '500' }],
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/container-queries')],
}

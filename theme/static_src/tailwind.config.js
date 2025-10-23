module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
        '../../**/*.js',
        '../../**/*.py',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        container: {
            center: true,
        },
        extend: {
            spacing: {
                '96': '24rem',
            },
            scrollMargin: {
                '96': '24rem',
            },
            scrollPadding: {
                '96': '24rem',
            },
            colors: {
                'regal-blue': '#243c5a',
                'cyan-400': '#22d3ee',
                'cyan-50': '#ecfeff',
                'cyan-500': '#06b6d4',
                'cyan-600': '#0891b2',
                'cyan-900': '#164e63',
                'blue-500': '#3b82f6',
                'black': '#000000',
                'teal-700': '#0f766e',
                'teal-800': '#115e59',
                'sky-900': '#0c4a6e',
                'orange-600': '#ea580c',
                'orange-500': '#f97316',
                'neutral-950': '#09090b',
            },
            animation: {
                'spin-slow': 'spin 3s linear infinite',
                wiggle: 'wiggle 1s ease-in-out infinite',
            }
        },
        fontFamily: {
            sans: ['Graphik', 'sans-serif'],
            serif: ['Merriweather', 'serif'],
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}

// tailwind.config.js
module.exports = {
  content: [
    '../../templates/**/*.html', // j'adapte selon ton projet
    './src/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        bgcolor: '#FBF2FF', //ma couleur personnalisée
      },
    },
  },
  plugins: [],
}
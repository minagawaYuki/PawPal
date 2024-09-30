/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./userprofile/templates/userprofile/*.{html,js}"],
  theme: {
    colors: {
      'textfield': '#FAF7F0',
      'button': '#4A4947',
      'white': '#FFFFFF',
      'black': '#000000',
      'container': '#ECE8DF',
      'background': '#D8D2C2',
    },
    extend: {},
  },
  plugins: [],
}


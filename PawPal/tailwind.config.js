/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./userprofile/templates/userprofile/*.{html,js}",
            "./register/templates/register/*.{html,js}",
            "./transactions/templates/transactions/*.{html,js}",
            "./admindashboard/templates/admindashboard/*.{html,js}"],
  theme: {
    colors: {
      'textfield': '#FAF7F0',
      'button': '#4A4947',
      'white': '#FFFFFF',
      'black': '#000000',
      'container': '#ECE8DF',
      'background': '#D8D2C2',
      'pending_background': '#F5E4A1',
      'finished_background': '#B8EF96',
      'pending_text_color': '#A68603',
      'finished_text_background': '#3E9B05',
      primary: '#334155', // slate-700
                        'primary-hover': '#475569', // slate-600
                        accent: '#22c55e', // green-500
                        'accent-hover': '#16a34a', // green-600
                        danger: '#ef4444', // red-500
                        'danger-hover': '#dc2626', // red-600
    },
    extend: {
      backgroundColor: {
        'button-hover': '#6D6C6A', 
        'pending-hover': '#E4D28F',
      },
    },
  },
  plugins: [],
}


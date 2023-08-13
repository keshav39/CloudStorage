/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./{templates,static}/**/*.{html, js}",
    "./{templates,static}/**/*.{html, js}",
    "./users/*.py",
  ],
  theme: {
    colors: {},
    extend: {},
  },
  plugins: [],
};

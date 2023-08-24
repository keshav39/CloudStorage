/** @type {import('tailwindcss').Config} */
const colors = require("tailwindcss/colors");

module.exports = {
  content: ["./src/**/*.{html, js}"],
  theme: {
    colors: {
      white: "#fff",
      body: "#f2f2f2",
      common_bg: "#3f978c",
      button: "#3f978c",
      button_hover: "#265a43",
      border: "#265a43",
    },
    extend: {
      height: {
      },
    },
  },
  plugins: [],
};

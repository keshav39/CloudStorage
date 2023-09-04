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
      blue_400: "#60a5fa",
      blue_500: "#3b82f6",
      blue_600: "#2563eb",
      purple_400: "#c084fc",
      grey_600: "#4b5563",
      red_500: "#ef4444",
      red_600: "#dc2626",

    },
    extend: {
      height: {},
    },
  },
  plugins: [],
};

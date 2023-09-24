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
      gray_200: "#e5e7eb",
      gray_300: "#d1d5db",
      gray_400: "#9ca3af",
      gray_500: "#64748b",
      gray_700: "#374151",
      gray_800: "#1f2937",
      gray_900: "#111827",
      red_500: "#ef4444",
      red_600: "#dc2626",
      green_500: "#22c55e",
      green_600: "#16a34a",
    },
    extend: {
      height: {},
    },
  },
  plugins: [],
};

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Ubuntu", "sans-serif"],
      },
      colors: {
        darkBg: "#0b0f17",
        sidebar: "#111827",
        card: "#161e2e",
        accentBlue: "#2563eb",
      },
    },
  },
  plugins: [],
};

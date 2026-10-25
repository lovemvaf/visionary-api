import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#142D4E",
          dark: "#0B192C",
          light: "#1F3E68",
        },
        visionary: {
          DEFAULT: "#2264AC",
          hover: "#1A508B",
          light: "#EBF3FC",
        },
        tealAccent: {
          DEFAULT: "#22A6A1",
          hover: "#1B8783",
          light: "#E6F7F6",
        },
        surface: {
          DEFAULT: "#F5F7FB",
          card: "#FFFFFF",
          border: "#E2E8F0",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;

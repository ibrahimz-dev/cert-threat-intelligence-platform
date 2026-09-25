import tailwindcssAnimate from 'tailwindcss-animate';

/**
 * Slate-grey dark theme (neutral zinc, no blue tint).
 * `darkMode: 'class'` + HSL vars from src/index.css. The `base / surface /
 * raised / line / ink / dim / faint` entries are compat aliases so existing
 * classes (`bg-base`, `text-dim`, `border-line` …) render the grey palette
 * without rewriting every component. `/ <alpha-value>` keeps opacity
 * modifiers (bg-surface/80, border-line/60 …) working.
 */
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border) / <alpha-value>)',
        input: 'hsl(var(--input) / <alpha-value>)',
        ring: 'hsl(var(--ring) / <alpha-value>)',
        background: 'hsl(var(--background) / <alpha-value>)',
        foreground: 'hsl(var(--foreground) / <alpha-value>)',
        primary: {
          DEFAULT: 'hsl(var(--primary) / <alpha-value>)',
          foreground: 'hsl(var(--primary-foreground) / <alpha-value>)',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary) / <alpha-value>)',
          foreground: 'hsl(var(--secondary-foreground) / <alpha-value>)',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive) / <alpha-value>)',
          foreground: 'hsl(var(--destructive-foreground) / <alpha-value>)',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted) / <alpha-value>)',
          foreground: 'hsl(var(--muted-foreground) / <alpha-value>)',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent) / <alpha-value>)',
          foreground: 'hsl(var(--accent-foreground) / <alpha-value>)',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover) / <alpha-value>)',
          foreground: 'hsl(var(--popover-foreground) / <alpha-value>)',
        },
        card: {
          DEFAULT: 'hsl(var(--card) / <alpha-value>)',
          foreground: 'hsl(var(--card-foreground) / <alpha-value>)',
        },

        // ---- Compat aliases → grey tokens (do not use for new code) ----
        base: 'hsl(var(--background) / <alpha-value>)', // page background (#111113 dark)
        surface: 'hsl(var(--card) / <alpha-value>)', // card / panel surface (#1b1b1e dark)
        raised: 'hsl(var(--muted) / <alpha-value>)', // hover / raised layer
        line: 'hsl(var(--border) / <alpha-value>)', // borders / dividers
        ink: 'hsl(var(--foreground) / <alpha-value>)', // primary text
        dim: 'hsl(var(--muted-foreground) / <alpha-value>)', // secondary text
        faint: 'hsl(var(--muted-foreground) / <alpha-value>)', // tertiary text
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        // Vertical ticker for the "recent high-priority feed" widget.
        ticker: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-50%)' },
        },
        // Live-status pulse.
        'pulse-glow': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.3 },
        },
        // Card / modal entrance.
        'fade-in': {
          '0%': { opacity: 0, transform: 'translateY(6px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        // shadcn/ui animations (accordion, dialogs, overlay).
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        ticker: 'ticker 30s linear infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'fade-in': 'fade-in 0.25s ease-out',
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [tailwindcssAnimate],
};

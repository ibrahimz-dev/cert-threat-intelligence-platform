import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext(null);

function applyTheme(theme) {
  const root = document.documentElement;
  const dark = theme !== 'light';
  root.classList.toggle('dark', dark);
  // Keep `data-theme` in sync for any legacy selectors.
  root.setAttribute('data-theme', dark ? 'dark' : 'light');
  try {
    localStorage.setItem('cti-theme', dark ? 'dark' : 'light');
  } catch {
    /* storage unavailable — theme still applies for this session */
  }
}

function initialTheme() {
  try {
    const saved = localStorage.getItem('cti-theme');
    if (saved === 'light' || saved === 'dark') return saved;
  } catch {
    /* ignore */
  }
  // Match C:\Users\ibrahm\Desktop\cert: class strategy, dark by default,
  // system preference ignored.
  return 'dark';
}

/**
 * ThemeProvider — class-based dark-first switch (ported from cert's
 * next-themes `attribute="class" defaultTheme="dark"` setup, minus the extra
 * dependency). Toggles the `dark` class on <html> which the CSS variables in
 * index.css use to re-skin the entire app. Persisted in localStorage.
 */
export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(initialTheme);

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const toggle = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));

  return <ThemeContext.Provider value={{ theme, toggle, setTheme }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within <ThemeProvider>');
  return ctx;
}

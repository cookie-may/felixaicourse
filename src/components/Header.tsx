'use client';

import Link from 'next/link';
import { useTheme } from './ThemeProvider';
import { Star, Menu, Moon, Sun } from 'lucide-react';
import { useState } from 'react';

export default function Header() {
  const { theme, toggleTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinkStyle = {
    transition: 'color 0.2s',
    color: 'var(--text-muted)',
  } as React.CSSProperties;

  return (
    <header
      className="fixed top-0 left-0 right-0 z-50 border-b-2 border-dashed"
      style={{
        background: 'var(--header-bg)',
        backdropFilter: 'blur(12px)',
        borderColor: 'var(--border)'
      }}
    >
      <style>
        {`
          .nav-link { transition: color 0.2s; }
          .nav-link:hover { color: var(--accent) !important; }
        `}
      </style>
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 no-underline">
          <span className="text-xl" style={{ color: 'var(--accent)' }}>●</span>
          <span
            className="font-heading font-bold text-xl"
            style={{ color: 'var(--text)' }}
          >
            AI from Scratch
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/#phases" className="nav-link" style={navLinkStyle}>
            Phases
          </Link>
          <Link href="/catalog" className="nav-link" style={navLinkStyle}>
            Catalog
          </Link>
          <Link href="/#roadmap" className="nav-link" style={navLinkStyle}>
            Roadmap
          </Link>
          <Link href="/glossary" className="nav-link" style={navLinkStyle}>
            Glossary
          </Link>
          <Link href="/ai" className="nav-link" style={navLinkStyle}>
            AI Tutor
          </Link>

          <a
            href="https://github.com/rohitg00/ai-engineering-from-scratch"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-3 py-2 rounded-lg border"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              color: 'var(--text)',
              textDecoration: 'none'
            }}
          >
            <Star className="w-4 h-4" style={{ fill: 'currentColor' }} />
            <span>Star</span>
          </a>

          <button
            onClick={toggleTheme}
            className="w-10 h-10 rounded-full border-2 flex items-center justify-center cursor-pointer transition-all"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              color: 'var(--text)'
            }}
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </nav>

        {/* Mobile menu button */}
        <button
          className="md:hidden p-2"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          style={{ color: 'var(--text)' }}
        >
          <Menu className="w-6 h-6" />
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div
          className="md:hidden border-t-2"
          style={{
            background: 'var(--bg-surface)',
            borderColor: 'var(--border)',
            padding: '1rem'
          }}
        >
          <nav className="flex flex-col gap-4">
            <Link href="/#phases" onClick={() => setMobileMenuOpen(false)} style={{ color: 'var(--text)' }}>
              Phases
            </Link>
            <Link href="/catalog" onClick={() => setMobileMenuOpen(false)} style={{ color: 'var(--text)' }}>
              Catalog
            </Link>
            <Link href="/#roadmap" onClick={() => setMobileMenuOpen(false)} style={{ color: 'var(--text)' }}>
              Roadmap
            </Link>
            <Link href="/glossary" onClick={() => setMobileMenuOpen(false)} style={{ color: 'var(--text)' }}>
              Glossary
            </Link>
            <Link href="/ai" onClick={() => setMobileMenuOpen(false)} style={{ color: 'var(--text)' }}>
              AI Tutor
            </Link>
            <button
              onClick={toggleTheme}
              className="flex items-center gap-2"
              style={{ color: 'var(--text)' }}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
            </button>
          </nav>
        </div>
      )}
    </header>
  );
}
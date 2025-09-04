'use client';

import { useState, useMemo } from 'react';
import { GLOSSARY } from '@/data/glossary';
import PixelPagination from '@/components/PixelPagination';

const PER_PAGE = 10;

export default function GlossaryPage() {
  const [search, setSearch] = useState('');
  const [page, setPage]     = useState(1);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    if (!q) return GLOSSARY;
    return GLOSSARY.filter(e =>
      e.term.toLowerCase().includes(q) ||
      e.says.toLowerCase().includes(q) ||
      e.means.toLowerCase().includes(q)
    );
  }, [search]);

  const handleSearch = (v: string) => { setSearch(v); setPage(1); };
  const pageSlice    = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  return (
    <div style={{ minHeight: '100vh', padding: '48px 24px' }}>
      <div style={{ maxWidth: '860px', margin: '0 auto' }}>

        {/* ── Header ── */}
        <div style={{ marginBottom: '40px' }}>
          <div className="section-label">
            <div className="bar" />
            <span>AI GLOSSARY</span>
          </div>
          <h1 style={{
            fontFamily: 'var(--pixel-font)', fontSize: '18px',
            color: 'var(--text)', marginBottom: '10px', lineHeight: 1.4,
          }}>
            WHAT PEOPLE SAY vs WHAT IT MEANS
          </h1>
          <p style={{ fontFamily: 'var(--body-font)', fontSize: '15px', color: 'var(--text-muted)', maxWidth: '520px' }}>
            277 terms. No jargon. No fluff. Just what things actually mean.
          </p>
        </div>

        {/* ── Search ── */}
        <div style={{ position: 'relative', marginBottom: '28px' }}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
            style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }}>
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input
            className="pixel-input"
            style={{ paddingLeft: '40px', fontSize: '15px' }}
            type="text"
            placeholder="Search terms..."
            value={search}
            onChange={e => handleSearch(e.target.value)}
          />
        </div>

        {/* ── Count ── */}
        <div style={{ marginBottom: '20px' }}>
          <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)', letterSpacing: '0.5px' }}>
            {filtered.length} {filtered.length === 1 ? 'TERM' : 'TERMS'} FOUND
          </span>
        </div>

        {/* ── Terms ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {pageSlice.map((entry, i) => (
            <div
              key={i}
              style={{
                background:  'var(--bg-card)',
                border:      '1px solid var(--border)',
                borderLeft:  '3px solid var(--accent)',
                padding:     '20px 24px',
                transition:  'border-color 0.12s, box-shadow 0.12s',
                boxShadow:   '0 0 14px rgba(232,108,44,0.04)',
              }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLDivElement).style.boxShadow = '0 0 18px var(--accent-glow)';
                (e.currentTarget as HTMLDivElement).style.borderColor = 'var(--accent)';
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLDivElement).style.boxShadow = '0 0 14px rgba(232,108,44,0.04)';
                (e.currentTarget as HTMLDivElement).style.borderColor = 'var(--border)';
              }}
            >
              {/* Term name */}
              <h2 style={{
                fontFamily: 'var(--pixel-font)', fontSize: '12px',
                color: 'var(--accent)', marginBottom: '16px',
                textShadow: '0 0 10px var(--accent-glow)',
                letterSpacing: '0.5px',
              }}>
                {entry.term}
              </h2>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {/* Says */}
                <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                  <span style={{
                    fontFamily: 'var(--pixel-font)', fontSize: '7px',
                    padding: '4px 8px', whiteSpace: 'nowrap', flexShrink: 0,
                    background: 'var(--accent-dim)',
                    border: '1px solid var(--accent-border)',
                    color: 'var(--accent)', letterSpacing: '0.3px',
                  }}>
                    SAYS
                  </span>
                  <p style={{ fontFamily: 'var(--body-font)', fontSize: '14px', color: 'var(--text-muted)', margin: 0, lineHeight: 1.7 }}>
                    {entry.says}
                  </p>
                </div>

                {/* Means */}
                <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                  <span style={{
                    fontFamily: 'var(--pixel-font)', fontSize: '7px',
                    padding: '4px 8px', whiteSpace: 'nowrap', flexShrink: 0,
                    background: 'var(--complete-dim)',
                    border: '1px solid rgba(114,184,48,0.3)',
                    color: 'var(--complete)', letterSpacing: '0.3px',
                  }}>
                    MEANS
                  </span>
                  <p style={{ fontFamily: 'var(--body-font)', fontSize: '14px', color: 'var(--text)', margin: 0, lineHeight: 1.7, fontWeight: 500 }}>
                    {entry.means}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {pageSlice.length === 0 && (
          <div style={{ textAlign: 'center', padding: '60px 24px' }}>
            <p style={{ fontFamily: 'var(--pixel-font)', fontSize: '9px', color: 'var(--text-dim)' }}>
              NO TERMS MATCH &ldquo;{search}&rdquo;
            </p>
          </div>
        )}

        <PixelPagination
          page={page}
          total={filtered.length}
          perPage={PER_PAGE}
          onChange={p => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
        />

        <p style={{
          textAlign: 'center', marginTop: '48px',
          fontFamily: 'var(--mono-font)', fontSize: '12px',
          color: 'var(--text-dim)',
        }}>
          Felix glossary — practical definitions for AI terms, no fluff.
        </p>
      </div>
    </div>
  );
}

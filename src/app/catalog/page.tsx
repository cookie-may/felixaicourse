'use client';

import { useState, useMemo } from 'react';
import { PHASES } from '@/data/phases';
import { useProgress } from '@/components/ProgressProvider';
import Link from 'next/link';
import PixelPagination from '@/components/PixelPagination';

const PER_PAGE = 20;

export default function CatalogPage() {
  const [search, setSearch]           = useState('');
  const [phaseFilter, setPhaseFilter] = useState('all');
  const [typeFilter, setTypeFilter]   = useState('all');
  const [page, setPage]               = useState(1);
  const { isComplete }                = useProgress();

  const allLessons = useMemo(() => {
    const lessons: Array<{
      name: string;
      type: string;
      lang: string;
      path?: string;
      phaseName: string;
      phaseId: number;
    }> = [];
    PHASES.forEach(phase => {
      phase.lessons.forEach(lesson => {
        lessons.push({
          name:      lesson.name,
          type:      lesson.type,
          lang:      lesson.lang,
          path:      lesson.path,
          phaseName: phase.name,
          phaseId:   phase.id,
        });
      });
    });
    return lessons;
  }, []);

  const filtered = useMemo(() => {
    const q = search.toLowerCase();
    return allLessons.filter(l => {
      const matchSearch = !q ||
        l.name.toLowerCase().includes(q) ||
        l.lang.toLowerCase().includes(q) ||
        l.phaseName.toLowerCase().includes(q);
      const matchPhase = phaseFilter === 'all' || l.phaseId === parseInt(phaseFilter);
      const matchType  = typeFilter === 'all' || l.type === typeFilter;
      return matchSearch && matchPhase && matchType;
    });
  }, [allLessons, search, phaseFilter, typeFilter]);

  /* reset page on filter change */
  const handleSearch = (v: string) => { setSearch(v); setPage(1); };
  const handlePhase  = (v: string) => { setPhaseFilter(v); setPage(1); };
  const handleType   = (v: string) => { setTypeFilter(v); setPage(1); };

  const pageSlice = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const selStyle: React.CSSProperties = {
    background:  'var(--bg-card)',
    border:      '1px solid var(--border)',
    color:       'var(--text)',
    fontFamily:  'var(--mono-font)',
    fontSize:    '13px',
    padding:     '10px 14px',
    outline:     'none',
    cursor:      'pointer',
  };

  return (
    <div style={{ minHeight: '100vh', padding: '48px 24px' }}>
      <div style={{ maxWidth: '1100px', margin: '0 auto' }}>

        {/* ── Header ── */}
        <div style={{ marginBottom: '40px' }}>
          <div className="section-label">
            <div className="bar" />
            <span>LESSON CATALOG</span>
          </div>
          <h1 style={{
            fontFamily: 'var(--pixel-font)', fontSize: '20px',
            color: 'var(--text)', marginBottom: '10px', lineHeight: 1.4,
          }}>
            ALL 272+ LESSONS
          </h1>
          <p style={{ fontFamily: 'var(--body-font)', fontSize: '15px', color: 'var(--text-muted)', maxWidth: '560px' }}>
            Every lesson across all 20 phases. Search, filter by phase or type, and jump straight in.
          </p>
        </div>

        {/* ── Filters ── */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginBottom: '24px', alignItems: 'center' }}>
          {/* Search */}
          <div style={{ position: 'relative', flex: '1 1 260px', minWidth: '200px' }}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
              style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-dim)' }}>
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              className="pixel-input"
              style={{ paddingLeft: '36px' }}
              type="text"
              placeholder="Search lessons, phases, languages..."
              value={search}
              onChange={e => handleSearch(e.target.value)}
            />
          </div>

          {/* Phase filter */}
          <select style={selStyle} value={phaseFilter} onChange={e => handlePhase(e.target.value)}>
            <option value="all">ALL PHASES</option>
            {PHASES.map(p => (
              <option key={p.id} value={p.id}>
                {String(p.id).padStart(2, '0')} · {p.name}
              </option>
            ))}
          </select>

          {/* Type filter */}
          <select style={selStyle} value={typeFilter} onChange={e => handleType(e.target.value)}>
            <option value="all">ALL TYPES</option>
            <option value="Build">BUILD</option>
            <option value="Learn">LEARN</option>
          </select>
        </div>

        {/* ── Count ── */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)', letterSpacing: '0.5px' }}>
            SHOWING {Math.min((page - 1) * PER_PAGE + 1, filtered.length)}–{Math.min(page * PER_PAGE, filtered.length)} OF {filtered.length}
          </span>
          <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)' }}>
            {allLessons.length} TOTAL
          </span>
        </div>

        {/* ── Table ── */}
        <div style={{
          border: '1px solid var(--border)',
          borderTop: '3px solid var(--accent)',
          background: 'var(--bg-card)',
          overflowX: 'auto',
          boxShadow: '0 0 20px rgba(232,108,44,0.06)',
        }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border)', background: 'var(--bg-surface)' }}>
                {['PHASE', 'LESSON', 'TYPE', 'LANG', 'STATUS'].map(h => (
                  <th key={h} style={{
                    textAlign: 'left', padding: '14px 16px',
                    fontFamily: 'var(--pixel-font)', fontSize: '8px',
                    color: 'var(--accent)', letterSpacing: '0.5px',
                    whiteSpace: 'nowrap',
                  }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {pageSlice.map((lesson, i) => {
                const parts   = lesson.path?.split('/');
                const phSlug  = parts?.[1];
                const lsSlug  = parts?.[2];
                const hasLink = !!phSlug && !!lsSlug;
                const done    = lesson.path ? isComplete(lesson.path) : false;

                return (
                  <tr
                    key={i}
                    style={{
                      borderBottom: '1px solid var(--border-dim)',
                      transition: 'background 0.12s',
                    }}
                    onMouseEnter={e => (e.currentTarget.style.background = 'var(--bg-card-hover)')}
                    onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
                  >
                    {/* Phase */}
                    <td style={{ padding: '14px 16px', whiteSpace: 'nowrap' }}>
                      <span style={{
                        fontFamily: 'var(--pixel-font)', fontSize: '9px',
                        color: 'var(--accent)', letterSpacing: '0.3px',
                      }}>
                        {String(lesson.phaseId).padStart(2, '0')}
                      </span>
                      <span style={{
                        display: 'block', fontFamily: 'var(--mono-font)',
                        fontSize: '11px', color: 'var(--text-dim)', marginTop: '2px',
                      }}>
                        {lesson.phaseName}
                      </span>
                    </td>

                    {/* Lesson name */}
                    <td style={{ padding: '14px 16px', minWidth: '200px' }}>
                      {hasLink ? (
                        <Link
                          href={`/lessons/${phSlug}/${lsSlug}`}
                          style={{
                            fontFamily: 'var(--body-font)', fontSize: '14px',
                            color: 'var(--text)', textDecoration: 'none',
                            fontWeight: 500,
                          }}
                          onMouseEnter={(e: React.MouseEvent<HTMLAnchorElement>) => { e.currentTarget.style.color = 'var(--accent)'; }}
                          onMouseLeave={(e: React.MouseEvent<HTMLAnchorElement>) => { e.currentTarget.style.color = 'var(--text)'; }}
                        >
                          {lesson.name}
                        </Link>
                      ) : (
                        <span style={{ fontFamily: 'var(--body-font)', fontSize: '14px', color: 'var(--text-muted)' }}>
                          {lesson.name}
                        </span>
                      )}
                    </td>

                    {/* Type */}
                    <td style={{ padding: '14px 16px', whiteSpace: 'nowrap' }}>
                      <span style={{
                        fontFamily: 'var(--pixel-font)', fontSize: '7px',
                        padding: '4px 8px',
                        border: `1px solid ${lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)'}`,
                        color: lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)',
                        letterSpacing: '0.3px',
                        boxShadow: lesson.type === 'Build'
                          ? '0 0 6px var(--complete-glow)'
                          : '0 0 6px var(--accent-glow)',
                      }}>
                        {lesson.type.toUpperCase()}
                      </span>
                    </td>

                    {/* Lang */}
                    <td style={{ padding: '14px 16px' }}>
                      <span style={{ fontFamily: 'var(--mono-font)', fontSize: '12px', color: 'var(--text-muted)' }}>
                        {lesson.lang}
                      </span>
                    </td>

                    {/* Status */}
                    <td style={{ padding: '14px 16px', whiteSpace: 'nowrap' }}>
                      {done ? (
                        <span style={{
                          fontFamily: 'var(--pixel-font)', fontSize: '7px',
                          padding: '4px 8px',
                          background: 'var(--complete-dim)',
                          border: '1px solid var(--complete)',
                          color: 'var(--complete)',
                          letterSpacing: '0.3px',
                          boxShadow: '0 0 6px var(--complete-glow)',
                        }}>
                          ✓ DONE
                        </span>
                      ) : hasLink ? (
                        <span style={{
                          fontFamily: 'var(--pixel-font)', fontSize: '7px',
                          padding: '4px 8px',
                          background: 'var(--accent-dim)',
                          border: '1px solid var(--accent-border)',
                          color: 'var(--text-dim)',
                          letterSpacing: '0.3px',
                        }}>
                          OPEN
                        </span>
                      ) : (
                        <span style={{
                          fontFamily: 'var(--pixel-font)', fontSize: '7px',
                          padding: '4px 8px',
                          border: '1px solid var(--border)',
                          color: 'var(--text-dim)',
                          letterSpacing: '0.3px',
                        }}>
                          —
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>

          {pageSlice.length === 0 && (
            <div style={{ textAlign: 'center', padding: '48px 24px' }}>
              <p style={{ fontFamily: 'var(--pixel-font)', fontSize: '9px', color: 'var(--text-dim)' }}>
                NO LESSONS MATCH YOUR SEARCH
              </p>
            </div>
          )}
        </div>

        <PixelPagination
          page={page}
          total={filtered.length}
          perPage={PER_PAGE}
          onChange={p => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
        />
      </div>
    </div>
  );
}

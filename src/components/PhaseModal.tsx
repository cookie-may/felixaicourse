'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Phase, Lesson } from '@/data/phases';
import { useProgress } from './ProgressProvider';
import { X } from 'lucide-react';

interface Props { phase: Phase; phaseIndex: number; onClose: () => void; }

/* derive route params from lesson.path = "phases/00-setup-and-tooling/01-dev-environment" */
function routeOf(lesson: Lesson): { phase: string; lesson: string } | null {
  if (!lesson.path) return null;
  const parts = lesson.path.split('/');   // ["phases", "00-setup-and-tooling", "01-dev-environment"]
  if (parts.length !== 3) return null;
  return { phase: parts[1], lesson: parts[2] };
}

/* the key used in localStorage — same as lesson.path */
function keyOf(lesson: Lesson): string | null {
  return lesson.path ?? null;
}

/* segmented bar (reuse style from globals) */
function SegBar({ pct }: { pct: number }) {
  const N = 12;
  const filled = Math.floor(pct / (100 / N));
  return (
    <div style={{ display: 'flex', gap: '2px' }}>
      {Array.from({ length: N }).map((_, i) => (
        <div key={i} style={{
          height: '3px', flex: 1,
          background: i < filled ? 'var(--accent)' : 'var(--border)',
          boxShadow: i < filled ? '0 0 4px var(--accent-glow)' : 'none',
        }} />
      ))}
    </div>
  );
}

export default function PhaseModal({ phase, onClose }: Props) {
  const router = useRouter();
  const { isComplete, markComplete, markIncomplete, getPhaseProgress } = useProgress();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', esc);
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', esc); document.body.style.overflow = ''; };
  }, [onClose]);

  const paths   = phase.lessons.filter(l => l.path).map(l => l.path!);
  const prog    = getPhaseProgress(paths);
  const pct     = prog.percentage;

  return (
    <div
      onClick={e => { if (e.target === e.currentTarget) onClose(); }}
      style={{
        position: 'fixed', inset: 0, zIndex: 100,
        display: 'flex', alignItems: 'flex-end', justifyContent: 'center',
        background: 'var(--overlay-bg)',
        backdropFilter: 'blur(6px)',
      }}
    >
      <div ref={ref}
        style={{
          width: '100%', maxWidth: '680px', maxHeight: '82vh',
          overflowY: 'auto',
          background: 'var(--modal-bg)',
          borderTop: '2px solid var(--accent)',
          borderLeft: '1px solid var(--border)',
          borderRight: '1px solid var(--border)',
          boxShadow: '0 -4px 40px var(--accent-glow), 0 -1px 0 var(--accent)',
          padding: '28px 24px 32px',
        }}
        onClick={e => e.stopPropagation()}
      >
        {/* header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '18px' }}>
          <div style={{ flex: 1, paddingRight: '16px' }}>
            <div style={{
              fontFamily: 'var(--pixel-font)', fontSize: '8px',
              color: 'var(--accent)', letterSpacing: '0.5px',
              textShadow: '0 0 8px var(--accent-glow)',
              marginBottom: '6px',
            }}>
              PHASE {String(phase.id).padStart(2,'0')}
            </div>
            <h2 style={{ fontSize: '17px', fontWeight: '600', color: 'var(--text)', margin: '0 0 6px', lineHeight: 1.3 }}>
              {phase.name}
            </h2>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: 1.6, margin: 0 }}>
              {phase.desc.replace(/[*_~`]/g, '')}
            </p>
          </div>
          <button onClick={onClose}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: '2px', flexShrink: 0, transition: 'color 0.15s' }}
            onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent)')}
            onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
          >
            <X size={16} />
          </button>
        </div>

        {/* progress */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '10px', color: 'var(--text-dim)', fontFamily: 'var(--mono-font)' }}>
              {prog.completed}/{phase.lessons.length} complete
            </span>
            <span style={{
              fontSize: '10px', fontFamily: 'var(--pixel-font)',
              color: pct > 0 ? 'var(--accent)' : 'var(--text-dim)',
              textShadow: pct > 0 ? '0 0 6px var(--accent-glow)' : 'none',
            }}>
              {pct}%
            </span>
          </div>
          <SegBar pct={pct} />
        </div>

        {/* lesson list */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border-dim)' }}>
          {phase.lessons.map((lesson, i) => {
            const key     = keyOf(lesson);
            const route   = routeOf(lesson);
            /* ONLY check localStorage — never use lesson.status for "done" state */
            const done    = key ? isComplete(key) : false;
            const canRead = !!route;

            return (
              <div key={i}
                onClick={() => { if (canRead && route) { router.push(`/lessons/${route.phase}/${route.lesson}`); onClose(); } }}
                style={{
                  background: 'var(--bg-card)',
                  padding: '11px 14px',
                  display: 'flex', alignItems: 'center', gap: '12px',
                  cursor: canRead ? 'pointer' : 'default',
                  transition: 'background 0.1s, border-color 0.1s',
                  borderLeft: `3px solid ${done ? 'var(--complete)' : 'transparent'}`,
                }}
                onMouseEnter={e => { if (canRead) e.currentTarget.style.background = 'var(--bg-card-hover)'; }}
                onMouseLeave={e => { e.currentTarget.style.background = 'var(--bg-card)'; }}
              >
                {/* status square */}
                <div style={{
                  width: '8px', height: '8px', flexShrink: 0,
                  background: done ? 'var(--complete)' : 'var(--border)',
                  boxShadow: done ? '0 0 6px var(--complete-glow)' : 'none',
                }} />

                {/* index + name */}
                <span style={{ fontFamily: 'var(--mono-font)', fontSize: '10px', color: 'var(--text-dim)', flexShrink: 0, minWidth: '22px' }}>
                  {String(i + 1).padStart(2,'0')}
                </span>
                <span style={{
                  flex: 1, fontSize: '13px',
                  color: canRead ? '#d4c0a8' : 'var(--text-dim)',
                  overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                }}>
                  {lesson.name}
                </span>

                {/* type badge */}
                <span style={{
                  fontSize: '9px', fontFamily: 'var(--pixel-font)', letterSpacing: '0.3px',
                  padding: '2px 7px',
                  color: lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)',
                  border: `1px solid ${lesson.type === 'Build' ? 'rgba(114,184,48,0.3)' : 'var(--accent-border)'}`,
                  background: lesson.type === 'Build' ? 'var(--complete-dim)' : 'var(--accent-dim)',
                  boxShadow: lesson.type === 'Build' ? '0 0 4px var(--complete-glow)' : '0 0 4px var(--accent-glow)',
                  flexShrink: 0,
                }}>
                  {lesson.type.toUpperCase()}
                </span>

                {/* read label */}
                {canRead && (
                  <span style={{ fontSize: '10px', color: done ? 'var(--complete)' : 'var(--text-dim)', fontFamily: 'var(--pixel-font)', flexShrink: 0, textShadow: done ? '0 0 4px var(--complete-glow)' : 'none' }}>
                    {done ? '✓' : '▶'}
                  </span>
                )}

                {/* mark done toggle */}
                {key && (
                  <button
                    onClick={ev => { ev.stopPropagation(); done ? markIncomplete(key) : markComplete(key); }}
                    title={done ? 'Mark incomplete' : 'Mark complete'}
                    style={{
                      width: '18px', height: '18px', flexShrink: 0,
                      background: done ? 'var(--complete)' : 'transparent',
                      border: `1px solid ${done ? 'var(--complete)' : 'var(--border)'}`,
                      cursor: 'pointer',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '8px', color: done ? '#0b0806' : 'var(--text-dim)',
                      boxShadow: done ? '0 0 6px var(--complete-glow)' : 'none',
                      transition: 'all 0.15s',
                    }}
                    onMouseEnter={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; }}}
                    onMouseLeave={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-dim)'; }}}
                  >
                    {done ? '✓' : '□'}
                  </button>
                )}
              </div>
            );
          })}
        </div>

        {/* footer */}
        <div style={{ marginTop: '14px', display: 'flex', justifyContent: 'space-between', fontSize: '9px', color: 'var(--text-dim)', fontFamily: 'var(--pixel-font)', letterSpacing: '0.3px' }}>
          <span>PROGRESS SAVED IN BROWSER</span>
          <span>CLICK LESSON TO READ ▶</span>
        </div>
      </div>
    </div>
  );
}

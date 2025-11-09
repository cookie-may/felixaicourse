'use client';

import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { useRouter } from 'next/navigation';
import { Phase, Lesson } from '@/data/phases';
import { useProgress } from './ProgressProvider';
import { X } from 'lucide-react';

interface Props { phase: Phase; phaseIndex: number; onClose: () => void; }

function routeOf(lesson: Lesson): { phase: string; lesson: string } | null {
  if (!lesson.path) return null;
  const parts = lesson.path.split('/');
  if (parts.length !== 3) return null;
  return { phase: parts[1], lesson: parts[2] };
}

function keyOf(lesson: Lesson): string | null {
  return lesson.path ?? null;
}

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
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', esc);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', esc);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  const paths = phase.lessons.filter(l => l.path).map(l => l.path!);
  const prog  = getPhaseProgress(paths);
  const pct   = prog.percentage;

  if (!mounted) return null;

  return createPortal(
    <>
      {/* Backdrop */}
      <div
        onClick={onClose}
        style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          zIndex: 200,
          background: 'rgba(8,5,3,0.88)',
          backdropFilter: 'blur(6px)',
        }}
      />

      {/* Modal — centered via transform, never exceeds viewport */}
      <div
        ref={ref}
        onClick={e => e.stopPropagation()}
        style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          zIndex: 201,
          width: 'min(640px, calc(100vw - 48px))',
          height: 'min(680px, calc(100vh - 80px))',
          display: 'flex',
          flexDirection: 'column',
          background: 'var(--modal-bg)',
          border: '1px solid var(--border)',
          borderTop: '2px solid var(--accent)',
          boxShadow: '0 0 0 1px var(--border), 0 0 60px var(--accent-glow), 0 24px 64px rgba(0,0,0,0.8)',
        }}
      >
        {/* ── Header (fixed) ── */}
        <div style={{ padding: '20px 20px 16px', flexShrink: 0, borderBottom: '1px solid var(--border-dim)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
            <div style={{ flex: 1, paddingRight: '12px' }}>
              <div style={{
                fontFamily: 'var(--pixel-font)', fontSize: '8px',
                color: 'var(--accent)', letterSpacing: '0.5px',
                textShadow: '0 0 8px var(--accent-glow)', marginBottom: '6px',
              }}>
                PHASE {String(phase.id).padStart(2, '0')}
              </div>
              <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--text)', margin: '0 0 4px', lineHeight: 1.3 }}>
                {phase.name}
              </h2>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: 1.6, margin: 0 }}>
                {phase.desc.replace(/[*_~`]/g, '')}
              </p>
            </div>
            <button
              onClick={onClose}
              style={{
                background: 'none', border: 'none', cursor: 'pointer',
                color: 'var(--text-muted)', padding: '4px', flexShrink: 0,
                transition: 'color 0.15s', display: 'flex',
              }}
              onMouseEnter={e => (e.currentTarget.style.color = 'var(--accent)')}
              onMouseLeave={e => (e.currentTarget.style.color = 'var(--text-muted)')}
            >
              <X size={16} />
            </button>
          </div>

          {/* Progress */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
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
        </div>

        {/* ── Lesson list (scrollable) ── */}
        <div style={{ flex: 1, overflowY: 'auto', minHeight: 0 }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border-dim)' }}>
            {phase.lessons.map((lesson, i) => {
              const key     = keyOf(lesson);
              const route   = routeOf(lesson);
              const done    = key ? isComplete(key) : false;
              const canRead = !!route;

              return (
                <div
                  key={i}
                  onClick={() => { if (canRead && route) { router.push(`/lessons/${route.phase}/${route.lesson}`); onClose(); } }}
                  style={{
                    background: 'var(--bg-card)',
                    padding: '10px 14px',
                    display: 'flex', alignItems: 'center', gap: '10px',
                    cursor: canRead ? 'pointer' : 'default',
                    borderLeft: `3px solid ${done ? 'var(--complete)' : 'transparent'}`,
                    transition: 'background 0.1s',
                  }}
                  onMouseEnter={e => { if (canRead) e.currentTarget.style.background = 'var(--bg-card-hover)'; }}
                  onMouseLeave={e => { e.currentTarget.style.background = 'var(--bg-card)'; }}
                >
                  <div style={{
                    width: '7px', height: '7px', flexShrink: 0,
                    background: done ? 'var(--complete)' : 'var(--border)',
                    boxShadow: done ? '0 0 5px var(--complete-glow)' : 'none',
                  }} />
                  <span style={{ fontFamily: 'var(--mono-font)', fontSize: '10px', color: 'var(--text-dim)', flexShrink: 0, minWidth: '20px' }}>
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <span style={{
                    flex: 1, fontSize: '13px',
                    color: canRead ? '#d4c0a8' : 'var(--text-dim)',
                    overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                  }}>
                    {lesson.name}
                  </span>
                  <span style={{
                    fontSize: '8px', fontFamily: 'var(--pixel-font)',
                    padding: '2px 6px', flexShrink: 0,
                    color: lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)',
                    border: `1px solid ${lesson.type === 'Build' ? 'rgba(114,184,48,0.3)' : 'var(--accent-border)'}`,
                    background: lesson.type === 'Build' ? 'var(--complete-dim)' : 'var(--accent-dim)',
                  }}>
                    {lesson.type.toUpperCase()}
                  </span>
                  {canRead && (
                    <span style={{
                      fontSize: '11px', fontFamily: 'var(--pixel-font)', flexShrink: 0,
                      color: done ? 'var(--complete)' : '#ffffff',
                      textShadow: done ? '0 0 6px var(--complete-glow)' : '0 0 4px rgba(255,255,255,0.4)',
                    }}>
                      {done ? '✓' : '▶'}
                    </span>
                  )}
                  {key && (
                    <button
                      onClick={ev => { ev.stopPropagation(); done ? markIncomplete(key) : markComplete(key); }}
                      title={done ? 'Mark incomplete' : 'Mark complete'}
                      style={{
                        width: '20px', height: '20px', flexShrink: 0,
                        background: done ? 'var(--complete)' : 'rgba(255,255,255,0.08)',
                        border: `1px solid ${done ? 'var(--complete)' : 'rgba(255,255,255,0.35)'}`,
                        cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: '10px', color: done ? '#0b0806' : '#ffffff',
                        fontWeight: 700,
                        boxShadow: done ? '0 0 6px var(--complete-glow)' : 'none',
                        transition: 'all 0.15s',
                      }}
                      onMouseEnter={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.background = 'rgba(232,108,44,0.12)'; } }}
                      onMouseLeave={e => { if (!done) { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.35)'; e.currentTarget.style.color = '#ffffff'; e.currentTarget.style.background = 'rgba(255,255,255,0.08)'; } }}
                    >
                      {done ? '✓' : '□'}
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* ── Footer (fixed) ── */}
        <div style={{
          padding: '10px 20px',
          borderTop: '1px solid var(--border-dim)',
          flexShrink: 0,
          display: 'flex', justifyContent: 'space-between',
          fontSize: '8px', color: 'var(--text-dim)',
          fontFamily: 'var(--pixel-font)', letterSpacing: '0.3px',
        }}>
          <span>PROGRESS SAVED IN BROWSER</span>
          <span>CLICK LESSON TO READ ▶</span>
        </div>
      </div>
    </>,
    document.body
  );
}

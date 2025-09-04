'use client';

import { useEffect, useState, useRef } from 'react';
import Image from 'next/image';
import { PHASES, getTotalLessons } from '@/data/phases';
import { useProgress } from '@/components/ProgressProvider';
import PhaseModal from '@/components/PhaseModal';

/* ── ticker items ─────────────────────────────────────────── */
const TICKS = [
  'Math Foundations','Deep Learning','Transformers','LLMs from Scratch',
  'Agent Engineering','Multi-Agent Swarms','Production AI','Computer Vision',
  'NLP','Reinforcement Learning','Generative AI','Speech & Audio','Ethics',
  'Math Foundations','Deep Learning','Transformers','LLMs from Scratch',
  'Agent Engineering','Multi-Agent Swarms','Production AI','Computer Vision',
  'NLP','Reinforcement Learning','Generative AI','Speech & Audio','Ethics',
];

/* ── lang color map ───────────────────────────────────────── */
const LANG_CLR: Record<string, { bg: string; color: string; glow: string }> = {
  Python:     { bg: '#141e08', color: '#7ab648', glow: 'rgba(122,182,72,0.35)' },
  TS:         { bg: '#08121e', color: '#378add', glow: 'rgba(55,138,221,0.35)' },
  TypeScript: { bg: '#08121e', color: '#378add', glow: 'rgba(55,138,221,0.35)' },
  Rust:       { bg: '#1e0c08', color: '#d85a30', glow: 'rgba(216,90,48,0.35)'  },
  Julia:      { bg: '#081414', color: '#1d9e75', glow: 'rgba(29,158,117,0.35)' },
};

function phaseLangs(phase: typeof PHASES[0]) {
  const seen = new Set<string>();
  phase.lessons.forEach(l =>
    l.lang.split(',').forEach(x => {
      const t = x.trim();
      if (t && t !== '—') seen.add(t === 'TypeScript' ? 'TS' : t);
    })
  );
  return Array.from(seen).slice(0, 3);
}

/* ── animated counter ─────────────────────────────────────── */
function Counter({ to }: { to: number }) {
  const [v, setV] = useState(0);
  const ran = useRef(false);
  useEffect(() => {
    if (ran.current) return;
    ran.current = true;
    let t: number;
    const tick = (ts: number, start: number) => {
      const p = Math.min((ts - start) / 1000, 1);
      setV(Math.round((1 - Math.pow(1 - p, 3)) * to));
      if (p < 1) t = requestAnimationFrame(ts2 => tick(ts2, start));
    };
    t = requestAnimationFrame(ts => tick(ts, ts));
    return () => cancelAnimationFrame(t);
  }, [to]);
  return <>{v}</>;
}

/* ── segmented progress bar ───────────────────────────────── */
function SegBar({ pct, full = false }: { pct: number; full?: boolean }) {
  const N = full ? 16 : 10;
  const filled = Math.floor(pct / (100 / N));
  return (
    <div className="seg-bar">
      {Array.from({ length: N }).map((_, i) => (
        <div key={i} className={`seg ${i < filled ? (full ? 'filled-complete' : 'filled') : ''}`} />
      ))}
    </div>
  );
}

/* ── feature card data ────────────────────────────────────── */
const FEATS = [
  { icon: '⚙', title: 'Build, don\'t import', desc: 'Implement every algorithm from raw math. You write the backprop, the tokenizer, the attention.' },
  { icon: '⌨', title: 'Real code, real projects', desc: 'Python, TypeScript, Rust, Julia. Every lesson has runnable code. No slides, no theory-only.' },
  { icon: '✦', title: 'Ship something reusable', desc: 'Each lesson produces a prompt, skill, agent, or MCP server. Your toolkit grows every phase.' },
  { icon: '◎', title: 'Free & open source', desc: 'MIT licensed. Clone it, fork it, learn at your own pace. No paywall, no gatekeeping.' },
];

/* ═══════════════════════════════════════════════════════════ */
export default function HomePage() {
  const [sel, setSel] = useState<number | null>(null);
  const [mounted, setMounted] = useState(false);
  const { completedLessons, getPhaseProgress } = useProgress();

  useEffect(() => { setMounted(true); }, []);

  const total    = getTotalLessons();
  const userDone = mounted ? completedLessons.size : 0;
  const overallPct = total > 0 && userDone > 0 ? Math.round((userDone / total) * 100) : 0;

  return (
    <div style={{ paddingTop: '68px', minHeight: '100vh' }}>

      {/* ── HERO ─────────────────────────────────────────── */}
      <section style={{
        padding: 'clamp(48px,8vw,88px) 1.5rem clamp(48px,6vw,72px)',
        textAlign: 'center',
        borderBottom: '1px solid var(--border)',
        position: 'relative',
      }}>
        {/* corner decorations */}
        <div style={{ position: 'absolute', top: 0, left: 0, width: '40px', height: '40px', borderTop: '2px solid var(--accent)', borderLeft: '2px solid var(--accent)', boxShadow: '-2px -2px 8px var(--accent-glow)' }} />
        <div style={{ position: 'absolute', top: 0, right: 0, width: '40px', height: '40px', borderTop: '2px solid var(--accent)', borderRight: '2px solid var(--accent)', boxShadow: '2px -2px 8px var(--accent-glow)' }} />

        <div style={{ maxWidth: '680px', margin: '0 auto' }}>
          {/* badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '8px',
            background: 'var(--accent-dim)', border: '1px solid var(--accent-border)',
            color: 'var(--accent)', fontSize: '10px',
            fontFamily: 'var(--pixel-font)', letterSpacing: '0.5px',
            padding: '6px 14px', marginBottom: '28px',
          }}>
            <div style={{ width: '5px', height: '5px', background: 'var(--accent)', boxShadow: '0 0 6px var(--accent-glow)' }} />
            OPEN SOURCE · MIT · ~290H
          </div>

          {/* pixel cat logo */}
          <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '24px' }}>
            <Image
              src="/logo.png" alt="felix" width={88} height={88}
              className="logo-glow"
              style={{ borderRadius: '8px' }}
            />
          </div>

          {/* headline */}
          <h1 style={{ margin: '0 0 16px', lineHeight: 1.2 }}>
            <span style={{
              display: 'block',
              fontFamily: 'var(--pixel-font)',
              fontSize: 'clamp(14px,3vw,20px)',
              color: 'var(--text)',
              letterSpacing: '1px',
              marginBottom: '8px',
            }}>
              LEARN AI.
            </span>
            <span style={{
              display: 'block',
              fontFamily: 'var(--pixel-font)',
              fontSize: 'clamp(14px,3vw,20px)',
              color: 'var(--accent)',
              textShadow: '0 0 12px var(--accent-glow), 0 0 36px rgba(232,108,44,0.3)',
              letterSpacing: '1px',
            }}>
              BUILD IT. SHIP IT.
            </span>
          </h1>

          <p style={{ fontSize: '14px', color: 'var(--text-muted)', maxWidth: '440px', margin: '0 auto 36px', lineHeight: 1.75 }}>
            260+ lessons across 20 phases. From linear algebra to autonomous agent swarms.
            Python, TypeScript, Rust, Julia.
          </p>

          {/* stats */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: 'clamp(24px,5vw,52px)', marginBottom: '36px', flexWrap: 'wrap' }}>
            {[
              { val: total,    suffix: '+', label: 'LESSONS',   anim: true  },
              { val: 20,       suffix: '',  label: 'PHASES',    anim: false },
              { val: 4,        suffix: '',  label: 'LANGUAGES', anim: false },
              { val: userDone, suffix: '',  label: 'DONE',      anim: true  },
            ].map((s, i) => (
              <div key={i} style={{ textAlign: 'center' }}>
                <div style={{
                  fontFamily: 'var(--pixel-font)',
                  fontSize: 'clamp(12px,2.5vw,18px)',
                  color: i === 3 && userDone > 0 ? 'var(--complete)' : 'var(--accent)',
                  textShadow: i === 3 && userDone > 0
                    ? '0 0 10px var(--complete-glow)'
                    : '0 0 10px var(--accent-glow)',
                  marginBottom: '6px',
                  letterSpacing: '1px',
                }}>
                  {s.anim ? <Counter to={s.val} /> : s.val}{s.suffix}
                </div>
                <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '7px', color: 'var(--text-dim)', letterSpacing: '1px' }}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>

          {/* CTAs */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
            <a href="#phases" className="btn-primary">▶ EXPLORE PHASES</a>
            <a href="https://github.com/cookie-may/felixforlearnai" target="_blank" rel="noopener noreferrer"
              className="btn-ghost">⭐ STAR ON GITHUB</a>
          </div>
        </div>
      </section>

      {/* ── TICKER ───────────────────────────────────────── */}
      <div style={{ overflow: 'hidden', borderBottom: '1px solid var(--border)', background: 'var(--bg-surface)' }}>
        <div className="ticker-track">
          {TICKS.map((t, i) => (
            <span key={i} style={{
              fontSize: '9px', fontFamily: 'var(--pixel-font)',
              color: 'var(--text-dim)', padding: '10px 0',
              display: 'inline-flex', alignItems: 'center',
            }}>
              <span style={{
                color: 'var(--accent)', margin: '0 14px 0 14px',
                textShadow: '0 0 6px var(--accent-glow)',
              }}>▸</span>
              {t.toUpperCase()}
            </span>
          ))}
        </div>
      </div>

      {/* ── PHASES GRID ──────────────────────────────────── */}
      <section id="phases" style={{ padding: '48px 1.5rem' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
          {/* section header */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ width: '3px', height: '18px', background: 'var(--accent)', boxShadow: '0 0 8px var(--accent-glow)' }} />
              <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '13px', color: 'var(--accent)', textShadow: '0 0 8px var(--accent-glow)', letterSpacing: '0.5px' }}>
                THE 20 PHASES
              </span>
            </div>
            <span style={{ fontSize: '7px', color: 'var(--text-dim)', fontFamily: 'var(--pixel-font)' }}>
              CLICK TO EXPLORE →
            </span>
          </div>

          {/* grid */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(178px, 1fr))',
            gap: '2px',
            background: 'var(--border-dim)',
            border: '1px solid var(--border)',
          }}>
            {PHASES.map((phase, idx) => {
              const paths = phase.lessons.filter(l => l.path).map(l => l.path!);
              const prog  = getPhaseProgress(paths);
              const pct   = mounted ? prog.percentage : 0;
              const langs = phaseLangs(phase);

              return (
                <div key={phase.id} className="phase-card" onClick={() => setSel(idx)}
                  style={{ padding: '16px' }}>
                  {/* phase number */}
                  <div style={{
                    fontFamily: 'var(--pixel-font)', fontSize: '8px',
                    color: 'var(--accent)',
                    textShadow: pct === 100 ? '0 0 8px var(--complete-glow)' : '0 0 6px var(--accent-glow)',
                    marginBottom: '8px', letterSpacing: '0.5px',
                  }}>
                    {pct === 100 ? '✓' : '□'} PH{String(phase.id).padStart(2,'0')}
                  </div>

                  {/* name */}
                  <div style={{ fontSize: '14px', color: '#d4c0a8', fontWeight: '500', marginBottom: '10px', lineHeight: 1.35 }}>
                    {phase.name}
                  </div>

                  {/* seg progress bar */}
                  <SegBar pct={pct} />

                  {/* lesson count */}
                  <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '6px', marginBottom: '8px', fontFamily: 'var(--mono-font)' }}>
                    {mounted && prog.completed > 0
                      ? <span><span style={{ color: 'var(--complete)', textShadow: '0 0 6px var(--complete-glow)' }}>{prog.completed}</span>/{phase.lessons.length}</span>
                      : `${phase.lessons.length} lessons`
                    }
                  </div>

                  {/* lang pills */}
                  <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap' }}>
                    {langs.map(l => {
                      const c = LANG_CLR[l] ?? { bg: 'var(--bg)', color: 'var(--text-dim)', glow: 'transparent' };
                      return (
                        <span key={l} style={{
                          fontSize: '9px', padding: '1px 6px',
                          background: c.bg, color: c.color,
                          border: `1px solid ${c.color}22`,
                        }}>
                          {l}
                        </span>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── WHY ──────────────────────────────────────────── */}
      <section style={{ padding: '0 1.5rem 48px', borderTop: '1px solid var(--border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', paddingTop: '48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <div style={{ width: '3px', height: '18px', background: 'var(--accent)', boxShadow: '0 0 8px var(--accent-glow)' }} />
            <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '13px', color: 'var(--accent)', textShadow: '0 0 8px var(--accent-glow)', letterSpacing: '0.5px' }}>
              WHY THIS COURSE
            </span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '2px', background: 'var(--border-dim)' }}>
            {FEATS.map(f => (
              <div key={f.title} style={{ background: 'var(--bg-card)', padding: '20px 18px', border: '0 none' }}>
                <div style={{ fontSize: '18px', marginBottom: '10px', color: 'var(--accent)', textShadow: '0 0 10px var(--accent-glow)' }}>{f.icon}</div>
                <div style={{ fontSize: '14px', fontWeight: '600', color: '#d4c0a8', marginBottom: '7px' }}>{f.title}</div>
                <div style={{ fontSize: '14px', color: 'var(--text-muted)', lineHeight: 1.6 }}>{f.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── ROADMAP ──────────────────────────────────────── */}
      <section id="roadmap" style={{ padding: '0 1.5rem 48px', borderTop: '1px solid var(--border)' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', paddingTop: '48px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <div style={{ width: '3px', height: '18px', background: 'var(--accent)', boxShadow: '0 0 8px var(--accent-glow)' }} />
            <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '13px', color: 'var(--accent)', textShadow: '0 0 8px var(--accent-glow)', letterSpacing: '0.5px' }}>
              ROADMAP
            </span>
          </div>

          {/* overall bar */}
          <div style={{ marginBottom: '24px', paddingLeft: '13px' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-dim)', marginBottom: '6px', fontFamily: 'var(--mono-font)' }}>
              overall progress — {userDone}/{total} lessons
              {mounted && overallPct > 0 && (
                <span style={{ color: 'var(--accent)', marginLeft: '8px', textShadow: '0 0 6px var(--accent-glow)' }}>
                  [{overallPct}%]
                </span>
              )}
            </div>
            <SegBar pct={overallPct} full />
          </div>

          {/* phase pills */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px,1fr))', gap: '2px', background: 'var(--border-dim)' }}>
            {PHASES.map(phase => {
              const paths = phase.lessons.filter(l => l.path).map(l => l.path!);
              const prog  = mounted ? getPhaseProgress(paths) : { completed: 0, total: paths.length, percentage: 0 };
              const done  = mounted && prog.completed === prog.total && prog.total > 0;

              return (
                <div key={phase.id} onClick={() => setSel(PHASES.indexOf(phase))}
                  style={{
                    background: 'var(--bg-card)', padding: '10px 12px',
                    display: 'flex', alignItems: 'center', gap: '10px',
                    cursor: 'pointer', transition: 'background 0.15s',
                  }}
                  onMouseEnter={e => (e.currentTarget.style.background = 'var(--bg-card-hover)')}
                  onMouseLeave={e => (e.currentTarget.style.background = 'var(--bg-card)')}
                >
                  <div style={{
                    width: '6px', height: '6px', flexShrink: 0,
                    background: done ? 'var(--complete)' : 'var(--planned)',
                    boxShadow: done ? '0 0 6px var(--complete-glow)' : 'none',
                  }} />
                  <span style={{ fontSize: '10px', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--mono-font)' }}>
                    <span style={{ color: 'var(--text-dim)', marginRight: '4px' }}>
                      {String(phase.id).padStart(2,'0')}
                    </span>
                    {phase.name}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────── */}
      <section style={{ padding: '0 1.5rem 56px', borderTop: '1px solid var(--border)' }}>
        <div style={{
          maxWidth: '1280px', margin: '48px auto 0',
          background: 'var(--bg-card)',
          border: '1px solid var(--border)',
          padding: '36px 32px',
          textAlign: 'center',
          position: 'relative',
        }}>
          {/* corner accents */}
          {[['top','left'],['top','right'],['bottom','left'],['bottom','right']].map(([v,h]) => (
            <div key={`${v}${h}`} style={{
              position: 'absolute', [v]: '-1px', [h]: '-1px',
              width: '12px', height: '12px',
              borderTop: v === 'top' ? '2px solid var(--accent)' : 'none',
              borderBottom: v === 'bottom' ? '2px solid var(--accent)' : 'none',
              borderLeft: h === 'left' ? '2px solid var(--accent)' : 'none',
              borderRight: h === 'right' ? '2px solid var(--accent)' : 'none',
              boxShadow: '0 0 6px var(--accent-glow)',
            }} />
          ))}

          <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '12px', color: 'var(--accent)', textShadow: '0 0 12px var(--accent-glow)', marginBottom: '10px' }}>
            START BUILDING
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-dim)', marginBottom: '20px' }}>
            Everything is open source and free. No account required.
          </p>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '12px',
            background: 'var(--code-bg)', border: '1px solid var(--border)',
            borderLeft: '3px solid var(--accent)',
            padding: '10px 16px', marginBottom: '24px',
            fontFamily: 'var(--mono-font)', fontSize: '12px', color: 'var(--accent)',
            textShadow: '0 0 8px rgba(232,108,44,0.3)',
          }}>
            git clone https://github.com/cookie-may/felixforlearnai
          </div>
          <div>
            <a href="#phases" className="btn-primary">▶ BROWSE PHASES</a>
          </div>
        </div>
      </section>

      {/* Modal */}
      {sel !== null && (
        <PhaseModal phase={PHASES[sel]} phaseIndex={sel} onClose={() => setSel(null)} />
      )}
    </div>
  );
}

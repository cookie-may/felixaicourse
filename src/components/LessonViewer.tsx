'use client';

import dynamic from 'next/dynamic';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { useProgress } from '@/components/ProgressProvider';
import { PHASES } from '@/data/phases';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';

const MermaidBlock = dynamic(() => import('@/components/MermaidBlock'), { ssr: false });

interface Props { phaseSlug: string; lessonSlug: string; initialContent: string; }

function GHIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
    </svg>
  );
}

function findMeta(phaseSlug: string, lessonSlug: string) {
  const lessonPath = `phases/${phaseSlug}/${lessonSlug}`;
  for (const phase of PHASES) {
    const lesson = phase.lessons.find(l => l.path === lessonPath);
    if (lesson) return { phase, lesson };
  }
  return null;
}

function flatLessons() {
  const list: { path: string; phaseName: string; lessonName: string; phaseSlug: string; lessonSlug: string }[] = [];
  PHASES.forEach(phase => {
    phase.lessons.forEach(lesson => {
      if (lesson.path) {
        const parts = lesson.path.split('/');
        if (parts.length === 3) {
          list.push({
            path: lesson.path,
            phaseName: phase.name,
            lessonName: lesson.name,
            phaseSlug: parts[1],
            lessonSlug: parts[2],
          });
        }
      }
    });
  });
  return list;
}

/* ReactMarkdown custom components — mermaid code blocks → MermaidBlock */
const mdComponents: Components = {
  code({ className, children, ...rest }) {
    const lang = /language-(\w+)/.exec(className ?? '')?.[1];
    const code = String(children).replace(/\n$/, '');
    if (lang === 'mermaid') return <MermaidBlock code={code} />;
    /* check if inside a pre (block code) or inline */
    return (
      <code className={className} {...rest}>
        {children}
      </code>
    );
  },
};

export default function LessonViewer({ phaseSlug, lessonSlug, initialContent }: Props) {
  const router = useRouter();
  const { isComplete, markComplete, markIncomplete } = useProgress();

  const lessonPath = `phases/${phaseSlug}/${lessonSlug}`;
  const done       = isComplete(lessonPath);
  const meta       = findMeta(phaseSlug, lessonSlug);
  const all        = flatLessons();
  const idx        = all.findIndex(l => l.path === lessonPath);
  const prev       = idx > 0 ? all[idx - 1] : null;
  const next       = idx < all.length - 1 ? all[idx + 1] : null;

  const ghUrl = `https://github.com/cookie-may/felixforlearnai/tree/main/public/${lessonPath}`;

  const iconBtn: React.CSSProperties = {
    display: 'flex', alignItems: 'center', gap: '5px',
    fontSize: '10px', fontFamily: 'var(--pixel-font)', letterSpacing: '0.3px',
    color: 'var(--text-muted)',
    background: 'var(--bg-card)',
    border: '1px solid var(--border)',
    padding: '6px 11px',
    cursor: 'pointer', textDecoration: 'none',
    transition: 'border-color 0.15s, color 0.15s, box-shadow 0.15s',
  };

  const noContent = !initialContent;

  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh', paddingTop: '68px' }}>

      {/* ── sub-header ─────────────────────────────────── */}
      <div style={{
        position: 'sticky', top: '68px', zIndex: 40,
        background: 'var(--header-bg)', backdropFilter: 'blur(14px)',
        borderBottom: '1px solid var(--border)',
        padding: '0 1.5rem', height: '48px',
        display: 'flex', alignItems: 'center',
      }}>
        <div style={{
          maxWidth: '860px', width: '100%', margin: '0 auto',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px',
        }}>
          <button onClick={() => router.back()} style={{ ...iconBtn, flexShrink: 0 }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 6px var(--accent-glow)'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.boxShadow = 'none'; }}
          >
            <ArrowLeft size={11} /> BACK
          </button>

          {meta && (
            <div style={{ flex: 1, textAlign: 'center', overflow: 'hidden' }}>
              <span style={{ fontSize: '9px', fontFamily: 'var(--pixel-font)', color: 'var(--accent)', textShadow: '0 0 6px var(--accent-glow)', letterSpacing: '0.3px' }}>
                PH{String(meta.phase.id).padStart(2,'0')}
              </span>
              <span style={{ fontSize: '9px', color: 'var(--text-dim)', margin: '0 6px' }}>›</span>
              <span style={{ fontSize: '13px', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {meta.lesson.name}
              </span>
            </div>
          )}

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexShrink: 0 }}>
            <a href={ghUrl} target="_blank" rel="noopener noreferrer"
              style={iconBtn}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--accent)'; (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; }}
            >
              <GHIcon /> SRC
            </a>

            <button
              onClick={() => done ? markIncomplete(lessonPath) : markComplete(lessonPath)}
              style={{
                ...iconBtn,
                borderColor: done ? 'var(--complete)' : 'var(--border)',
                color: done ? 'var(--complete)' : 'var(--text-muted)',
                background: done ? 'var(--complete-dim)' : 'var(--bg-card)',
                boxShadow: done ? '0 0 8px var(--complete-glow)' : 'none',
              }}
              onMouseEnter={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 6px var(--accent-glow)'; }}}
              onMouseLeave={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.boxShadow = 'none'; }}}
            >
              {done ? '✓ DONE' : '□ MARK DONE'}
            </button>
          </div>
        </div>
      </div>

      {/* ── content ────────────────────────────────────── */}
      <div style={{ maxWidth: '860px', margin: '0 auto', padding: '36px 1.5rem 80px' }}>

        {noContent && (
          <div style={{
            background: 'var(--bg-card)', border: '1px solid var(--border)',
            borderTop: '2px solid var(--accent)', padding: '40px 32px', textAlign: 'center',
          }}>
            <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '10px', color: 'var(--accent)', textShadow: '0 0 10px var(--accent-glow)', marginBottom: '12px' }}>
              CONTENT NOT FOUND
            </div>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', marginBottom: '20px' }}>
              Make sure{' '}
              <code style={{ fontFamily: 'var(--mono-font)', color: 'var(--accent)' }}>
                public/phases/{phaseSlug}/{lessonSlug}/docs/en.md
              </code>{' '}
              exists.
            </p>
            <a href={ghUrl} target="_blank" rel="noopener noreferrer" className="btn-ghost" style={{ fontSize: '11px' }}>
              VIEW ON GITHUB ↗
            </a>
          </div>
        )}

        {!noContent && (
          <>
            {/* lesson metadata bar */}
            {meta && (
              <div style={{
                display: 'flex', gap: '24px', flexWrap: 'wrap',
                marginBottom: '28px', paddingBottom: '16px',
                borderBottom: '1px solid var(--border)',
              }}>
                {[
                  { label: 'PHASE',  val: `${String(meta.phase.id).padStart(2,'0')} · ${meta.phase.name}` },
                  { label: 'TYPE',   val: meta.lesson.type },
                  { label: 'LANG',   val: meta.lesson.lang },
                ].map(item => (
                  <div key={item.label}>
                    <div style={{ fontSize: '8px', fontFamily: 'var(--pixel-font)', color: 'var(--text-dim)', letterSpacing: '0.5px', marginBottom: '4px' }}>
                      {item.label}
                    </div>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', fontFamily: 'var(--mono-font)' }}>
                      {item.val}
                    </div>
                  </div>
                ))}

                {done && (
                  <div style={{ marginLeft: 'auto' }}>
                    <span style={{
                      fontFamily: 'var(--pixel-font)', fontSize: '8px',
                      color: 'var(--complete)', letterSpacing: '0.5px',
                      background: 'var(--complete-dim)',
                      border: '1px solid rgba(114,184,48,0.3)',
                      padding: '4px 10px',
                      boxShadow: '0 0 8px var(--complete-glow)',
                    }}>
                      ✓ COMPLETE
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* rendered markdown — mermaid blocks auto-rendered */}
            <div className="lesson-prose">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>
                {initialContent}
              </ReactMarkdown>
            </div>

            {/* mark-complete CTA */}
            {!done && (
              <div style={{
                marginTop: '40px', padding: '20px 24px',
                background: 'var(--accent-dim)',
                border: '1px solid var(--accent-border)',
                borderLeft: '3px solid var(--accent)',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap',
              }}>
                <span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>
                  Finished reading? Mark this lesson complete to track your progress.
                </span>
                <button onClick={() => markComplete(lessonPath)} className="btn-primary" style={{ fontSize: '11px', padding: '8px 18px' }}>
                  ✓ MARK COMPLETE
                </button>
              </div>
            )}

            {/* prev / next */}
            <div style={{
              marginTop: '40px', paddingTop: '24px',
              borderTop: '1px solid var(--border)',
              display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px',
            }}>
              {prev ? (
                <button onClick={() => router.push(`/lessons/${prev.phaseSlug}/${prev.lessonSlug}`)}
                  style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', padding: '14px 16px', cursor: 'pointer', textAlign: 'left', transition: 'border-color 0.15s, box-shadow 0.15s' }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 8px var(--accent-glow)'; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none'; }}
                >
                  <div style={{ fontSize: '8px', fontFamily: 'var(--pixel-font)', color: 'var(--text-dim)', marginBottom: '5px', letterSpacing: '0.3px' }}>◀ PREVIOUS</div>
                  <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{prev.lessonName}</div>
                </button>
              ) : <div />}

              {next ? (
                <button onClick={() => router.push(`/lessons/${next.phaseSlug}/${next.lessonSlug}`)}
                  style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', padding: '14px 16px', cursor: 'pointer', textAlign: 'right', transition: 'border-color 0.15s, box-shadow 0.15s' }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 8px var(--accent-glow)'; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none'; }}
                >
                  <div style={{ fontSize: '8px', fontFamily: 'var(--pixel-font)', color: 'var(--text-dim)', marginBottom: '5px', letterSpacing: '0.3px' }}>NEXT ▶</div>
                  <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>{next.lessonName}</div>
                </button>
              ) : (
                <button
                  onClick={() => { markComplete(lessonPath); router.push('/'); }}
                  style={{ background: 'var(--accent-dim)', border: '1px solid var(--accent-border)', padding: '14px 16px', cursor: 'pointer', textAlign: 'right', boxShadow: '0 0 10px var(--accent-glow)' }}
                >
                  <div style={{ fontSize: '8px', fontFamily: 'var(--pixel-font)', color: 'var(--accent)', marginBottom: '5px', letterSpacing: '0.3px', textShadow: '0 0 6px var(--accent-glow)' }}>🎉 LAST LESSON</div>
                  <div style={{ fontSize: '13px', color: 'var(--accent)' }}>Finish & go home</div>
                </button>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

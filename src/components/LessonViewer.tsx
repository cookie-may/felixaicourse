'use client';

import dynamic from 'next/dynamic';
import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { useProgress } from '@/components/ProgressProvider';
import { PHASES } from '@/data/phases';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Components } from 'react-markdown';
import type { OutputFile, CodeFile, QuizQuestion } from '@/app/lessons/[phase]/[lesson]/page';

const MermaidBlock = dynamic(() => import('@/components/MermaidBlock'), { ssr: false });

interface Props {
  phaseSlug: string;
  lessonSlug: string;
  initialContent: string;
  outputs: OutputFile[];
  codeFiles: CodeFile[];
  quiz: { questions: QuizQuestion[] } | null;
}

/* ── helpers ──────────────────────────────────────────────── */
function GHIcon({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
    </svg>
  );
}

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  return `${(bytes / 1024).toFixed(1)} KB`;
}

const LANG_ICON: Record<string, string> = {
  py: '🐍', ts: '🟦', tsx: '🟦', js: '🟨', rs: '🦀', jl: '🟣', sh: '🐚', md: '📄',
};

function runCmd(phaseSlug: string, lessonSlug: string, filename: string, ext: string) {
  const fp = `phases/${phaseSlug}/${lessonSlug}/code/${filename}`;
  switch (ext) {
    case 'py': return `python ${fp}`;
    case 'ts': return `npx ts-node ${fp}`;
    case 'js': return `node ${fp}`;
    case 'rs': return `cargo run --manifest-path phases/${phaseSlug}/${lessonSlug}/Cargo.toml`;
    case 'jl': return `julia ${fp}`;
    case 'sh': return `bash ${fp}`;
    default:   return `cat ${fp}`;
  }
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
  const list: { path: string; lessonName: string; phaseSlug: string; lessonSlug: string }[] = [];
  PHASES.forEach(phase => {
    phase.lessons.forEach(lesson => {
      if (lesson.path) {
        const parts = lesson.path.split('/');
        if (parts.length === 3) {
          list.push({ path: lesson.path, lessonName: lesson.name, phaseSlug: parts[1], lessonSlug: parts[2] });
        }
      }
    });
  });
  return list;
}

/* ── ReactMarkdown mermaid integration ──────────────────────── */
const mdComponents: Components = {
  code({ className, children }) {
    const lang = /language-(\w+)/.exec(className ?? '')?.[1];
    const code = String(children).replace(/\n$/, '');
    if (lang === 'mermaid') return <MermaidBlock code={code} />;
    return <code className={className}>{children}</code>;
  },
};

/* ── Section wrapper ────────────────────────────────────────── */
function SectionCard({ icon, title, subtitle, children }: { icon: string; title: string; subtitle?: string; children: React.ReactNode }) {
  return (
    <div style={{
      marginTop: '40px',
      border: '1px solid var(--border)',
      borderTop: '3px solid var(--accent)',
      background: 'var(--bg-card)',
      boxShadow: '0 0 16px rgba(232,108,44,0.05)',
    }}>
      <div style={{ padding: '18px 20px 14px', borderBottom: '1px solid var(--border-dim)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span style={{ fontSize: '20px' }}>{icon}</span>
          <div>
            <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '10px', color: 'var(--accent)', letterSpacing: '0.5px', textShadow: '0 0 8px var(--accent-glow)' }}>
              {title}
            </div>
            {subtitle && (
              <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '3px' }}>{subtitle}</div>
            )}
          </div>
        </div>
      </div>
      <div style={{ padding: '16px 20px 20px' }}>{children}</div>
    </div>
  );
}

/* ── Outputs section ────────────────────────────────────────── */
function OutputsSection({ outputs, phaseSlug, lessonSlug }: { outputs: OutputFile[]; phaseSlug: string; lessonSlug: string }) {
  const [copied, setCopied] = useState<string | null>(null);

  const copy = useCallback((key: string, text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 2000);
    }).catch(() => {});
  }, []);

  return (
    <SectionCard icon="📦" title="WHAT THIS LESSON SHIPS" subtitle="Prompts, skills, and artifacts you can use right now">
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {outputs.map(out => {
          const ghLink = `https://github.com/cookie-may/felixforlearnai/tree/main/public/phases/${phaseSlug}/${lessonSlug}/outputs/${out.filename}`;
          const isCopied = copied === out.filename;
          const typeLabel = out.filename.startsWith('skill-') ? 'SKILL' : out.filename.startsWith('agent-') ? 'AGENT' : 'PROMPT';
          const typeColor = typeLabel === 'SKILL' ? 'var(--complete)' : typeLabel === 'AGENT' ? '#378add' : 'var(--accent)';

          return (
            <div key={out.filename} style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border)',
              padding: '14px 16px',
              display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap',
            }}>
              <div style={{ flex: 1, minWidth: '200px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '5px' }}>
                  <span style={{
                    fontFamily: 'var(--pixel-font)', fontSize: '7px',
                    padding: '3px 7px',
                    color: typeColor,
                    border: `1px solid ${typeColor}44`,
                    background: `${typeColor}11`,
                  }}>
                    {typeLabel}
                  </span>
                  <span style={{ fontFamily: 'var(--mono-font)', fontSize: '13px', color: 'var(--text)' }}>
                    {out.filename}
                  </span>
                </div>
                {out.description && (
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', margin: 0, lineHeight: 1.6 }}>
                    {out.description}
                  </p>
                )}
              </div>
              <div style={{ display: 'flex', gap: '6px', flexShrink: 0 }}>
                <a href={ghLink} target="_blank" rel="noopener noreferrer" style={{
                  display: 'flex', alignItems: 'center', gap: '6px',
                  fontFamily: 'var(--pixel-font)', fontSize: '11px', letterSpacing: '0.3px',
                  color: 'var(--text-muted)', background: 'var(--bg-card)',
                  border: '1px solid var(--border)', padding: '7px 13px',
                  textDecoration: 'none', transition: 'border-color 0.12s, color 0.12s',
                }}
                  onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--accent)'; (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; }}
                >
                  <GHIcon size={13} /> VIEW
                </a>
                <button onClick={() => copy(out.filename, out.body)} style={{
                  display: 'flex', alignItems: 'center', gap: '6px',
                  fontFamily: 'var(--pixel-font)', fontSize: '11px', letterSpacing: '0.3px',
                  color: isCopied ? 'var(--complete)' : 'var(--accent)',
                  background: isCopied ? 'var(--complete-dim)' : 'var(--accent-dim)',
                  border: `1px solid ${isCopied ? 'rgba(114,184,48,0.3)' : 'var(--accent-border)'}`,
                  padding: '7px 13px', cursor: 'pointer',
                  boxShadow: isCopied ? '0 0 6px var(--complete-glow)' : '0 0 6px var(--accent-glow)',
                  transition: 'all 0.15s',
                }}>
                  {isCopied ? '✓ COPIED' : '⬇ INSTALL'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </SectionCard>
  );
}

/* ── Code section ───────────────────────────────────────────── */
function CodeSection({ codeFiles, phaseSlug, lessonSlug }: { codeFiles: CodeFile[]; phaseSlug: string; lessonSlug: string }) {
  const [copied, setCopied] = useState<string | null>(null);

  const copy = useCallback((key: string, text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 2000);
    }).catch(() => {});
  }, []);

  return (
    <SectionCard icon="💻" title="RUN THE CODE" subtitle="Executable files from this lesson">
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {codeFiles.map(f => {
          const cmd = runCmd(phaseSlug, lessonSlug, f.filename, f.ext);
          const icon = LANG_ICON[f.ext] ?? '📄';
          const ghLink = `https://github.com/cookie-may/felixforlearnai/tree/main/public/phases/${phaseSlug}/${lessonSlug}/code/${f.filename}`;
          const isCopied = copied === f.filename;

          return (
            <div key={f.filename} style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border)',
              borderLeft: '3px solid var(--accent)',
              padding: '12px 16px',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px', flexWrap: 'wrap', marginBottom: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '16px' }}>{icon}</span>
                  <span style={{ fontFamily: 'var(--mono-font)', fontSize: '14px', color: 'var(--text)', fontWeight: 500 }}>
                    {f.filename}
                  </span>
                  <span style={{ fontFamily: 'var(--mono-font)', fontSize: '11px', color: 'var(--text-dim)' }}>
                    {formatSize(f.sizeBytes)}
                  </span>
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <a href={ghLink} target="_blank" rel="noopener noreferrer" style={{
                    display: 'flex', alignItems: 'center', gap: '6px',
                    fontFamily: 'var(--pixel-font)', fontSize: '11px', letterSpacing: '0.3px',
                    color: 'var(--text-muted)', background: 'var(--bg-card)',
                    border: '1px solid var(--border)', padding: '7px 13px',
                    textDecoration: 'none', transition: 'border-color 0.12s, color 0.12s',
                  }}
                    onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--accent)'; (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; }}
                    onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; }}
                  >
                    <GHIcon size={13} /> VIEW
                  </a>
                </div>
              </div>

              {/* run command */}
              <div style={{
                background: 'var(--code-bg)',
                border: '1px solid var(--border)',
                padding: '10px 14px',
                display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px',
                flexWrap: 'wrap',
              }}>
                <code style={{
                  fontFamily: 'var(--mono-font)', fontSize: '12px',
                  color: 'var(--accent)', textShadow: '0 0 6px rgba(232,108,44,0.3)',
                  flex: 1, minWidth: '180px',
                }}>
                  {cmd}
                </code>
                <button onClick={() => copy(f.filename, cmd)} style={{
                  fontFamily: 'var(--pixel-font)', fontSize: '11px', letterSpacing: '0.3px',
                  color: isCopied ? 'var(--complete)' : 'var(--text-muted)',
                  background: 'transparent',
                  border: `1px solid ${isCopied ? 'rgba(114,184,48,0.4)' : 'var(--border)'}`,
                  padding: '6px 12px', cursor: 'pointer',
                  transition: 'all 0.15s',
                  flexShrink: 0,
                }}>
                  {isCopied ? '✓ COPIED' : '⧉ COPY'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </SectionCard>
  );
}

/* ── Quiz section ───────────────────────────────────────────── */
function QuizSection({ questions }: { questions: QuizQuestion[] }) {
  const [answers, setAnswers] = useState<Record<number, number>>({});

  const answered = Object.keys(answers).length;

  return (
    <SectionCard icon="🧠" title="KNOWLEDGE CHECK" subtitle={`${questions.length} questions · test your understanding`}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {questions.map((q, qi) => {
          const selected = answers[qi];
          const isAnswered = selected !== undefined;
          const isCorrect = selected === q.correct;

          return (
            <div key={qi} style={{
              background: 'var(--bg-surface)',
              border: `1px solid ${isAnswered ? (isCorrect ? 'rgba(114,184,48,0.4)' : 'rgba(232,108,44,0.4)') : 'var(--border)'}`,
              padding: '16px',
              transition: 'border-color 0.2s',
            }}>
              {/* stage badge + question */}
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', marginBottom: '14px' }}>
                <span style={{
                  fontFamily: 'var(--pixel-font)', fontSize: '7px',
                  padding: '3px 7px', flexShrink: 0, marginTop: '2px',
                  color: q.stage === 'pre' ? 'var(--accent)' : 'var(--complete)',
                  border: `1px solid ${q.stage === 'pre' ? 'var(--accent-border)' : 'rgba(114,184,48,0.3)'}`,
                  background: q.stage === 'pre' ? 'var(--accent-dim)' : 'var(--complete-dim)',
                }}>
                  {q.stage === 'pre' ? 'PRE' : 'POST'}
                </span>
                <p style={{ fontFamily: 'var(--body-font)', fontSize: '15px', color: 'var(--text)', margin: 0, lineHeight: 1.6, fontWeight: 500 }}>
                  {q.question}
                </p>
              </div>

              {/* options */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: isAnswered ? '14px' : 0 }}>
                {q.options.map((opt, oi) => {
                  const isSelected = selected === oi;
                  const isRight    = oi === q.correct;
                  let bg = 'var(--bg-card)', border = 'var(--border)', color = 'var(--text-muted)';
                  if (isAnswered) {
                    if (isRight)                    { bg = 'var(--complete-dim)'; border = 'rgba(114,184,48,0.5)'; color = 'var(--complete)'; }
                    else if (isSelected && !isRight) { bg = 'rgba(232,108,44,0.08)'; border = 'var(--accent-border)'; color = 'var(--accent)'; }
                  }

                  return (
                    <button key={oi}
                      disabled={isAnswered}
                      onClick={() => setAnswers(prev => ({ ...prev, [qi]: oi }))}
                      style={{
                        display: 'flex', alignItems: 'center', gap: '10px',
                        background: bg, border: `1px solid ${border}`, color,
                        padding: '10px 14px', cursor: isAnswered ? 'default' : 'pointer',
                        textAlign: 'left', width: '100%',
                        transition: 'all 0.15s', fontFamily: 'var(--body-font)', fontSize: '14px',
                        lineHeight: 1.5,
                      }}
                      onMouseEnter={e => { if (!isAnswered) { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--text)'; }}}
                      onMouseLeave={e => { if (!isAnswered) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; }}}
                    >
                      <span style={{
                        fontFamily: 'var(--pixel-font)', fontSize: '8px',
                        width: '20px', height: '20px', flexShrink: 0,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        border: `1px solid ${border}`,
                        background: isAnswered && isRight ? 'var(--complete)' : isAnswered && isSelected ? 'var(--accent)' : 'transparent',
                        color: isAnswered && (isRight || isSelected) ? 'var(--bg)' : 'inherit',
                      }}>
                        {isAnswered && isRight ? '✓' : isAnswered && isSelected ? '✗' : String.fromCharCode(65 + oi)}
                      </span>
                      {opt}
                    </button>
                  );
                })}
              </div>

              {/* explanation */}
              {isAnswered && (
                <div style={{
                  padding: '12px 14px',
                  background: isCorrect ? 'var(--complete-dim)' : 'var(--accent-dim)',
                  border: `1px solid ${isCorrect ? 'rgba(114,184,48,0.3)' : 'var(--accent-border)'}`,
                  borderLeft: `3px solid ${isCorrect ? 'var(--complete)' : 'var(--accent)'}`,
                }}>
                  <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '7px', color: isCorrect ? 'var(--complete)' : 'var(--accent)', marginBottom: '6px', letterSpacing: '0.5px' }}>
                    {isCorrect ? '✓ CORRECT' : '✗ INCORRECT'}
                  </div>
                  <p style={{ fontSize: '13px', color: 'var(--text-muted)', margin: 0, lineHeight: 1.7 }}>
                    {q.explanation}
                  </p>
                </div>
              )}
            </div>
          );
        })}

        {answered === questions.length && (
          <div style={{
            padding: '16px 20px', textAlign: 'center',
            background: 'var(--accent-dim)', border: '1px solid var(--accent-border)',
            boxShadow: '0 0 16px var(--accent-glow)',
          }}>
            <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '11px', color: 'var(--accent)', textShadow: '0 0 10px var(--accent-glow)', marginBottom: '6px' }}>
              QUIZ COMPLETE
            </div>
            <p style={{ fontSize: '14px', color: 'var(--text-muted)', margin: 0 }}>
              {Object.entries(answers).filter(([qi, ans]) => questions[Number(qi)].correct === ans).length}/{questions.length} correct
            </p>
          </div>
        )}
      </div>
    </SectionCard>
  );
}

/* ── Learning path section ──────────────────────────────────── */
function LearningPathSection({ phaseSlug, lessonSlug }: { phaseSlug: string; lessonSlug: string }) {
  const router = useRouter();
  const { isComplete } = useProgress();
  const currentPath = `phases/${phaseSlug}/${lessonSlug}`;

  const phase = PHASES.find(p => p.lessons.some(l => l.path === currentPath));
  if (!phase) return null;

  const completed = phase.lessons.filter(l => l.path && isComplete(l.path)).length;

  return (
    <SectionCard icon="🗺" title="LEARNING PATH" subtitle={`Phase ${String(phase.id).padStart(2,'0')}: ${phase.name}`}>
      {/* scroll track */}
      <div style={{ overflowX: 'auto', paddingBottom: '8px' }}>
        <div style={{ display: 'flex', gap: '6px', minWidth: 'max-content' }}>
          {phase.lessons.map((lesson, i) => {
            const isCurrent = lesson.path === currentPath;
            const isDone    = lesson.path ? isComplete(lesson.path) : false;
            const parts     = lesson.path?.split('/');
            const canNav    = parts?.length === 3;

            return (
              <button key={i}
                onClick={() => { if (canNav && parts) router.push(`/lessons/${parts[1]}/${parts[2]}`); }}
                disabled={!canNav}
                style={{
                  display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
                  padding: '10px 12px', minWidth: '140px', maxWidth: '160px',
                  background: isCurrent ? 'var(--accent-dim)' : isDone ? 'var(--complete-dim)' : 'var(--bg-surface)',
                  border: `1px solid ${isCurrent ? 'var(--accent)' : isDone ? 'rgba(114,184,48,0.4)' : 'var(--border)'}`,
                  borderTop: isCurrent ? '2px solid var(--accent)' : isDone ? '2px solid var(--complete)' : '1px solid var(--border)',
                  cursor: canNav ? 'pointer' : 'default',
                  boxShadow: isCurrent ? '0 0 10px var(--accent-glow)' : isDone ? '0 0 6px var(--complete-glow)' : 'none',
                  transition: 'all 0.12s',
                  textAlign: 'left',
                }}
                onMouseEnter={e => { if (canNav && !isCurrent) e.currentTarget.style.borderColor = 'var(--accent)'; }}
                onMouseLeave={e => { if (canNav && !isCurrent) e.currentTarget.style.borderColor = isDone ? 'rgba(114,184,48,0.4)' : 'var(--border)'; }}
              >
                <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '7px', color: isCurrent ? 'var(--accent)' : isDone ? 'var(--complete)' : 'var(--text-dim)', marginBottom: '5px', letterSpacing: '0.3px' }}>
                  {isDone ? '✓' : isCurrent ? '▶' : String(i + 1).padStart(2,'0')}
                </div>
                <div style={{ fontSize: '12px', color: isCurrent ? 'var(--text)' : 'var(--text-muted)', lineHeight: 1.4, fontWeight: isCurrent ? 600 : 400 }}>
                  {lesson.name}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ marginTop: '12px', fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)', letterSpacing: '0.3px' }}>
        {completed}/{phase.lessons.length} LESSONS COMPLETE IN THIS PHASE
      </div>
    </SectionCard>
  );
}

/* ═══════════════════════════════════════════════════════════════ */
export default function LessonViewer({ phaseSlug, lessonSlug, initialContent, outputs, codeFiles, quiz }: Props) {
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
    display: 'flex', alignItems: 'center', gap: '7px',
    fontSize: '13px', fontFamily: 'var(--pixel-font)', letterSpacing: '0.3px',
    color: '#c8b49a', background: 'var(--bg-card)',
    border: '1px solid #4a3020', padding: '9px 16px',
    cursor: 'pointer', textDecoration: 'none',
    transition: 'border-color 0.15s, color 0.15s, box-shadow 0.15s',
  };

  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh', paddingTop: '68px' }}>

      {/* ── Sub-header ────────────────────────────── */}
      <div style={{
        position: 'sticky', top: '68px', zIndex: 40,
        background: 'var(--header-bg)', backdropFilter: 'blur(14px)',
        borderBottom: '1px solid var(--border)',
        padding: '0 1.5rem', height: '58px',
        display: 'flex', alignItems: 'center',
      }}>
        <div style={{ maxWidth: '860px', width: '100%', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
          <button onClick={() => router.back()} style={{ ...iconBtn, flexShrink: 0 }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 6px var(--accent-glow)'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.boxShadow = 'none'; }}
          >
            <ArrowLeft size={14} /> BACK
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
            <a href={ghUrl} target="_blank" rel="noopener noreferrer" style={iconBtn}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--accent)'; (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.borderColor = 'var(--border)'; (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; }}
            >
              <GHIcon size={14} /> SRC
            </a>
            <button
              onClick={() => done ? markIncomplete(lessonPath) : markComplete(lessonPath)}
              style={{ ...iconBtn, borderColor: done ? 'var(--complete)' : '#4a3020', color: done ? 'var(--complete)' : '#c8b49a', background: done ? 'var(--complete-dim)' : 'var(--bg-card)', boxShadow: done ? '0 0 8px var(--complete-glow)' : 'none' }}
              onMouseEnter={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 6px var(--accent-glow)'; }}}
              onMouseLeave={e => { if (!done) { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.boxShadow = 'none'; }}}
            >
              {done ? '✓ DONE' : '□ MARK DONE'}
            </button>
          </div>
        </div>
      </div>

      {/* ── Main content ──────────────────────────── */}
      <div style={{ maxWidth: '860px', margin: '0 auto', padding: '36px 1.5rem 80px' }}>

        {/* No content fallback */}
        {!initialContent && (
          <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderTop: '2px solid var(--accent)', padding: '40px 32px', textAlign: 'center' }}>
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
          </div>
        )}

        {initialContent && (
          <>
            {/* Meta bar */}
            {meta && (
              <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', marginBottom: '28px', paddingBottom: '16px', borderBottom: '1px solid var(--border)' }}>
                {[
                  { label: 'PHASE', val: `${String(meta.phase.id).padStart(2,'0')} · ${meta.phase.name}` },
                  { label: 'TYPE',  val: meta.lesson.type },
                  { label: 'LANG',  val: meta.lesson.lang },
                ].map(item => (
                  <div key={item.label}>
                    <div style={{ fontSize: '8px', fontFamily: 'var(--pixel-font)', color: 'var(--text-dim)', letterSpacing: '0.5px', marginBottom: '4px' }}>{item.label}</div>
                    <div style={{ fontSize: '13px', color: 'var(--text-muted)', fontFamily: 'var(--mono-font)' }}>{item.val}</div>
                  </div>
                ))}
                {done && (
                  <div style={{ marginLeft: 'auto' }}>
                    <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--complete)', letterSpacing: '0.5px', background: 'var(--complete-dim)', border: '1px solid rgba(114,184,48,0.3)', padding: '4px 10px', boxShadow: '0 0 8px var(--complete-glow)' }}>
                      ✓ COMPLETE
                    </span>
                  </div>
                )}
              </div>
            )}

            {/* Lesson prose */}
            <div className="lesson-prose">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>
                {initialContent}
              </ReactMarkdown>
            </div>

            {/* ── New sections ── */}
            {outputs.length > 0 && (
              <OutputsSection outputs={outputs} phaseSlug={phaseSlug} lessonSlug={lessonSlug} />
            )}

            {codeFiles.length > 0 && (
              <CodeSection codeFiles={codeFiles} phaseSlug={phaseSlug} lessonSlug={lessonSlug} />
            )}

            {quiz && quiz.questions?.length > 0 && (
              <QuizSection questions={quiz.questions} />
            )}

            <LearningPathSection phaseSlug={phaseSlug} lessonSlug={lessonSlug} />

            {/* Mark-complete CTA */}
            {!done && (
              <div style={{ marginTop: '40px', padding: '20px 24px', background: 'var(--accent-dim)', border: '1px solid var(--accent-border)', borderLeft: '3px solid var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '14px', color: 'var(--text-muted)' }}>
                  Finished reading? Mark this lesson complete to track your progress.
                </span>
                <button onClick={() => markComplete(lessonPath)} className="btn-primary" style={{ fontSize: '11px', padding: '8px 18px' }}>
                  ✓ MARK COMPLETE
                </button>
              </div>
            )}

            {/* Next module button */}
            {next && (
              <button
                onClick={() => router.push(`/lessons/${next.phaseSlug}/${next.lessonSlug}`)}
                style={{
                  marginTop: '16px', width: '100%',
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '18px 24px',
                  background: 'var(--bg-card)',
                  border: '1px solid var(--border)',
                  borderLeft: '3px solid var(--accent)',
                  cursor: 'pointer',
                  transition: 'border-color 0.15s, box-shadow 0.15s, background 0.15s',
                  textAlign: 'left',
                }}
                onMouseEnter={e => { e.currentTarget.style.background = 'var(--bg-card-hover)'; e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.boxShadow = '0 0 14px var(--accent-glow)'; }}
                onMouseLeave={e => { e.currentTarget.style.background = 'var(--bg-card)'; e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.boxShadow = 'none'; }}
              >
                <div>
                  <div style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)', marginBottom: '6px', letterSpacing: '0.3px' }}>
                    NEXT MODULE ▶
                  </div>
                  <div style={{ fontSize: '15px', color: 'var(--text)', fontWeight: 500 }}>
                    {next.lessonName}
                  </div>
                </div>
                <span style={{ fontSize: '20px', color: 'var(--accent)', textShadow: '0 0 8px var(--accent-glow)', flexShrink: 0 }}>→</span>
              </button>
            )}

            {!next && (
              <button
                onClick={() => { markComplete(lessonPath); router.push('/'); }}
                style={{ marginTop: '16px', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', padding: '20px 24px', background: 'var(--accent-dim)', border: '1px solid var(--accent-border)', cursor: 'pointer', boxShadow: '0 0 16px var(--accent-glow)' }}
              >
                <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '11px', color: 'var(--accent)', textShadow: '0 0 10px var(--accent-glow)', letterSpacing: '0.5px' }}>
                  🎉 COURSE COMPLETE — GO HOME
                </span>
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}

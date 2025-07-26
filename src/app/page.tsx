'use client';

import { useEffect, useState } from 'react';
import { PHASES, getTotalLessons, getCompletedLessons } from '@/data/phases';
import { GLOSSARY } from '@/data/glossary';
import { useProgress } from '@/components/ProgressProvider';
import PhaseModal from '@/components/PhaseModal';

const PATHWAY_ITEMS = [
  'Math', 'ML', 'Deep Learning', 'Transformers', 'LLMs', 'Agents', 'Production',
  'Math', 'ML', 'Deep Learning', 'Transformers', 'LLMs', 'Agents', 'Production',
  'Math', 'ML', 'Deep Learning', 'Transformers', 'LLMs', 'Agents', 'Production',
];

const ROTATIONS = [-1.5, 0.8, -0.7, 1.2, -1, 0.5, -0.3, 1.4, -1.2, 0.6, -0.8, 1.1, -0.4, 0.9, -1.3, 0.7, -0.6, 1.3, -0.9, 0.4];

function AnimatedNumber({ target, duration = 1200 }: { target: number; duration?: number }) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    let startTime: number;
    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.round(eased * target));
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [target, duration]);

  return <span>{value}</span>;
}

export default function HomePage() {
  const [selectedPhase, setSelectedPhase] = useState<number | null>(null);
  const [mounted, setMounted] = useState(false);
  const { completedLessons, getPhaseProgress } = useProgress();

  useEffect(() => {
    setMounted(true);
  }, []);

  const totalLessons = getTotalLessons();
  const totalPhases = PHASES.length;
  const staticCompleted = getCompletedLessons();
  const userCompleted = mounted ? completedLessons.size : 0;
  const totalCompleted = staticCompleted + (userCompleted > 0 ? userCompleted : 0);

  const handlePhaseClick = (index: number) => {
    setSelectedPhase(index);
  };

  const closeModal = () => {
    setSelectedPhase(null);
  };

  return (
    <>
      {/* Hero Section */}
      <section
        className="min-h-screen flex items-center justify-center relative overflow-hidden"
        style={{
          background: 'linear-gradient(135deg, #0d0d18 0%, #141430 40%, #0d0d18 100%)'
        }}
      >
        <div className="text-center px-6 py-20 max-w-3xl relative z-10">
          <div
            className="inline-block px-4 py-1 rounded-full text-sm font-mono mb-6 border"
            style={{
              color: 'var(--accent)',
              borderColor: 'rgba(255, 107, 107, 0.3)',
              background: 'rgba(255, 107, 107, 0.08)'
            }}
          >
            Open Source · MIT License · ~290 hours
          </div>

          <h1 className="font-heading text-5xl md:text-7xl font-bold mb-4">
            <span className="block" style={{ color: '#e8e5df' }}>AI Engineering</span>
            <span className="block" style={{ color: 'var(--accent)' }}>from Scratch</span>
          </h1>

          <p className="text-lg md:text-xl mb-8 max-w-xl mx-auto" style={{ color: '#9a9aaa' }}>
            260+ lessons across 20 phases. Build neural networks, transformers, and LLMs from first principles. Python, TypeScript, Rust, Julia.
          </p>

          {/* Stats */}
          <div className="flex justify-center gap-8 md:gap-12 mb-8">
            <div className="text-center">
              <span className="block text-4xl font-bold font-mono" style={{ color: 'var(--accent)' }}>
                <AnimatedNumber target={totalLessons} />
              </span>
              <span className="text-xs uppercase tracking-wider" style={{ color: '#9a9aaa' }}>Lessons</span>
            </div>
            <div className="text-center">
              <span className="block text-4xl font-bold font-mono" style={{ color: 'var(--accent)' }}>
                {totalPhases}
              </span>
              <span className="text-xs uppercase tracking-wider" style={{ color: '#9a9aaa' }}>Phases</span>
            </div>
            <div className="text-center">
              <span className="block text-4xl font-bold font-mono" style={{ color: 'var(--accent)' }}>
                4
              </span>
              <span className="text-xs uppercase tracking-wider" style={{ color: '#9a9aaa' }}>Languages</span>
            </div>
            <div className="text-center">
              <span className="block text-4xl font-bold font-mono" style={{ color: 'var(--accent)' }}>
                {mounted && totalCompleted}
              </span>
              <span className="text-xs uppercase tracking-wider" style={{ color: '#9a9aaa' }}>Complete</span>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex gap-4 justify-center flex-wrap mb-6">
            <a
              href="#phases"
              className="px-6 py-3 rounded-full font-bold border-2 transition-all hover:-translate-y-0.5 hover:shadow-hard"
              style={{
                background: 'var(--accent)',
                borderColor: 'var(--accent)',
                color: '#fff'
              }}
            >
              Explore Phases
            </a>
            <a
              href="https://github.com/rohitg00/ai-engineering-from-scratch"
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3 rounded-full font-bold border-2 transition-all hover:-translate-y-0.5"
              style={{
                background: 'transparent',
                borderColor: '#e8e5df',
                color: '#e8e5df'
              }}
            >
              ⭐ Star on GitHub
            </a>
          </div>

          <a
            href="https://github.com/rohitg00/ai-engineering-from-scratch/stargazers"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm"
            style={{ color: '#ffb800', textDecoration: 'none' }}
          >
            ⭐ 1,000+ stars this week
          </a>
        </div>
      </section>

      {/* Pathway Strip */}
      <div
        className="py-5 border-y-2 border-dashed overflow-hidden"
        style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
      >
        <div className="flex gap-4 scroll-pathway whitespace-nowrap">
          {PATHWAY_ITEMS.map((item, i) => (
            <span key={i} className="flex items-center gap-4">
              <span
                className="px-4 py-2 rounded-full font-heading font-bold border-2"
                style={{
                  background: 'var(--bg)',
                  borderColor: 'var(--border)',
                  color: 'var(--text)'
                }}
              >
                {item}
              </span>
              <span style={{ color: 'var(--accent)' }}>~&gt;</span>
            </span>
          ))}
        </div>
      </div>

      {/* Why This Course Section */}
      <section className="py-20 px-6 border-b-2 border-dashed" style={{ borderColor: 'var(--border)' }}>
        <div className="max-w-6xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl text-center mb-4">Why This Course</h2>
          <p className="text-center mb-12" style={{ color: 'var(--text-muted)' }}>
            What makes us different from the rest
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              className="p-6 rounded-2xl border-l-4 border-2 fade-in"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)',
                borderLeftColor: 'var(--accent)',
                boxShadow: '4px 4px 0 var(--shadow-color)'
              }}
            >
              <div className="text-3xl mb-3">⚙</div>
              <h3 className="font-heading text-xl mb-2" style={{ color: 'var(--accent)' }}>Build, Don't Import</h3>
              <p style={{ color: 'var(--text-muted)' }}>
                Implement every algorithm from raw math. No magic wrappers. You write the backprop, the tokenizer, the attention mechanism.
              </p>
            </div>

            <div
              className="p-6 rounded-2xl border-l-4 border-2 fade-in"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)',
                borderLeftColor: 'var(--accent)',
                boxShadow: '4px 4px 0 var(--shadow-color)'
              }}
            >
              <div className="text-3xl mb-3">☰</div>
              <h3 className="font-heading text-xl mb-2" style={{ color: 'var(--accent)' }}>20 Phases of Depth</h3>
              <p style={{ color: 'var(--text-muted)' }}>
                A structured path from calculus and linear algebra through LLMs, agents, multi-agent swarms, and production deployment.
              </p>
            </div>

            <div
              className="p-6 rounded-2xl border-l-4 border-2 fade-in"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)',
                borderLeftColor: 'var(--accent)',
                boxShadow: '4px 4px 0 var(--shadow-color)'
              }}
            >
              <div className="text-3xl mb-3">⌨</div>
              <h3 className="font-heading text-xl mb-2" style={{ color: 'var(--accent)' }}>Real Code, Real Projects</h3>
              <p style={{ color: 'var(--text-muted)' }}>
                Python, TypeScript, Rust, Julia. Every lesson has runnable code, not slides. Build a GPT, a RAG system, an agent team.
              </p>
            </div>

            <div
              className="p-6 rounded-2xl border-l-4 border-2 fade-in"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)',
                borderLeftColor: 'var(--accent)',
                boxShadow: '4px 4px 0 var(--shadow-color)'
              }}
            >
              <div className="text-3xl mb-3">✿</div>
              <h3 className="font-heading text-xl mb-2" style={{ color: 'var(--accent)' }}>Free & Open Source</h3>
              <p style={{ color: 'var(--text-muted)' }}>
                The entire curriculum is on GitHub. Clone it, fork it, learn at your own pace. No paywall, no signup, no gatekeeping.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Phases Section */}
      <section id="phases" className="py-20 px-6 border-b-2 border-dashed" style={{ borderColor: 'var(--border)' }}>
        <div className="max-w-6xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl text-center mb-4">The 20 Phases</h2>
          <p className="text-center mb-12" style={{ color: 'var(--text-muted)' }}>
            Click any phase to see its lessons
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            {PHASES.map((phase, index) => {
              const rot = ROTATIONS[index % ROTATIONS.length];
              const lessonPaths = phase.lessons
                .filter(l => l.url)
                .map(l => {
                  const match = l.url?.match(/(phases\/[^/]+\/[^/]+)\/?$/);
                  return match ? match[1] : '';
                })
                .filter(Boolean);
              const progress = getPhaseProgress(lessonPaths);
              const doneCount = phase.lessons.filter(l => l.status === 'complete').length + (progress.completed > 0 ? progress.completed : 0);
              const totalCount = phase.lessons.length;
              const pct = totalCount > 0 ? Math.round((doneCount / totalCount) * 100) : 0;

              return (
                <div
                  key={phase.id}
                  onClick={() => handlePhaseClick(index)}
                  className="phase-card p-5 rounded-2xl border-2 cursor-pointer transition-all hover:-translate-y-1"
                  style={{
                    background: 'var(--bg-surface)',
                    borderColor: 'var(--border)',
                    borderTopColor: phase.status === 'complete' ? 'var(--complete)' : phase.status === 'in-progress' ? 'var(--accent)' : 'var(--border)',
                    boxShadow: '4px 4px 0 var(--shadow-color)',
                    transform: `rotate(${rot}deg)`
                  }}
                >
                  <span
                    className="block text-xs font-mono font-bold mb-1"
                    style={{ color: 'var(--accent)' }}
                  >
                    {phase.status}
                  </span>
                  <span
                    className="block text-sm font-mono font-bold mb-2"
                    style={{ color: 'var(--text-muted)' }}
                  >
                    Phase {String(phase.id).padStart(2, '0')}
                  </span>
                  <h3 className="font-heading font-bold text-lg mb-2" style={{ color: 'var(--text)' }}>
                    {phase.name}
                  </h3>
                  <p className="text-sm mb-3 line-clamp-2" style={{ color: 'var(--text-muted)' }}>
                    {phase.desc}
                  </p>
                  <div className="h-1.5 rounded-full overflow-hidden mb-2" style={{ background: 'var(--border)' }}>
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${pct}%`, background: 'var(--complete)' }}
                    />
                  </div>
                  <span className="text-xs font-mono" style={{ color: 'var(--text-muted)' }}>
                    {doneCount}/{totalCount} lessons
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section id="roadmap" className="py-20 px-6 border-b-2 border-dashed" style={{ borderColor: 'var(--border)' }}>
        <div className="max-w-6xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl text-center mb-12">Learning Roadmap</h2>

          {/* Progress bar */}
          <div className="max-w-xl mx-auto mb-12">
            <div className="flex items-center gap-4">
              <div className="flex-1 h-3 rounded-full overflow-hidden" style={{ background: 'var(--border)' }}>
                <div
                  className="h-full rounded-full transition-all duration-1000"
                  style={{
                    width: `${totalCompleted > 0 ? Math.round((totalCompleted / totalLessons) * 100) : 0}%`,
                    background: 'linear-gradient(90deg, var(--complete), var(--secondary))'
                  }}
                />
              </div>
              <span className="font-mono font-bold" style={{ color: 'var(--complete)' }}>
                {totalCompleted > 0 ? Math.round((totalCompleted / totalLessons) * 100) : 0}%
              </span>
            </div>
          </div>

          {/* Phase pills */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
            {PHASES.map((phase) => (
              <div
                key={phase.id}
                className="px-4 py-3 rounded-xl border-2 flex items-center gap-3 transition-all hover:-translate-y-0.5"
                style={{
                  background: 'var(--bg-surface)',
                  borderColor: 'var(--border)'
                }}
              >
                <div
                  className="w-3 h-3 rounded-full shrink-0"
                  style={{
                    background: phase.status === 'complete' ? 'var(--complete)' : 'var(--planned)'
                  }}
                />
                <span className="text-sm font-mono truncate" style={{ color: 'var(--text)' }}>
                  {String(phase.id).padStart(2, '0')} {phase.name}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 border-b-2 border-dashed" style={{ borderColor: 'var(--border)' }}>
        <div className="max-w-6xl mx-auto">
          <h2 className="font-heading text-3xl md:text-4xl text-center mb-12">How It Works</h2>

          <div className="max-w-2xl mx-auto space-y-8">
            {[
              { num: 1, title: 'Clone the Repo', desc: 'One command. Everything you need is in the repository.' },
              { num: 2, title: 'Pick Your Phase', desc: 'Start at Phase 0 or jump to where your knowledge begins.' },
              { num: 3, title: 'Read the Theory', desc: 'Each lesson explains the concept from first principles.' },
              { num: 4, title: 'Build It Yourself', desc: 'Implement the algorithm. Run the code. Break things.' },
              { num: 5, title: 'Check Your Understanding', desc: 'Each phase has exercises. No multiple choice -- real code challenges.' },
              { num: 6, title: 'Ship the Capstone', desc: 'Phase 19 ties it all together. Build a production AI system.' },
            ].map((step, i) => (
              <div key={i} className="flex gap-5">
                <div
                  className="w-12 h-12 min-w-12 rounded-full border-2 flex items-center justify-center font-mono font-bold text-xl"
                  style={{
                    borderColor: 'var(--accent)',
                    color: 'var(--accent)',
                    background: 'var(--bg-surface)'
                  }}
                >
                  {step.num}
                </div>
                <div>
                  <h3 className="font-heading text-xl mb-1" style={{ color: 'var(--text)' }}>{step.title}</h3>
                  <p style={{ color: 'var(--text-muted)' }}>{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Glossary Callout */}
      <section className="py-20 px-6 border-b-2 border-dashed" style={{ borderColor: 'var(--border)' }}>
        <div className="max-w-6xl mx-auto">
          <div
            className="p-8 rounded-2xl border-2 flex flex-col md:flex-row items-center gap-8"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              boxShadow: '6px 6px 0 var(--shadow-color)'
            }}
          >
            <div className="flex-1">
              <h3 className="font-heading text-2xl mb-2" style={{ color: 'var(--accent)' }}>AI Glossary</h3>
              <p className="mb-4" style={{ color: 'var(--text-muted)' }}>
                Confused by jargon? We built a glossary that tells you what people <em>say</em> vs what things actually <em>mean</em>.
              </p>
              <div className="flex flex-wrap gap-2">
                {GLOSSARY.slice(0, 8).map((entry) => (
                  <span
                    key={entry.term}
                    className="px-3 py-1 rounded-full text-sm font-mono"
                    style={{
                      background: 'var(--bg)',
                      border: '1px solid var(--border)',
                      color: 'var(--text-muted)'
                    }}
                  >
                    {entry.term}
                  </span>
                ))}
              </div>
            </div>
            <a
              href="/glossary"
              className="px-6 py-3 rounded-full font-bold border-2 transition-all hover:-translate-y-0.5"
              style={{
                background: 'transparent',
                borderColor: 'var(--accent)',
                color: 'var(--accent)'
              }}
            >
              Browse All Terms
            </a>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6" style={{ background: 'var(--bg-surface)' }}>
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="font-heading text-3xl mb-4">Start Building</h2>
          <p className="mb-6" style={{ color: 'var(--text-muted)' }}>
            One command to begin your AI engineering journey.
          </p>
          <div
            className="inline-flex items-center gap-4 px-5 py-3 rounded-2xl border-2"
            style={{ background: 'var(--code-bg)', borderColor: 'var(--border)' }}
          >
            <code className="font-mono text-sm" style={{ color: 'var(--secondary)' }}>
              git clone https://github.com/rohitg00/ai-engineering-from-scratch.git
            </code>
            <button
              onClick={() => navigator.clipboard.writeText('git clone https://github.com/rohitg00/ai-engineering-from-scratch.git')}
              className="p-2 hover:scale-110 transition-transform"
              style={{ color: 'var(--text-muted)' }}
            >
              📋
            </button>
          </div>
        </div>
      </section>

      {/* Phase Modal */}
      {selectedPhase !== null && (
        <PhaseModal
          phase={PHASES[selectedPhase]}
          phaseIndex={selectedPhase}
          onClose={closeModal}
        />
      )}
    </>
  );
}

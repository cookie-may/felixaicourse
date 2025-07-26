'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Phase, Lesson } from '@/data/phases';
import { useProgress } from './ProgressProvider';
import { X, Check, Circle, ExternalLink } from 'lucide-react';

interface PhaseModalProps {
  phase: Phase;
  phaseIndex: number;
  onClose: () => void;
}

export default function PhaseModal({ phase, onClose }: PhaseModalProps) {
  const router = useRouter();
  const { isComplete, markComplete, markIncomplete } = useProgress();
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEsc);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEsc);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) onClose();
  };

  const handleLessonClick = (lesson: Lesson) => {
    if (lesson.path) {
      const [phaseSlug, lessonSlug] = lesson.path.split('/');
      router.push(`/lessons/${phaseSlug}/${lessonSlug}`);
      onClose();
    } else if (lesson.url) {
      window.open(lesson.url, '_blank');
    }
  };

  const getLessonPath = (lesson: Lesson): string | null => {
    if (lesson.path) return lesson.path;
    if (lesson.url) {
      const match = lesson.url.match(/phases\/([^/]+)\/([^/]+)/);
      if (match) return `${match[1]}/${match[2]}`;
    }
    return null;
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center"
      style={{
        background: 'var(--overlay-bg)',
        backdropFilter: 'blur(6px)',
        opacity: 1
      }}
      onClick={handleOverlayClick}
    >
      <div
        ref={modalRef}
        className="w-full max-w-2xl max-h-[80vh] overflow-y-auto rounded-t-3xl p-8 border-2"
        style={{
          background: 'var(--modal-bg)',
          borderColor: 'var(--border)',
          transform: 'translateY(0)',
          transition: 'transform 0.4s cubic-bezier(0.22, 1, 0.36, 1)'
        }}
      >
        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <span className="text-sm font-mono font-bold" style={{ color: 'var(--accent)' }}>
              Phase {String(phase.id).padStart(2, '0')}
            </span>
            <h2 className="font-heading text-2xl mt-1">{phase.name}</h2>
            <p className="mt-2" style={{ color: 'var(--text-muted)' }}>{phase.desc}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:opacity-70 transition-opacity"
            style={{ color: 'var(--text-muted)' }}
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Lessons */}
        <div className="space-y-1">
          {phase.lessons.map((lesson, i) => {
            const lessonPath = getLessonPath(lesson);
            const userDone = lessonPath ? isComplete(lessonPath) : false;
            const isDone = lesson.status === 'complete' || userDone;
            const hasContent = lesson.url || lesson.path;

            return (
              <div
                key={i}
                className="flex items-center gap-4 p-3 rounded-lg border border-transparent hover:border-[var(--border)] transition-colors"
              >
                {/* Status dot */}
                <div
                  className="w-2 h-2 rounded-full"
                  style={{
                    background: isDone ? 'var(--complete)' : lesson.status === 'planned' ? 'var(--planned)' : 'var(--border)'
                  }}
                />

                {/* Lesson name */}
                <button
                  onClick={() => handleLessonClick(lesson)}
                  className="flex-1 text-left font-medium hover:opacity-80"
                  style={{ color: 'var(--text)', textDecoration: 'none', background: 'none', border: 'none', cursor: 'pointer' }}
                  disabled={!hasContent}
                >
                  <span style={{ opacity: hasContent ? 1 : 0.5 }}>
                    {lesson.name}
                  </span>
                </button>

                {/* Type badge */}
                <span
                  className="px-2 py-1 rounded text-xs font-mono font-semibold"
                  style={{
                    border: '1px solid var(--border)',
                    color: lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)',
                    borderColor: lesson.type === 'Build'
                      ? 'rgba(90, 184, 143, 0.35)'
                      : 'rgba(255, 107, 107, 0.35)'
                  }}
                >
                  {lesson.type}
                </span>

                {/* Language */}
                <span className="text-xs font-mono hidden sm:block" style={{ color: 'var(--text-muted)' }}>
                  {lesson.lang}
                </span>

                {/* Read button */}
                {hasContent && (
                  <button
                    onClick={() => handleLessonClick(lesson)}
                    className="px-3 py-1.5 rounded text-sm border transition-colors hover:border-[var(--accent)]"
                    style={{
                      borderColor: 'var(--border)',
                      color: 'var(--text-muted)',
                      background: 'none'
                    }}
                  >
                    {userDone ? 'Review' : 'Read'}
                  </button>
                )}

                {/* Toggle completion */}
                {lessonPath && (
                  <button
                    onClick={() => userDone ? markIncomplete(lessonPath) : markComplete(lessonPath)}
                    className="w-6 h-6 rounded border flex items-center justify-center transition-all hover:border-[var(--accent)]"
                    style={{
                      borderColor: 'var(--border)',
                      color: 'var(--text-muted)',
                      background: userDone ? 'var(--complete)' : 'transparent'
                    }}
                    title={userDone ? 'Mark incomplete' : 'Mark complete'}
                  >
                    {userDone ? <Check className="w-4 h-4 text-white" /> : <Circle className="w-4 h-4" />}
                  </button>
                )}
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="mt-6 pt-4 border-t flex justify-between items-center text-sm" style={{ borderColor: 'var(--border)' }}>
          <span style={{ color: 'var(--text-muted)' }}>
            Progress saved in browser.
          </span>
          <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
            Click lesson to view content
          </span>
        </div>
      </div>
    </div>
  );
}

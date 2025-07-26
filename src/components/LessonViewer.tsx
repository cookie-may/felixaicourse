'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, ExternalLink, Check, Circle } from 'lucide-react';
import { useProgress } from '@/components/ProgressProvider';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface LessonViewerProps {
  phaseSlug: string;
  lessonSlug: string;
}

export default function LessonViewer({ phaseSlug, lessonSlug }: LessonViewerProps) {
  const router = useRouter();
  const { isComplete, markComplete, markIncomplete } = useProgress();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lessonTitle, setLessonTitle] = useState('');

  useEffect(() => {
    const fetchLessonContent = async () => {
      setLoading(true);
      setError(null);

      const lessonPath = `phases/${phaseSlug}/${lessonSlug}`;
      const rawUrl = `https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/${lessonPath}/docs/en.md`;

      try {
        const response = await fetch(rawUrl);
        if (!response.ok) {
          throw new Error('Lesson content not found');
        }
        const text = await response.text();
        setContent(text);

        const titleMatch = text.match(/^#\s+(.+)$/m);
        if (titleMatch) {
          setLessonTitle(titleMatch[1]);
        } else {
          setLessonTitle(lessonSlug.replace(/-/g, ' '));
        }
      } catch (err) {
        setError('Could not load lesson content. Please try again later.');
        console.error('Error fetching lesson:', err);
      } finally {
        setLoading(false);
      }
    };

    if (phaseSlug && lessonSlug) {
      fetchLessonContent();
    }
  }, [phaseSlug, lessonSlug]);

  const lessonPath = `phases/${phaseSlug}/${lessonSlug}`;
  const userDone = isComplete(lessonPath);
  const githubUrl = `https://github.com/rohitg00/ai-engineering-from-scratch/tree/main/${lessonPath}`;

  const toggleComplete = () => {
    if (userDone) {
      markIncomplete(lessonPath);
    } else {
      markComplete(lessonPath);
    }
  };

  return (
    <div className="min-h-screen" style={{ background: 'var(--bg)' }}>
      {/* Header */}
      <div
        className="sticky top-16 z-40 border-b px-4 py-3"
        style={{ background: 'var(--header-bg)', borderColor: 'var(--border)' }}
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <button
            onClick={() => router.back()}
            className="flex items-center gap-2 px-3 py-2 rounded-lg transition-colors hover:bg-[var(--bg-surface)]"
            style={{ color: 'var(--text-muted)' }}
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Back</span>
          </button>

          <div className="flex items-center gap-3">
            <a
              href={githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-2 rounded-lg border transition-colors hover:border-[var(--accent)]"
              style={{
                borderColor: 'var(--border)',
                color: 'var(--text-muted)'
              }}
            >
              <ExternalLink className="w-4 h-4" />
              <span className="hidden sm:inline">GitHub</span>
            </a>

            <button
              onClick={toggleComplete}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border transition-colors"
              style={{
                borderColor: userDone ? 'var(--complete)' : 'var(--border)',
                color: userDone ? 'var(--complete)' : 'var(--text-muted)',
                background: userDone ? 'rgba(90, 184, 143, 0.1)' : 'transparent'
              }}
            >
              {userDone ? <Check className="w-4 h-4" /> : <Circle className="w-4 h-4" />}
              <span className="hidden sm:inline">{userDone ? 'Completed' : 'Mark Complete'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div
              className="w-8 h-8 border-4 rounded-full animate-spin"
              style={{
                borderColor: 'var(--border)',
                borderTopColor: 'var(--accent)'
              }}
            />
          </div>
        ) : error ? (
          <div
            className="p-8 rounded-2xl border-2 text-center"
            style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
          >
            <div className="text-4xl mb-4">📚</div>
            <h2 className="font-heading text-2xl mb-2" style={{ color: 'var(--text)' }}>
              Lesson Not Available
            </h2>
            <p style={{ color: 'var(--text-muted)' }}>{error}</p>
            <a
              href={githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 px-4 py-2 rounded-lg border-2"
              style={{ borderColor: 'var(--accent)', color: 'var(--accent)' }}
            >
              View on GitHub
            </a>
          </div>
        ) : (
          <article
            className="prose prose-invert max-w-none lesson-content"
            style={{ color: 'var(--text)' }}
          >
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="font-heading text-4xl font-bold mb-6" style={{ color: 'var(--accent)' }}>
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="font-heading text-2xl font-bold mt-8 mb-4" style={{ color: 'var(--text)' }}>
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="font-heading text-xl font-semibold mt-6 mb-3" style={{ color: 'var(--text)' }}>
                    {children}
                  </h3>
                ),
                p: ({ children }) => (
                  <p className="mb-4 leading-relaxed" style={{ color: 'var(--text-muted)' }}>
                    {children}
                  </p>
                ),
                a: ({ href, children }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline underline-offset-2 hover:text-[var(--accent)]"
                    style={{ color: 'var(--secondary)' }}
                  >
                    {children}
                  </a>
                ),
                code: ({ children, className }) => {
                  const isInline = !className;
                  if (isInline) {
                    return (
                      <code
                        className="px-1.5 py-0.5 rounded text-sm font-mono"
                        style={{
                          background: 'var(--code-bg)',
                          color: 'var(--accent)',
                          border: '1px solid var(--border)'
                        }}
                      >
                        {children}
                      </code>
                    );
                  }
                  return (
                    <code className={`${className} block p-4 rounded-lg font-mono text-sm overflow-x-auto my-4`} style={{ background: 'var(--code-bg)', border: '1px solid var(--border)' }}>
                      {children}
                    </code>
                  );
                },
                pre: ({ children }) => (
                  <pre className="p-4 rounded-lg overflow-x-auto my-4 font-mono text-sm" style={{ background: 'var(--code-bg)', border: '1px solid var(--border)' }}>
                    {children}
                  </pre>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc list-inside mb-4 space-y-2" style={{ color: 'var(--text-muted)' }}>
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal list-inside mb-4 space-y-2" style={{ color: 'var(--text-muted)' }}>
                    {children}
                  </ol>
                ),
                li: ({ children }) => (
                  <li className="leading-relaxed">{children}</li>
                ),
                blockquote: ({ children }) => (
                  <blockquote
                    className="border-l-4 pl-4 my-4 italic"
                    style={{ borderColor: 'var(--accent)', color: 'var(--text-muted)' }}
                  >
                    {children}
                  </blockquote>
                ),
                table: ({ children }) => (
                  <div className="overflow-x-auto my-4">
                    <table className="w-full border-collapse rounded-lg overflow-hidden" style={{ border: '1px solid var(--border)' }}>
                      {children}
                    </table>
                  </div>
                ),
                th: ({ children }) => (
                  <th className="px-4 py-2 text-left font-semibold" style={{ background: 'var(--bg-surface)', borderBottom: '1px solid var(--border)' }}>
                    {children}
                  </th>
                ),
                td: ({ children }) => (
                  <td className="px-4 py-2" style={{ borderBottom: '1px solid var(--border)' }}>
                    {children}
                  </td>
                ),
                hr: () => (
                  <hr className="my-8 border-dashed" style={{ borderColor: 'var(--border)' }} />
                ),
              }}
            >
              {content}
            </ReactMarkdown>
          </article>
        )}
      </div>
    </div>
  );
}

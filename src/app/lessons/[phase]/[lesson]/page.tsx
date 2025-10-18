import fs from 'fs';
import path from 'path';
import { PHASES } from '@/data/phases';
import LessonViewer from '@/components/LessonViewer';

export interface OutputFile {
  filename: string;
  name: string;
  description: string;
  body: string;
}

export interface CodeFile {
  filename: string;
  sizeBytes: number;
  ext: string;
}

export interface QuizQuestion {
  stage: string;
  question: string;
  options: string[];
  correct: number;
  explanation: string;
}

function parseFrontmatter(raw: string): { meta: Record<string, string>; body: string } {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) return { meta: {}, body: raw };
  const meta: Record<string, string> = {};
  for (const line of match[1].split('\n')) {
    const colon = line.indexOf(':');
    if (colon > 0) meta[line.slice(0, colon).trim()] = line.slice(colon + 1).trim();
  }
  return { meta, body: match[2].trim() };
}

export async function generateStaticParams() {
  const paths: { phase: string; lesson: string }[] = [];
  PHASES.forEach(phase => {
    phase.lessons.forEach(lesson => {
      if (lesson.path) {
        const parts = lesson.path.split('/');
        if (parts.length === 3 && parts[1] && parts[2]) {
          paths.push({ phase: parts[1], lesson: parts[2] });
        }
      }
    });
  });
  return paths;
}

export default function LessonPage({ params }: { params: { phase: string; lesson: string } }) {
  const base = path.join(process.cwd(), 'public', 'phases', params.phase, params.lesson);

  /* ── Lesson markdown ── */
  let initialContent = '';
  try { initialContent = fs.readFileSync(path.join(base, 'docs', 'en.md'), 'utf-8'); } catch {}

  /* ── Output files ── */
  let outputs: OutputFile[] = [];
  try {
    const dir = path.join(base, 'outputs');
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));
    outputs = files.map(f => {
      const raw = fs.readFileSync(path.join(dir, f), 'utf-8');
      const { meta, body } = parseFrontmatter(raw);
      return {
        filename: f,
        name: meta.name ?? f.replace('.md', ''),
        description: meta.description ?? '',
        body,
      };
    });
  } catch {}

  /* ── Code files ── */
  let codeFiles: CodeFile[] = [];
  try {
    const dir = path.join(base, 'code');
    const files = fs.readdirSync(dir).filter(f => !f.startsWith('.'));
    codeFiles = files.map(f => {
      const stat = fs.statSync(path.join(dir, f));
      return { filename: f, sizeBytes: stat.size, ext: path.extname(f).slice(1) };
    });
  } catch {}

  /* ── Quiz ── */
  let quiz: { questions: QuizQuestion[] } | null = null;
  try {
    const raw = fs.readFileSync(path.join(base, 'quiz.json'), 'utf-8');
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      quiz = { questions: parsed };
    } else if (parsed && Array.isArray(parsed.questions)) {
      quiz = { questions: parsed.questions };
    }
  } catch {}

  return (
    <LessonViewer
      phaseSlug={params.phase}
      lessonSlug={params.lesson}
      initialContent={initialContent}
      outputs={outputs}
      codeFiles={codeFiles}
      quiz={quiz}
    />
  );
}

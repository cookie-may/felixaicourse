import fs from 'fs';
import path from 'path';
import { PHASES } from '@/data/phases';
import LessonViewer from '@/components/LessonViewer';

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
  const mdPath = path.join(process.cwd(), 'public', 'phases', params.phase, params.lesson, 'docs', 'en.md');
  let content = '';
  try {
    content = fs.readFileSync(mdPath, 'utf-8');
  } catch {
    content = '';
  }
  return <LessonViewer phaseSlug={params.phase} lessonSlug={params.lesson} initialContent={content} />;
}

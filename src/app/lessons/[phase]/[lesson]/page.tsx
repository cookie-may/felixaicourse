import { PHASES } from '@/data/phases';
import LessonViewer from '@/components/LessonViewer';

/* Required for output:'export' — enumerate all lesson routes at build time */
export async function generateStaticParams() {
  const paths: { phase: string; lesson: string }[] = [];
  PHASES.forEach(phase => {
    phase.lessons.forEach(lesson => {
      if (lesson.path) {
        const parts = lesson.path.split('/');
        // "phases/00-setup-and-tooling/01-dev-environment" → parts[1], parts[2]
        if (parts.length === 3 && parts[1] && parts[2]) {
          paths.push({ phase: parts[1], lesson: parts[2] });
        }
      }
    });
  });
  return paths;
}

export default function LessonPage({ params }: { params: { phase: string; lesson: string } }) {
  return <LessonViewer phaseSlug={params.phase} lessonSlug={params.lesson} />;
}

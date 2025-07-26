import { PHASES } from '@/data/phases';
import LessonViewer from '@/components/LessonViewer';

// Generate static paths for all lessons
export async function generateStaticParams() {
  const paths: { phase: string; lesson: string }[] = [];
  PHASES.forEach((phase) => {
    phase.lessons.forEach((lesson) => {
      if (lesson.path) {
        const [phaseSlug, lessonSlug] = lesson.path.split('/');
        if (phaseSlug && lessonSlug) {
          paths.push({ phase: phaseSlug, lesson: lessonSlug });
        }
      }
    });
  });
  return paths;
}

export default function LessonPage({ params }: { params: { phase: string; lesson: string } }) {
  return <LessonViewer phaseSlug={params.phase} lessonSlug={params.lesson} />;
}

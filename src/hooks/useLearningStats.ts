'use client';

import { useMemo } from 'react';
import { useProgress } from '@/components/ProgressProvider';
import { PHASES } from '@/data/phases';

export interface PhaseStats {
  id: number;
  name: string;
  total: number;
  completed: number;
  pct: number;
}

export interface LearningStats {
  totalLessons: number;
  completedLessons: number;
  overallPct: number;
  phaseStats: PhaseStats[];
  topPhase: PhaseStats | null;
}

export function useLearningStats(): LearningStats {
  const { isComplete } = useProgress();

  return useMemo(() => {
    const phaseStats: PhaseStats[] = PHASES.map(phase => {
      const withPath = phase.lessons.filter(l => l.path);
      const completed = withPath.filter(l => isComplete(l.path!)).length;
      return {
        id: phase.id,
        name: phase.name,
        total: withPath.length,
        completed,
        pct: withPath.length > 0 ? Math.round(completed / withPath.length * 100) : 0,
      };
    });

    const totalLessons = phaseStats.reduce((s, p) => s + p.total, 0);
    const completedLessons = phaseStats.reduce((s, p) => s + p.completed, 0);
    const overallPct = totalLessons > 0 ? Math.round(completedLessons / totalLessons * 100) : 0;
    const topPhase = [...phaseStats].sort((a, b) => b.pct - a.pct).find(p => p.completed > 0) ?? null;

    return { totalLessons, completedLessons, overallPct, phaseStats, topPhase };
  }, [isComplete]);
}

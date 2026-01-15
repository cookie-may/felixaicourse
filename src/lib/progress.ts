/**
 * Felix Learning Platform - Progress Tracker
 * Tracks and manages learning progress across phases
 */

export interface ProgressRecord {
  phaseId: number;
  lessonId: string;
  status: 'not_started' | 'in_progress' | 'completed';
  startedAt?: Date;
  completedAt?: Date;
  notes?: string;
}

export interface PhaseProgress {
  phaseId: number;
  totalLessons: number;
  completedLessons: number;
  inProgressLessons: number;
  percentage: number;
  estimatedTimeRemaining: number;
}

export class FelixProgressTracker {
  private records: Map<string, ProgressRecord> = new Map();
  private phaseMetadata: Map<number, { totalLessons: number; avgTimePerLesson: number }> = new Map();

  constructor() {
    this.initializePhaseMetadata();
  }

  private initializePhaseMetadata(): void {
    // Initialize phase metadata with estimated times
    const phaseData = [
      { id: 0, lessons: 12, avgTime: 2 },
      { id: 1, lessons: 22, avgTime: 4 },
      { id: 2, lessons: 18, avgTime: 3 },
      { id: 3, lessons: 13, avgTime: 5 },
      { id: 4, lessons: 28, avgTime: 4 },
      { id: 5, lessons: 18, avgTime: 3 },
      { id: 6, lessons: 12, avgTime: 3 },
      { id: 7, lessons: 14, avgTime: 4 },
      { id: 8, lessons: 14, avgTime: 5 },
      { id: 9, lessons: 12, avgTime: 4 },
      { id: 10, lessons: 14, avgTime: 6 },
      { id: 11, lessons: 13, avgTime: 3 },
      { id: 12, lessons: 11, avgTime: 4 },
      { id: 13, lessons: 10, avgTime: 3 },
      { id: 14, lessons: 15, avgTime: 5 },
      { id: 15, lessons: 11, avgTime: 4 },
      { id: 16, lessons: 14, avgTime: 5 },
      { id: 17, lessons: 11, avgTime: 4 },
      { id: 18, lessons: 6, avgTime: 2 },
      { id: 19, lessons: 5, avgTime: 8 },
    ];

    phaseData.forEach(p => {
      this.phaseMetadata.set(p.id, {
        totalLessons: p.lessons,
        avgTimePerLesson: p.avgTime,
      });
    });
  }

  recordProgress(phaseId: number, lessonId: string, status: ProgressRecord['status']): void {
    const key = `${phaseId}-${lessonId}`;
    const existing = this.records.get(key);

    const record: ProgressRecord = {
      phaseId,
      lessonId,
      status,
      startedAt: existing?.startedAt || (status !== 'not_started' ? new Date() : undefined),
      completedAt: status === 'completed' ? new Date() : undefined,
    };

    this.records.set(key, record);
  }

  getPhaseProgress(phaseId: number): PhaseProgress {
    const metadata = this.phaseMetadata.get(phaseId) || { totalLessons: 10, avgTimePerLesson: 3 };
    let completed = 0;
    let inProgress = 0;

    this.records.forEach((record) => {
      if (record.phaseId === phaseId) {
        if (record.status === 'completed') completed++;
        if (record.status === 'in_progress') inProgress++;
      }
    });

    const remaining = metadata.totalLessons - completed - inProgress;
    const estimatedTime = remaining * metadata.avgTimePerLesson;

    return {
      phaseId,
      totalLessons: metadata.totalLessons,
      completedLessons: completed,
      inProgressLessons: inProgress,
      percentage: Math.round(((completed + inProgress) / metadata.totalLessons) * 100),
      estimatedTimeRemaining: estimatedTime,
    };
  }

  getOverallProgress(): { totalPhases: number; completedPhases: number; percentage: number } {
    let totalCompleted = 0;
    let totalLessons = 0;

    this.phaseMetadata.forEach((metadata, phaseId) => {
      const progress = this.getPhaseProgress(phaseId);
      totalCompleted += progress.completedLessons;
      totalLessons += metadata.totalLessons;
    });

    return {
      totalPhases: 20,
      completedPhases: Math.floor(totalCompleted / 15),
      percentage: Math.round((totalCompleted / totalLessons) * 100),
    };
  }

  getNextLesson(phaseId: number): string | null {
    const progress = this.getPhaseProgress(phaseId);
    const completed = progress.completedLessons;

    // Return next lesson based on phase structure
    const lessonMap: { [key: number]: string[] } = {
      1: ['Linear Algebra Intuition', 'Vectors, Matrices & Operations', 'Matrix Transformations'],
    };

    return lessonMap[phaseId]?.[completed] || null;
  }

  exportProgress(): string {
    const data = {
      exportedAt: new Date().toISOString(),
      records: Array.from(this.records.entries()),
      overall: this.getOverallProgress(),
    };
    return JSON.stringify(data, null, 2);
  }
}

// Singleton instance for app-wide use
export const felixTracker = new FelixProgressTracker();
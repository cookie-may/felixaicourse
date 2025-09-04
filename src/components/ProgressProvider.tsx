'use client';

import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from 'react';

interface ProgressContextType {
  completedLessons: Set<string>;
  markComplete: (path: string) => void;
  markIncomplete: (path: string) => void;
  isComplete: (path: string) => boolean;
  resetProgress: () => void;
  getPhaseProgress: (lessonPaths: string[]) => { completed: number; total: number; percentage: number };
}

const ProgressContext = createContext<ProgressContextType | undefined>(undefined);

const STORAGE_KEY = 'felix-progress';

export function ProgressProvider({ children }: { children: ReactNode }) {
  const [completedLessons, setCompletedLessons] = useState<Set<string>>(new Set());
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setCompletedLessons(new Set(parsed));
      } catch (e) {
        console.error('Failed to parse progress:', e);
      }
    }
  }, []);

  useEffect(() => {
    if (mounted) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(completedLessons)));
    }
  }, [completedLessons, mounted]);

  const markComplete = useCallback((path: string) => {
    setCompletedLessons(prev => {
      const next = new Set(prev);
      next.add(path);
      return next;
    });
  }, []);

  const markIncomplete = useCallback((path: string) => {
    setCompletedLessons(prev => {
      const next = new Set(prev);
      next.delete(path);
      return next;
    });
  }, []);

  const isComplete = useCallback((path: string) => {
    return completedLessons.has(path);
  }, [completedLessons]);

  const resetProgress = useCallback(() => {
    setCompletedLessons(new Set());
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const getPhaseProgress = useCallback((lessonPaths: string[]) => {
    const completed = lessonPaths.filter(path => completedLessons.has(path)).length;
    const total = lessonPaths.length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { completed, total, percentage };
  }, [completedLessons]);

  return (
    <ProgressContext.Provider value={{
      completedLessons,
      markComplete,
      markIncomplete,
      isComplete,
      resetProgress,
      getPhaseProgress
    }}>
      {children}
    </ProgressContext.Provider>
  );
}

export function useProgress() {
  const context = useContext(ProgressContext);
  if (!context) {
    throw new Error('useProgress must be used within ProgressProvider');
  }
  return context;
}

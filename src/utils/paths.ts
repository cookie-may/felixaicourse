/**
 * Felix Learning Platform - Path Utilities
 * Provides utilities for navigating the curriculum structure
 */

export interface PhasePath {
  phaseId: number;
  phaseSlug: string;
  lessonSlug: string;
  fullPath: string;
}

export class FelixPathResolver {
  /**
   * Parse a path like "phases/01-math-foundations/02-vectors-matrices" into structured data
   */
  static parseLessonPath(path: string): PhasePath | null {
    const parts = path.split('/').filter(Boolean);
    if (parts.length < 2) return null;

    const phasePart = parts[0];
    const lessonPart = parts.slice(1).join('/');

    // Extract phase number from slug
    const phaseMatch = phasePart.match(/^(\d+)-/);
    const phaseId = phaseMatch ? parseInt(phaseMatch[1], 10) : 0;

    // Clean up slugs
    const phaseSlug = phasePart.replace(/^\d+-/, '');
    const lessonSlug = lessonPart.replace(/^\d+-/, '');

    return {
      phaseId,
      phaseSlug,
      lessonSlug,
      fullPath: path,
    };
  }

  /**
   * Build a lesson path from components
   */
  static buildLessonPath(phaseId: number, lessonSlug: string): string {
    const phasePrefix = String(phaseId).padStart(2, '0');
    const phaseSlugs = [
      'setup-and-tooling',
      'math-foundations',
      'ml-fundamentals',
      'deep-learning-core',
      'computer-vision',
      'nlp-foundations-to-advanced',
      'speech-and-audio',
      'transformers-deep-dive',
      'generative-ai',
      'reinforcement-learning',
      'llms-from-scratch',
      'llm-engineering',
      'multimodal-ai',
      'tools-and-protocols',
      'agent-engineering',
      'autonomous-systems',
      'multi-agent-and-swarms',
      'infrastructure-and-production',
      'ethics-safety-and-alignment',
      'capstone-projects',
    ];

    const phaseSlug = phaseSlugs[phaseId] || 'unknown';
    const lessonNum = lessonSlug.split('-')[0];
    const lessonName = lessonSlug.replace(/^\d+-/, '');

    return `phases/${phasePrefix}-${phaseSlug}/${lessonNum}-${lessonName}`;
  }

  /**
   * Get the parent phase path for a lesson
   */
  static getPhasePath(lessonPath: string): string {
    const parsed = this.parseLessonPath(lessonPath);
    if (!parsed) return '';

    const phasePrefix = String(parsed.phaseId).padStart(2, '0');
    return `phases/${phasePrefix}-${parsed.phaseSlug}`;
  }

  /**
   * Check if a path is within the phases directory
   */
  static isPhasePath(path: string): boolean {
    return path.startsWith('phases/') || path.includes('/phases/');
  }

  /**
   * Get adjacent lessons for navigation
   */
  static getAdjacentLessons(
    currentPhase: number,
    currentLessonIndex: number,
    totalLessonsInPhase: number
  ): { prev: string | null; next: string | null } {
    return {
      prev: currentLessonIndex > 0 ? String(currentLessonIndex - 1) : null,
      next: currentLessonIndex < totalLessonsInPhase - 1 ? String(currentLessonIndex + 1) : null,
    };
  }
}

export class FelixUrlBuilder {
  private baseUrl: string;

  constructor(baseUrl: string = '') {
    this.baseUrl = baseUrl;
  }

  lesson(phaseId: number, lessonSlug: string): string {
    const path = FelixPathResolver.buildLessonPath(phaseId, lessonSlug);
    return `${this.baseUrl}/lessons/${path}`;
  }

  phase(phaseId: number): string {
    const phasePrefix = String(phaseId).padStart(2, '0');
    return `${this.baseUrl}/catalog?phase=${phasePrefix}`;
  }

  catalog(): string {
    return `${this.baseUrl}/catalog`;
  }

  glossary(): string {
    return `${this.baseUrl}/glossary`;
  }

  ai(): string {
    return `${this.baseUrl}/ai`;
  }
}
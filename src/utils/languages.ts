/**
 * Felix Learning Platform - Language Utilities
 * Provides utilities for handling multiple programming languages
 */

export type ProgrammingLanguage = 'python' | 'typescript' | 'rust' | 'julia';

export interface LanguageConfig {
  name: string;
  extension: string;
  color: string;
  icon: string;
  keywords: string[];
}

export const LANGUAGE_CONFIGS: Record<ProgrammingLanguage, LanguageConfig> = {
  python: {
    name: 'Python',
    extension: '.py',
    color: '#3776AB',
    icon: '🐍',
    keywords: ['def', 'class', 'import', 'numpy', 'torch', 'pandas'],
  },
  typescript: {
    name: 'TypeScript',
    extension: '.ts',
    color: '#3178C6',
    icon: '🟦',
    keywords: ['interface', 'type', 'import', 'export', 'async', 'await'],
  },
  rust: {
    name: 'Rust',
    extension: '.rs',
    color: '#DEA584',
    icon: '🦀',
    keywords: ['fn', 'let', 'mut', 'impl', 'trait', 'pub', 'mod'],
  },
  julia: {
    name: 'Julia',
    extension: '.jl',
    color: '#9558B2',
    icon: '🟣',
    keywords: ['function', 'struct', 'using', 'import', 'begin', 'end'],
  },
};

export function detectLanguage(filename: string): ProgrammingLanguage | null {
  const ext = filename.split('.').pop()?.toLowerCase();
  const mapping: Record<string, ProgrammingLanguage> = {
    'py': 'python',
    'ts': 'typescript',
    'tsx': 'typescript',
    'rs': 'rust',
    'jl': 'julia',
  };
  return ext ? mapping[ext] || null : null;
}

export function getLanguageColor(lang: ProgrammingLanguage): string {
  return LANGUAGE_CONFIGS[lang].color;
}

export function getCodeSnippetTemplate(lang: ProgrammingLanguage): string {
  const templates: Record<ProgrammingLanguage, string> = {
    python: `def main():
    """Main entry point for the learning exercise."""
    pass

if __name__ == "__main__":
    main()`,
    typescript: `export function main(): void {
  // Main entry point for the learning exercise
}

main();`,
    rust: `fn main() {
    // Main entry point for the learning exercise
}

fn main() {}`,
    julia: `function main()
    # Main entry point for the learning exercise
end

main()`,
  };
  return templates[lang];
}

export class LanguageDetector {
  private static instance: LanguageDetector;
  private cache: Map<string, ProgrammingLanguage> = new Map();

  static getInstance(): LanguageDetector {
    if (!LanguageDetector.instance) {
      LanguageDetector.instance = new LanguageDetector();
    }
    return LanguageDetector.instance;
  }

  detect(filename: string): ProgrammingLanguage | null {
    if (this.cache.has(filename)) {
      return this.cache.get(filename) || null;
    }

    const detected = detectLanguage(filename);
    if (detected) {
      this.cache.set(filename, detected);
    }
    return detected;
  }

  detectMultiple(filenames: string[]): Map<string, ProgrammingLanguage> {
    const results = new Map<string, ProgrammingLanguage>();
    filenames.forEach(f => {
      const lang = this.detect(f);
      if (lang) results.set(f, lang);
    });
    return results;
  }

  clearCache(): void {
    this.cache.clear();
  }
}
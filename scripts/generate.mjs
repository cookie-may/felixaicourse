#!/usr/bin/env node
/**
 * Felix Learning Platform - Metadata Generator
 * Generates structured metadata for lessons
 */

function generateLessonMetadata(phaseId, lessonName, languages = []) {
  const timestamp = new Date().toISOString();
  const slug = lessonName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

  return {
    id: `${phaseId}-${slug}`,
    phase: phaseId,
    title: lessonName,
    slug: slug,
    languages: languages,
    created: timestamp,
    version: '1.0.0',
    status: 'generated',
    metadata: {
      type: 'lesson',
      format: 'interactive',
      difficulty: estimateDifficulty(phaseId),
    },
  };
}

function estimateDifficulty(phaseId) {
  if (phaseId <= 3) return 'foundational';
  if (phaseId <= 7) return 'intermediate';
  if (phaseId <= 14) return 'advanced';
  return 'expert';
}

function generatePhaseSummary() {
  const phases = [];

  const phaseNames = [
    'Setup & Tooling',
    'Math Foundations',
    'ML Fundamentals',
    'Deep Learning Core',
    'Computer Vision',
    'NLP: Foundations to Advanced',
    'Speech & Audio',
    'Transformers Deep Dive',
    'Generative AI',
    'Reinforcement Learning',
    'LLMs from Scratch',
    'LLM Engineering',
    'Multimodal AI',
    'Tools & Protocols',
    'Agent Engineering',
    'Autonomous Systems',
    'Multi-Agent & Swarms',
    'Infrastructure & Production',
    'Ethics, Safety & Alignment',
    'Capstone Projects',
  ];

  for (let i = 0; i < 20; i++) {
    phases.push({
      id: i,
      name: phaseNames[i],
      difficulty: estimateDifficulty(i),
      estimatedHours: Math.floor(Math.random() * 20) + 10,
    });
  }

  return phases;
}

function main() {
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║           Felix Metadata Generator v1.0                    ║');
  console.log('╚══════════════════════════════════════════════════════════════╝\n');

  // Generate sample lesson
  const sample = generateLessonMetadata(1, 'Linear Algebra Intuition', ['Python', 'Julia']);
  console.log('📝 Sample Generated Metadata:');
  console.log(JSON.stringify(sample, null, 2));

  console.log('\n📊 Phase Summary:');
  const summary = generatePhaseSummary();
  summary.forEach(p => {
    console.log(`   Phase ${String(p.id).padStart(2, '0')}: ${p.name.padEnd(30)} [${p.difficulty}] ~${p.estimatedHours}h`);
  });
}

main();
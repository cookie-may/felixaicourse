#!/usr/bin/env node
/**
 * Felix Learning Platform - Curriculum Validator
 * Validates all phases and lessons for completeness
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';

const BASE_PATH = './public/phases';

function getAllFiles(dir, files = []) {
  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      getAllFiles(fullPath, files);
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function countFilesByExtension(dir) {
  const files = getAllFiles(dir);
  const counts = {};
  for (const file of files) {
    const ext = extname(file).toLowerCase();
    counts[ext] = (counts[ext] || 0) + 1;
  }
  return counts;
}

function validateLessonStructure(lessonPath) {
  const codeDir = join(lessonPath, 'code');
  const readmePath = join(lessonPath, 'README.md');

  const results = {
    hasCode: false,
    hasReadme: false,
    codeFiles: [],
    readmeSize: 0,
  };

  try {
    const codeDirExists = statSync(codeDir);
    results.hasCode = codeDirExists.isDirectory();

    if (results.hasCode) {
      const codeFiles = readdirSync(codeDir);
      results.codeFiles = codeFiles.filter(f => !f.startsWith('.'));
    }
  } catch (e) {
    results.hasCode = false;
  }

  try {
    const readmeStat = statSync(readmePath);
    results.hasReadme = true;
    results.readmeSize = readmeStat.size;
  } catch (e) {
    results.hasReadme = false;
  }

  return results;
}

function analyzePhase(phaseDir) {
  const phaseName = phaseDir.replace(BASE_PATH + '/', '');
  const lessons = [];

  try {
    const lessonDirs = readdirSync(phaseDir);
    for (const lesson of lessonDirs) {
      const lessonPath = join(phaseDir, lesson);
      const stat = statSync(lessonPath);

      if (stat.isDirectory()) {
        const validation = validateLessonStructure(lessonPath);
        lessons.push({
          name: lesson,
          ...validation,
        });
      }
    }
  } catch (e) {
    console.error(`Error analyzing phase ${phaseName}: ${e.message}`);
  }

  return {
    phase: phaseName,
    lessonCount: lessons.length,
    lessons: lessons.filter(l => l.hasCode || l.hasReadme),
  };
}

function generateReport() {
  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║       Felix Learning Platform - Curriculum Analysis         ║');
  console.log('╚══════════════════════════════════════════════════════════════╝\n');

  // File statistics
  const fileCounts = countFilesByExtension(BASE_PATH);
  console.log('📊 File Distribution:');
  const extOrder = ['.py', '.ts', '.tsx', '.md', '.json', '.svg', '.yaml'];
  for (const ext of extOrder) {
    if (fileCounts[ext]) {
      console.log(`   ${ext.padEnd(6)} → ${String(fileCounts[ext]).padStart(4)} files`);
    }
  }

  const totalFiles = Object.values(fileCounts).reduce((a, b) => a + b, 0);
  console.log(`   ─────────────────────────────────────────`);
  console.log(`   Total: ${totalFiles} files\n`);

  // Phase analysis
  console.log('📚 Phase Structure:');
  try {
    const phases = readdirSync(BASE_PATH).sort();
    for (const phase of phases) {
      const analysis = analyzePhase(join(BASE_DIR || BASE_PATH, phase));
      const completed = analysis.lessons.filter(l => l.hasCode && l.hasReadme).length;
      const total = analysis.lessons.length;
      const bar = '█'.repeat(completed) + '░'.repeat(Math.max(0, total - completed));
      console.log(`   ${phase.padEnd(40)} [${bar}] ${completed}/${total}`);
    }
  } catch (e) {
    console.log('   Unable to read phase directory');
  }

  console.log('\n✅ Validation complete.');
}

generateReport();
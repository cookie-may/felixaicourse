'use client';

import { useState, useMemo } from 'react';
import { PHASES } from '@/data/phases';
import { useProgress } from '@/components/ProgressProvider';
import { Search } from 'lucide-react';

export default function CatalogPage() {
  const [search, setSearch] = useState('');
  const [phaseFilter, setPhaseFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  const { isComplete } = useProgress();

  const allLessons = useMemo(() => {
    const lessons: Array<{
      name: string;
      type: string;
      lang: string;
      status: string;
      url?: string;
      phaseName: string;
      phaseId: number;
    }> = [];

    PHASES.forEach(phase => {
      phase.lessons.forEach(lesson => {
        lessons.push({
          ...lesson,
          phaseName: phase.name,
          phaseId: phase.id,
        });
      });
    });

    return lessons;
  }, []);

  const filteredLessons = useMemo(() => {
    return allLessons.filter(lesson => {
      const matchesSearch = search === '' ||
        lesson.name.toLowerCase().includes(search.toLowerCase()) ||
        lesson.lang.toLowerCase().includes(search.toLowerCase()) ||
        lesson.phaseName.toLowerCase().includes(search.toLowerCase());

      const matchesPhase = phaseFilter === 'all' || lesson.phaseId === parseInt(phaseFilter);

      const matchesStatus = statusFilter === 'all' ||
        lesson.status === statusFilter ||
        (statusFilter === 'user-complete' && lesson.phaseId !== undefined);

      return matchesSearch && matchesPhase && matchesStatus;
    });
  }, [allLessons, search, phaseFilter, statusFilter]);

  return (
    <div className="min-h-screen py-12 px-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="font-heading text-4xl md:text-5xl mb-4">Lesson Catalog</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Every lesson across all 20 phases. Search, filter, sort.
          </p>
        </div>

        {/* Filters */}
        <div className="mb-8 flex flex-col md:flex-row gap-4 items-center">
          {/* Search */}
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5" style={{ color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search lessons..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl border-2 outline-none"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)',
                color: 'var(--text)'
              }}
            />
          </div>

          {/* Phase Filter */}
          <select
            value={phaseFilter}
            onChange={(e) => setPhaseFilter(e.target.value)}
            className="px-4 py-3 rounded-xl border-2 outline-none cursor-pointer"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              color: 'var(--text)'
            }}
          >
            <option value="all">All Phases</option>
            {PHASES.map(phase => (
              <option key={phase.id} value={phase.id}>
                Phase {String(phase.id).padStart(2, '0')}: {phase.name}
              </option>
            ))}
          </select>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-3 rounded-xl border-2 outline-none cursor-pointer"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              color: 'var(--text)'
            }}
          >
            <option value="all">All Status</option>
            <option value="complete">Complete</option>
            <option value="in-progress">In Progress</option>
            <option value="planned">Planned</option>
          </select>
        </div>

        {/* Results count */}
        <p className="mb-4 text-sm" style={{ color: 'var(--text-muted)' }}>
          Showing {filteredLessons.length} of {allLessons.length} lessons
        </p>

        {/* Table */}
        <div className="overflow-x-auto rounded-xl border-2" style={{ borderColor: 'var(--border)' }}>
          <table className="w-full">
            <thead
              className="border-b-2"
              style={{ background: 'var(--bg-surface)', borderColor: 'var(--border)' }}
            >
              <tr>
                <th className="text-left p-4 font-mono text-sm font-semibold" style={{ color: 'var(--text-muted)' }}>
                  Phase
                </th>
                <th className="text-left p-4 font-mono text-sm font-semibold" style={{ color: 'var(--text-muted)' }}>
                  Lesson
                </th>
                <th className="text-left p-4 font-mono text-sm font-semibold hidden sm:table-cell" style={{ color: 'var(--text-muted)' }}>
                  Type
                </th>
                <th className="text-left p-4 font-mono text-sm font-semibold hidden md:table-cell" style={{ color: 'var(--text-muted)' }}>
                  Language
                </th>
                <th className="text-left p-4 font-mono text-sm font-semibold" style={{ color: 'var(--text-muted)' }}>
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredLessons.map((lesson, i) => (
                <tr
                  key={i}
                  className="border-b last:border-b-0 hover:bg-[var(--bg-surface)] transition-colors"
                  style={{ borderColor: 'var(--border)' }}
                >
                  <td className="p-4">
                    <span className="text-sm font-mono" style={{ color: 'var(--accent)' }}>
                      {String(lesson.phaseId).padStart(2, '0')}
                    </span>
                  </td>
                  <td className="p-4">
                    {lesson.url ? (
                      <a
                        href={lesson.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium hover:opacity-80"
                        style={{ color: 'var(--text)', textDecoration: 'none' }}
                      >
                        {lesson.name}
                      </a>
                    ) : (
                      <span style={{ color: 'var(--text-muted)' }}>{lesson.name}</span>
                    )}
                  </td>
                  <td className="p-4 hidden sm:table-cell">
                    <span
                      className="px-2 py-1 rounded text-xs font-mono"
                      style={{
                        color: lesson.type === 'Build' ? 'var(--complete)' : 'var(--accent)',
                        border: '1px solid var(--border)'
                      }}
                    >
                      {lesson.type}
                    </span>
                  </td>
                  <td className="p-4 hidden md:table-cell">
                    <span className="text-sm font-mono" style={{ color: 'var(--text-muted)' }}>
                      {lesson.lang}
                    </span>
                  </td>
                  <td className="p-4">
                    <span
                      className="px-2 py-1 rounded-full text-xs font-mono capitalize"
                      style={{
                        background: lesson.status === 'complete'
                          ? 'rgba(90, 184, 143, 0.15)'
                          : lesson.status === 'in-progress'
                          ? 'rgba(255, 107, 107, 0.15)'
                          : 'rgba(128, 112, 96, 0.15)',
                        color: lesson.status === 'complete'
                          ? 'var(--complete)'
                          : lesson.status === 'in-progress'
                          ? 'var(--accent)'
                          : 'var(--planned)'
                      }}
                    >
                      {lesson.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredLessons.length === 0 && (
          <div className="text-center py-12">
            <p style={{ color: 'var(--text-muted)' }}>No lessons found matching your criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
}

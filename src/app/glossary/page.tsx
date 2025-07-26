'use client';

import { useState, useMemo } from 'react';
import { GLOSSARY, GlossaryEntry, searchGlossary } from '@/data/glossary';
import { Search } from 'lucide-react';

export default function GlossaryPage() {
  const [search, setSearch] = useState('');

  const filteredTerms = useMemo(() => {
    if (!search.trim()) return GLOSSARY;
    return searchGlossary(search);
  }, [search]);

  return (
    <div className="min-h-screen py-12 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="font-heading text-4xl md:text-5xl mb-4">AI Glossary</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            What people <em>say</em> vs what things actually <em>mean</em>
          </p>
        </div>

        {/* Search */}
        <div className="mb-8 relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5" style={{ color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search glossary terms..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-12 pr-4 py-4 rounded-xl border-2 text-lg outline-none"
            style={{
              background: 'var(--bg-surface)',
              borderColor: 'var(--border)',
              color: 'var(--text)'
            }}
          />
        </div>

        {/* Results count */}
        <p className="mb-6 text-sm" style={{ color: 'var(--text-muted)' }}>
          {filteredTerms.length} {filteredTerms.length === 1 ? 'term' : 'terms'} found
        </p>

        {/* Glossary Terms */}
        <div className="space-y-4">
          {filteredTerms.map((entry, i) => (
            <div
              key={i}
              className="p-6 rounded-2xl border-2"
              style={{
                background: 'var(--bg-surface)',
                borderColor: 'var(--border)'
              }}
            >
              <h2 className="font-heading text-2xl mb-3" style={{ color: 'var(--text)' }}>
                {entry.term}
              </h2>

              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <span
                    className="text-sm font-mono font-semibold px-2 py-1 rounded shrink-0"
                    style={{
                      background: 'rgba(255, 107, 107, 0.1)',
                      color: 'var(--accent)'
                    }}
                  >
                    Says:
                  </span>
                  <p style={{ color: 'var(--text-muted)' }}>{entry.says}</p>
                </div>

                <div className="flex items-start gap-3">
                  <span
                    className="text-sm font-mono font-semibold px-2 py-1 rounded shrink-0"
                    style={{
                      background: 'rgba(90, 184, 143, 0.1)',
                      color: 'var(--complete)'
                    }}
                  >
                    Means:
                  </span>
                  <p style={{ color: 'var(--text)' }}>{entry.means}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredTerms.length === 0 && (
          <div className="text-center py-12">
            <p style={{ color: 'var(--text-muted)' }}>No glossary terms found matching "{search}"</p>
          </div>
        )}

        {/* Bottom info */}
        <div className="mt-12 text-center text-sm" style={{ color: 'var(--text-muted)' }}>
          <p>
            The SLAFAI glossary provides clear, practical explanations of AI terminology.
            <br />
            No jargon, no fluff — just what things actually mean.
          </p>
        </div>
      </div>
    </div>
  );
}

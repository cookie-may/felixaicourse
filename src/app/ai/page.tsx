'use client';

import AIChat from '@/components/AIChat';

export default function AIPage() {
  return (
    <div className="min-h-screen py-12 px-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="font-heading text-4xl md:text-5xl mb-4">AI Tutor</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Chat with an AI tutor to help you learn AI engineering concepts.
          </p>
        </div>

        {/* Chat Component */}
        <AIChat />

        {/* Info */}
        <div
          className="mt-8 p-6 rounded-2xl border-2"
          style={{
            background: 'var(--bg-surface)',
            borderColor: 'var(--border)'
          }}
        >
          <h2 className="font-heading text-xl mb-4">About AI Tutor</h2>
          <div className="space-y-4 text-sm" style={{ color: 'var(--text-muted)' }}>
            <p>
              The AI Tutor uses OpenRouter to connect to Claude 3 Haiku, providing
              instant answers to your AI engineering questions.
            </p>
            <p>
              You need your own OpenRouter API key to use this feature. Keys are
              free to get at{' '}
              <a
                href="https://openrouter.ai/keys"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: 'var(--secondary)' }}
              >
                openrouter.ai/keys
              </a>
              .
            </p>
            <p>
              <strong>Privacy:</strong> Your API key is stored only in your browser&apos;s
              local storage and is never sent to our servers. All chat messages go
              directly to OpenRouter.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

import Link from 'next/link';

export default function Footer() {
  return (
    <footer
      className="border-t-2 border-dashed py-8"
      style={{ borderColor: 'var(--border)' }}
    >
      <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
        <p style={{ color: 'var(--text-muted)' }}>
          SLAFAI — Open Source · MIT License · ~290 hours
        </p>
        <div className="flex gap-6">
          <Link href="https://github.com/rohitg00/ai-engineering-from-scratch" style={{ color: 'var(--text-muted)' }}>
            GitHub
          </Link>
          <Link href="/catalog" style={{ color: 'var(--text-muted)' }}>
            Catalog
          </Link>
          <Link href="/glossary" style={{ color: 'var(--text-muted)' }}>
            Glossary
          </Link>
        </div>
      </div>
    </footer>
  );
}

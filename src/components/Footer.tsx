'use client';

import Link from 'next/link';
import Image from 'next/image';

function XIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-4.714-6.231-5.401 6.231H2.744l7.73-8.835L1.254 2.25H8.08l4.253 5.622zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
  );
}

function GHIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0 1 12 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.202 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
    </svg>
  );
}

export default function Footer() {
  return (
    <footer style={{
      borderTop: '1px solid var(--border)',
      padding: '0 1.5rem',
      height: '68px',
      background: 'var(--bg)',
      display: 'flex', alignItems: 'center',
    }}>
      <div style={{
        maxWidth: '1280px', width: '100%', margin: '0 auto',
        display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px',
      }}>
        {/* Logo — mirrors Header */}
        <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
          <Image src="/logo.png" alt="felix" width={38} height={38}
            style={{ borderRadius: '4px', filter: 'drop-shadow(0 0 6px rgba(232,108,44,0.5))' }}
          />
          <span style={{
            fontFamily: 'var(--pixel-font)',
            fontSize: '16px',
            color: 'var(--accent)',
            letterSpacing: '0.5px',
            textShadow: '0 0 10px var(--accent-glow), 0 0 28px rgba(232,108,44,0.3)',
            lineHeight: 1,
          }}>
            FELIX<br />
            <span style={{ color: 'var(--text-muted)', textShadow: 'none', fontSize: '12px' }}>forlearnai</span>
          </span>
        </Link>

        <div style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          {[
            { href: '/catalog',  label: 'CATALOG'  },
            { href: '/glossary', label: 'GLOSSARY' },
          ].map(l => (
            <Link key={l.href} href={l.href} style={{
              fontFamily: 'var(--pixel-font)', fontSize: '14px',
              color: 'var(--text-muted)', textDecoration: 'none', letterSpacing: '0.3px',
              transition: 'color 0.15s',
            }}
              onMouseEnter={(e: React.MouseEvent<HTMLAnchorElement>) => (e.currentTarget.style.color = 'var(--accent)')}
              onMouseLeave={(e: React.MouseEvent<HTMLAnchorElement>) => (e.currentTarget.style.color = 'var(--text-muted)')}
            >
              {l.label}
            </Link>
          ))}

          <div style={{ width: '1px', height: '14px', background: 'var(--border)' }} />

          <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '11px', color: 'var(--text-dim)', letterSpacing: '0.3px' }}>
            MIT LICENSE
          </span>

          <a href="https://x.com/felixforlearnai" target="_blank" rel="noopener noreferrer"
            title="Follow on X"
            style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', transition: 'color 0.15s, filter 0.15s' }}
            onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; (e.currentTarget as HTMLElement).style.filter = 'drop-shadow(0 0 4px var(--accent-glow))'; }}
            onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; (e.currentTarget as HTMLElement).style.filter = 'none'; }}
          >
            <XIcon />
          </a>
          <a href="https://github.com/cookie-may/felixforlearnai" target="_blank" rel="noopener noreferrer"
            title="GitHub"
            style={{ color: 'var(--text-muted)', display: 'flex', alignItems: 'center', transition: 'color 0.15s, filter 0.15s' }}
            onMouseEnter={e => { (e.currentTarget as HTMLElement).style.color = 'var(--accent)'; (e.currentTarget as HTMLElement).style.filter = 'drop-shadow(0 0 4px var(--accent-glow))'; }}
            onMouseLeave={e => { (e.currentTarget as HTMLElement).style.color = 'var(--text-muted)'; (e.currentTarget as HTMLElement).style.filter = 'none'; }}
          >
            <GHIcon />
          </a>
        </div>
      </div>
    </footer>
  );
}

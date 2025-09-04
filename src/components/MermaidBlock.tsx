'use client';

import { useEffect, useRef, useState } from 'react';

let mermaidReady = false;
let mermaidLib: typeof import('mermaid').default | null = null;

async function getMermaid() {
  if (!mermaidLib) {
    const mod = await import('mermaid');
    mermaidLib = mod.default;
  }
  if (!mermaidReady) {
    mermaidLib.initialize({
      startOnLoad: false,
      theme: 'dark' as const,
      darkMode: true,
      themeVariables: {
        primaryColor:        '#E86C2C',
        primaryTextColor:    '#f2e8d8',
        primaryBorderColor:  '#2e1e0e',
        lineColor:           '#8c7460',
        secondaryColor:      '#1c1510',
        tertiaryColor:       '#131009',
        background:          '#0b0806',
        mainBkg:             '#1c1510',
        nodeBorder:          '#E86C2C',
        clusterBkg:          '#131009',
        titleColor:          '#f2e8d8',
        edgeLabelBackground: '#1c1510',
        fontFamily:          'JetBrains Mono, monospace',
        fontSize:            '13px',
      },
    });
    mermaidReady = true;
  }
  return mermaidLib;
}

let idCounter = 0;

export default function MermaidBlock({ code }: { code: string }) {
  const [svg, setSvg]   = useState<string>('');
  const [err, setErr]   = useState(false);
  const [busy, setBusy] = useState(true);
  const idRef = useRef(`mermaid-${++idCounter}`);

  useEffect(() => {
    let cancelled = false;
    setBusy(true);
    setErr(false);

    getMermaid()
      .then(m => m.render(idRef.current, code.trim()))
      .then(({ svg: out }) => {
        if (!cancelled) { setSvg(out); setBusy(false); }
      })
      .catch(() => {
        if (!cancelled) { setErr(true); setBusy(false); }
      });

    return () => { cancelled = true; };
  }, [code]);

  if (busy) {
    return (
      <div className="mermaid-wrap skeleton" style={{ height: '120px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '9px', color: 'var(--accent)', opacity: 0.6 }}>
          RENDERING DIAGRAM...
        </span>
      </div>
    );
  }

  if (err) {
    return (
      <pre style={{
        background: 'var(--code-bg)', border: '1px solid var(--border)',
        borderLeft: '3px solid var(--accent)', padding: '1rem 1.25rem',
        fontFamily: 'var(--mono-font)', fontSize: '0.84em', color: '#d4c4a8',
        overflow: 'auto', margin: '1.25rem 0',
      }}>
        {code}
      </pre>
    );
  }

  return (
    <div
      className="mermaid-wrap"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
}

export default function LessonLoading() {
  return (
    <div style={{ background: 'var(--bg)', minHeight: '100vh', paddingTop: '68px' }}>

      {/* Sub-header skeleton */}
      <div style={{
        position: 'sticky', top: '68px', zIndex: 40,
        background: 'var(--header-bg)',
        borderBottom: '1px solid var(--border)',
        padding: '0 1.5rem', height: '58px',
        display: 'flex', alignItems: 'center',
      }}>
        <div style={{ maxWidth: '860px', width: '100%', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '12px' }}>
          <div className="skeleton" style={{ width: '80px', height: '36px' }} />
          <div className="skeleton" style={{ width: '240px', height: '14px', borderRadius: '2px' }} />
          <div style={{ display: 'flex', gap: '8px' }}>
            <div className="skeleton" style={{ width: '64px', height: '36px' }} />
            <div className="skeleton" style={{ width: '120px', height: '36px' }} />
          </div>
        </div>
      </div>

      {/* Content skeleton */}
      <div style={{ maxWidth: '860px', margin: '0 auto', padding: '36px 1.5rem 80px' }}>

        {/* Meta bar */}
        <div style={{ display: 'flex', gap: '32px', marginBottom: '28px', paddingBottom: '16px', borderBottom: '1px solid var(--border)' }}>
          {[120, 80, 90].map((w, i) => (
            <div key={i}>
              <div className="skeleton" style={{ width: '48px', height: '10px', marginBottom: '6px', borderRadius: '2px' }} />
              <div className="skeleton" style={{ width: `${w}px`, height: '14px', borderRadius: '2px' }} />
            </div>
          ))}
        </div>

        {/* Title */}
        <div className="skeleton" style={{ width: '70%', height: '28px', marginBottom: '16px', borderRadius: '2px' }} />
        <div className="skeleton" style={{ width: '45%', height: '20px', marginBottom: '32px', borderRadius: '2px' }} />

        {/* Paragraph lines */}
        {[100, 95, 88, 100, 92, 78, 100, 85, 60].map((w, i) => (
          <div key={i} className="skeleton" style={{ width: `${w}%`, height: '16px', marginBottom: '10px', borderRadius: '2px' }} />
        ))}

        {/* Code block skeleton */}
        <div style={{ marginTop: '28px', marginBottom: '28px' }}>
          <div className="skeleton" style={{ width: '100%', height: '120px', borderRadius: '2px' }} />
        </div>

        {/* More paragraph lines */}
        {[100, 90, 82, 95, 70].map((w, i) => (
          <div key={i} className="skeleton" style={{ width: `${w}%`, height: '16px', marginBottom: '10px', borderRadius: '2px' }} />
        ))}

        {/* Section card skeleton */}
        <div style={{ marginTop: '40px', border: '1px solid var(--border)', borderTop: '3px solid var(--border)', background: 'var(--bg-card)' }}>
          <div style={{ padding: '18px 20px 14px', borderBottom: '1px solid var(--border-dim)', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div className="skeleton" style={{ width: '24px', height: '24px', borderRadius: '50%' }} />
            <div className="skeleton" style={{ width: '180px', height: '12px', borderRadius: '2px' }} />
          </div>
          <div style={{ padding: '16px 20px 20px', display: 'flex', flexDirection: 'column' as const, gap: '10px' }}>
            {[1, 2].map(i => (
              <div key={i} style={{ border: '1px solid var(--border)', padding: '14px 16px', background: 'var(--bg-surface)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', flexDirection: 'column' as const, gap: '6px' }}>
                  <div className="skeleton" style={{ width: '200px', height: '13px', borderRadius: '2px' }} />
                  <div className="skeleton" style={{ width: '280px', height: '11px', borderRadius: '2px' }} />
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <div className="skeleton" style={{ width: '60px', height: '32px' }} />
                  <div className="skeleton" style={{ width: '80px', height: '32px' }} />
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}

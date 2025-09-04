'use client';

interface Props {
  page: number;
  total: number;
  perPage: number;
  onChange: (p: number) => void;
}

export default function PixelPagination({ page, total, perPage, onChange }: Props) {
  const pages = Math.ceil(total / perPage);
  if (pages <= 1) return null;

  /* build page window: always show first, last, current ±1 */
  const window = new Set<number>();
  window.add(1);
  window.add(pages);
  for (let p = Math.max(1, page - 1); p <= Math.min(pages, page + 1); p++) window.add(p);
  const nums = Array.from(window).sort((a, b) => a - b);

  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px', marginTop: '28px', flexWrap: 'wrap' }}>
      {/* Prev */}
      <button
        className="pag-btn"
        disabled={page === 1}
        onClick={() => onChange(page - 1)}
      >
        ◀ PREV
      </button>

      {/* Page numbers with ellipsis */}
      {nums.map((n, i) => {
        const prev = nums[i - 1];
        const gap  = prev && n - prev > 1;
        return (
          <span key={n} style={{ display: 'inline-flex', gap: '4px', alignItems: 'center' }}>
            {gap && (
              <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '9px', color: 'var(--text-dim)', padding: '0 4px' }}>···</span>
            )}
            <button
              className={`pag-btn ${page === n ? 'active' : ''}`}
              onClick={() => onChange(n)}
            >
              {String(n).padStart(2, '0')}
            </button>
          </span>
        );
      })}

      {/* Next */}
      <button
        className="pag-btn"
        disabled={page === pages}
        onClick={() => onChange(page + 1)}
      >
        NEXT ▶
      </button>

      {/* page info */}
      <span style={{ fontFamily: 'var(--pixel-font)', fontSize: '8px', color: 'var(--text-dim)', marginLeft: '8px', letterSpacing: '0.3px' }}>
        {page}/{pages}
      </span>
    </div>
  );
}

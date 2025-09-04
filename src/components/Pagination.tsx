'use client';

import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  itemsPerPage?: number;
  totalItems?: number;
}

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  itemsPerPage = 10,
  totalItems,
}: PaginationProps) {
  const maxVisiblePages = 7;
  const pageNumbers: (number | string)[] = [];

  if (totalPages <= maxVisiblePages) {
    for (let i = 1; i <= totalPages; i++) {
      pageNumbers.push(i);
    }
  } else {
    pageNumbers.push(1);

    if (currentPage > 4) pageNumbers.push('...');

    const start = Math.max(2, currentPage - 2);
    const end = Math.min(totalPages - 1, currentPage + 2);

    for (let i = start; i <= end; i++) {
      pageNumbers.push(i);
    }

    if (currentPage < totalPages - 3) pageNumbers.push('...');
    pageNumbers.push(totalPages);
  }

  return (
    <div className="flex flex-col items-center gap-4 mt-8">
      {/* Pagination info */}
      {totalItems && (
        <p style={{ color: 'var(--text-muted)', fontSize: '11px', fontFamily: 'var(--mono-font)' }}>
          Page {currentPage} of {totalPages} {itemsPerPage && `· ${itemsPerPage} per page`}
        </p>
      )}

      {/* Pagination controls */}
      <div className="flex items-center gap-2">
        {/* Previous button */}
        <button
          onClick={() => onPageChange(Math.max(1, currentPage - 1))}
          disabled={currentPage === 1}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '32px',
            height: '32px',
            background: currentPage === 1 ? 'var(--bg-surface)' : 'var(--bg-card)',
            border: '1px solid var(--border)',
            cursor: currentPage === 1 ? 'not-allowed' : 'pointer',
            transition: 'all 0.15s',
            opacity: currentPage === 1 ? 0.5 : 1,
          }}
          onMouseEnter={(e) => {
            if (currentPage !== 1) {
              e.currentTarget.style.borderColor = 'var(--accent)';
              e.currentTarget.style.background = 'var(--bg-card-hover)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'var(--border)';
            e.currentTarget.style.background = 'var(--bg-card)';
          }}
        >
          <ChevronLeft size={16} color={currentPage === 1 ? 'var(--text-dim)' : 'var(--text-muted)'} />
        </button>

        {/* Page numbers */}
        {pageNumbers.map((pageNum, idx) => (
          <button
            key={idx}
            onClick={() => typeof pageNum === 'number' && onPageChange(pageNum)}
            disabled={pageNum === '...'}
            style={{
              minWidth: '32px',
              height: '32px',
              padding: '0 8px',
              background: pageNum === currentPage ? 'var(--accent)' : 'var(--bg-card)',
              color: pageNum === currentPage ? '#0b0806' : 'var(--text-muted)',
              border: pageNum === currentPage ? '1px solid var(--accent)' : '1px solid var(--border)',
              fontFamily: 'var(--pixel-font)',
              fontSize: '9px',
              fontWeight: pageNum === currentPage ? 600 : 400,
              cursor: pageNum === '...' ? 'default' : 'pointer',
              transition: 'all 0.15s',
              boxShadow: pageNum === currentPage ? '0 0 8px var(--accent-glow)' : 'none',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
            onMouseEnter={(e) => {
              if (pageNum !== '...' && pageNum !== currentPage) {
                e.currentTarget.style.borderColor = 'var(--accent-border)';
                e.currentTarget.style.background = 'var(--bg-card-hover)';
              }
            }}
            onMouseLeave={(e) => {
              if (pageNum !== '...') {
                e.currentTarget.style.borderColor = pageNum === currentPage ? 'var(--accent)' : 'var(--border)';
                e.currentTarget.style.background = pageNum === currentPage ? 'var(--accent)' : 'var(--bg-card)';
              }
            }}
          >
            {pageNum === '...' ? '•••' : pageNum}
          </button>
        ))}

        {/* Next button */}
        <button
          onClick={() => onPageChange(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage === totalPages}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '32px',
            height: '32px',
            background: currentPage === totalPages ? 'var(--bg-surface)' : 'var(--bg-card)',
            border: '1px solid var(--border)',
            cursor: currentPage === totalPages ? 'not-allowed' : 'pointer',
            transition: 'all 0.15s',
            opacity: currentPage === totalPages ? 0.5 : 1,
          }}
          onMouseEnter={(e) => {
            if (currentPage !== totalPages) {
              e.currentTarget.style.borderColor = 'var(--accent)';
              e.currentTarget.style.background = 'var(--bg-card-hover)';
            }
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = 'var(--border)';
            e.currentTarget.style.background = 'var(--bg-card)';
          }}
        >
          <ChevronRight size={16} color={currentPage === totalPages ? 'var(--text-dim)' : 'var(--text-muted)'} />
        </button>
      </div>
    </div>
  );
}

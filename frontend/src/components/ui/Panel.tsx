import React from 'react';
import clsx from 'clsx';

interface PanelProps { title?: string; children: React.ReactNode; className?: string; noPad?: boolean; onClose?: () => void; }

export const Panel: React.FC<PanelProps> = ({ title, children, className, noPad = false, onClose }) => (
  <div className={clsx('relative flex flex-col panel-bg gold-border rounded-sm', className)}>
    <div className="absolute inset-x-0 top-0 h-[2px] bg-gradient-to-r from-transparent via-gold-400 to-transparent rounded-t-sm" />
    {title && (
      <header className="flex items-center justify-between px-3 pt-2.5 pb-1.5 border-b border-gold-600/50">
        <h3 className="font-cinzel text-xs font-bold tracking-[0.15em] text-gold-300 uppercase">{title}</h3>
        {onClose && (
          <button onClick={onClose} className="w-5 h-5 flex items-center justify-center rounded border border-gold-600 text-gold-400 text-xs hover:bg-gold-600/20 transition-colors">×</button>
        )}
      </header>
    )}
    <div className={clsx('flex-1', !noPad && 'p-3')}>{children}</div>
    <div className="absolute inset-x-0 bottom-0 h-[1px] bg-gradient-to-r from-transparent via-gold-600/40 to-transparent rounded-b-sm" />
  </div>
);

export const SectionLabel: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="flex items-center gap-2 mb-2">
    <div className="h-px flex-1 bg-gradient-to-r from-transparent to-gold-600/40" />
    <span className="font-cinzel text-[10px] font-semibold text-gold-400 tracking-widest uppercase px-1">{children}</span>
    <div className="h-px flex-1 bg-gradient-to-l from-transparent to-gold-600/40" />
  </div>
);

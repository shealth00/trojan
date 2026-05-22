import React from 'react';
import clsx from 'clsx';

interface HexSlotProps {
  icon?: string; label?: string; size?: number;
  equipped?: boolean; empty?: boolean;
  onClick?: () => void; className?: string;
}

export const HexSlot: React.FC<HexSlotProps> = ({ icon, label, size = 52, equipped = false, empty = false, onClick, className }) => {
  const hex = (
    <div
      role={onClick ? 'button' : undefined} tabIndex={onClick ? 0 : undefined}
      onClick={onClick} onKeyDown={(e) => e.key === 'Enter' && onClick?.()}
      className={clsx(
        'relative flex items-center justify-center transition-all duration-200 hex-clip select-none',
        equipped ? 'bg-gradient-to-br from-forest-700 to-forest-900 border-2 border-forest-400'
          : empty ? 'bg-stone-800/60 border border-stone-600'
          : 'bg-gradient-to-br from-stone-700 to-stone-800 border border-gold-600',
        onClick && 'cursor-pointer hover:brightness-125 active:brightness-90',
        className,
      )}
      style={{ width: size, height: size * 0.866 }}
    >
      <div className="hex-clip absolute inset-[2px] bg-gradient-to-b from-white/8 to-transparent pointer-events-none" />
      {icon ? <span className="text-lg leading-none z-10">{icon}</span> : <span className="text-stone-600 text-xs z-10">—</span>}
    </div>
  );
  if (!label) return hex;
  return (
    <div className="flex flex-col items-center gap-0.5">
      {hex}
      <span className="text-[9px] text-parchment-300/70 font-cinzel tracking-wide uppercase">{label}</span>
    </div>
  );
};

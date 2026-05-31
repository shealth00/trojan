import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import { OUTFITS } from '@/data/gameData';
import type { OutfitId } from '@/types/game';

const OUTFIT_PORTRAITS: Record<OutfitId, string> = {
  shepherd_rags:  '🧑',
  goliath_tunic:  '💪',
  jonathan_robe:  '🧝',
  royal_armor:    '👑',
};

interface OutfitCardProps {
  id:          OutfitId;
  name:        string;
  subtitle?:   string;
  incomplete?: boolean;
  locked?:     boolean;
  tags:        string[];
  selected:    boolean;
  onSelect:    () => void;
}

const OutfitCard: React.FC<OutfitCardProps> = ({
  id, name, subtitle, incomplete, locked, tags, selected, onSelect,
}) => (
  <button
    onClick={onSelect}
    disabled={locked}
    className={clsx(
      'flex flex-col rounded border transition-all duration-150 text-left overflow-hidden flex-1',
      locked
        ? 'opacity-50 cursor-not-allowed border-gold-500 bg-gradient-to-b from-gold-700/20 to-stone-900/60'
        : selected
        ? 'border-gold-400 bg-stone-900/80 shadow-[0_0_10px_rgba(201,168,76,0.35)]'
        : 'border-gold-600/30 bg-stone-900/50 hover:border-gold-500/60 cursor-pointer',
    )}
  >
    <div className={clsx(
      'w-full flex items-center justify-center py-4 relative',
      selected ? 'bg-gradient-to-b from-stone-700/60 to-stone-800/60'
        : locked  ? 'bg-gradient-to-b from-gold-700/30 to-gold-900/20'
        : 'bg-gradient-to-b from-stone-700/40 to-stone-800/40',
    )}>
      <span className="text-5xl leading-none select-none"
        style={{ filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.6))' }}>
        {OUTFIT_PORTRAITS[id]}
      </span>
      {incomplete && (
        <span className="absolute top-1 right-1 font-cinzel text-[7px] text-yellow-400/80 bg-yellow-900/40 rounded px-1">
          Incomplete
        </span>
      )}
      {locked && <span className="absolute top-1 right-1 text-sm">🔒</span>}
    </div>
    <div className="px-2 py-1.5 flex flex-col gap-0.5">
      <span className={clsx(
        'font-cinzel text-[9px] font-bold leading-tight uppercase tracking-wide',
        locked ? 'text-gold-400' : selected ? 'text-gold-200' : 'text-gold-300',
      )}>
        {name}
      </span>
      {subtitle && (
        <span className="text-[8px] text-gold-500/60 leading-tight">{subtitle}</span>
      )}
      <div className="flex flex-col gap-px mt-0.5">
        {tags.map((tag) => (
          <span key={tag} className={clsx(
            'text-[8px] leading-tight',
            tag.startsWith('+') ? 'text-green-400/80' : 'text-red-400/70',
          )}>
            {tag}
          </span>
        ))}
      </div>
    </div>
  </button>
);

export const OutfitsPanel: React.FC = () => {
  const currentOutfit = useGameStore((s) => s.currentOutfit);
  const equipOutfit   = useGameStore((s) => s.equipOutfit);

  return (
    <div className="panel-bg p-2">
      <div className="font-cinzel text-[9px] text-gold-500/60 tracking-[0.25em] uppercase pb-1.5 mb-2 border-b border-gold-600/20 text-center">
        Outfits
      </div>
      <div className="flex gap-2">
        {OUTFITS.map((outfit) => (
          <OutfitCard
            key={outfit.id}
            id={outfit.id}
            name={outfit.name}
            subtitle={outfit.subtitle}
            incomplete={outfit.incomplete}
            locked={outfit.locked}
            tags={outfit.tags}
            selected={currentOutfit === outfit.id}
            onSelect={() => equipOutfit(outfit.id)}
          />
        ))}
      </div>
    </div>
  );
};

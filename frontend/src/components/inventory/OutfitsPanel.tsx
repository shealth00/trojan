import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import { Panel } from '@/components/ui/Panel';
import { OUTFITS } from '@/data/gameData';

export const OutfitsPanel: React.FC = () => {
  const currentOutfit = useGameStore((s) => s.currentOutfit);
  const equipOutfit   = useGameStore((s) => s.equipOutfit);
  return (
    <Panel title="Outfits">
      <div className="grid grid-cols-2 gap-2">
        {OUTFITS.map((outfit) => {
          const selected = currentOutfit === outfit.id;
          return (
            <button key={outfit.id} onClick={() => equipOutfit(outfit.id)} disabled={outfit.locked}
              className={clsx('flex flex-col gap-1 p-2 rounded border text-left transition-all duration-150',
                outfit.locked ? 'opacity-40 cursor-not-allowed border-stone-700 bg-stone-900/40'
                  : selected ? 'selected-green border-forest-400 bg-forest-900/40'
                  : 'border-gold-600/30 bg-stone-800/30 hover:border-gold-500 cursor-pointer')}>
              <div className={clsx('w-full aspect-square rounded flex items-center justify-center text-3xl', selected ? 'bg-forest-900/60' : 'bg-stone-900/60')}>
                {outfit.locked ? '🔒' : '🧥'}
              </div>
              <span className={clsx('font-cinzel text-[10px] font-bold leading-tight', selected ? 'text-forest-300' : 'text-gold-300')}>{outfit.name}</span>
              {outfit.subtitle && <span className="text-[9px] text-parchment-200/50">{outfit.subtitle}</span>}
              {outfit.tags.map((tag) => (
                <span key={tag} className={clsx('text-[9px]', tag.startsWith('+') ? 'text-green-400/70' : 'text-red-400/70')}>{tag}</span>
              ))}
            </button>
          );
        })}
      </div>
    </Panel>
  );
};

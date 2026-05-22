import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import { Panel, SectionLabel } from '@/components/ui/Panel';
import { LYRE_STRINGS, BUFF_ICONS } from '@/data/gameData';

export const LyrePanel: React.FC = () => {
  const equippedString = useGameStore((s) => s.equippedString);
  const setLyreString  = useGameStore((s) => s.setLyreString);
  const selected = LYRE_STRINGS.find((s) => s.id === equippedString);
  return (
    <Panel title="Lyre Strings">
      <div className="flex flex-col gap-1.5">
        {LYRE_STRINGS.map((str) => {
          const isSelected = equippedString === str.id;
          const buffIcon = BUFF_ICONS[str.buffType] ?? '🎵';
          return (
            <button key={str.id} onClick={() => !str.locked && setLyreString(str.id)} disabled={str.locked}
              className={clsx('w-full flex items-center gap-2 p-2 rounded border text-left transition-all duration-150',
                str.locked ? 'opacity-40 cursor-not-allowed border-stone-700 bg-stone-900/30'
                  : isSelected ? 'selected-green border-forest-400 bg-forest-900/40'
                  : 'border-gold-600/30 bg-stone-800/30 hover:border-gold-500 cursor-pointer')}>
              <div className={clsx('w-8 h-8 flex-shrink-0 flex items-center justify-center rounded-full text-base border',
                isSelected ? 'border-forest-400 bg-forest-900/60' : 'border-gold-600/30 bg-stone-800/60')}>
                {str.locked ? '🔒' : buffIcon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-baseline gap-1.5">
                  <span className={clsx('font-cinzel text-[11px] font-bold', isSelected ? 'text-forest-300' : 'text-gold-300')}>{str.name}</span>
                  <span className="text-[9px] text-green-400/70 truncate">{str.bonusLabel}</span>
                </div>
                <div className="flex items-center gap-1.5 mt-0.5">
                  <span className="text-[9px] text-parchment-200/50">{str.sound}</span>
                  <span className={clsx('text-[9px] font-cinzel', isSelected ? 'text-forest-400' : 'text-gold-500/70')}>{str.buffType}</span>
                </div>
                <p className="text-[9px] text-parchment-200/40 mt-0.5 leading-tight line-clamp-1">{str.description}</p>
              </div>
              {isSelected && <div className="flex-shrink-0 w-3 h-3 rounded-full bg-forest-400" />}
            </button>
          );
        })}
      </div>
      {selected && (
        <div className="mt-3">
          <SectionLabel>Active Effect</SectionLabel>
          <div className="flex items-center gap-2 p-2 rounded border border-forest-600/40 bg-forest-900/20">
            <span className="text-base">{BUFF_ICONS[selected.buffType] ?? '🎵'}</span>
            <div className="flex flex-col">
              <span className="font-cinzel text-[10px] font-bold text-forest-300">{selected.buffType}</span>
              <span className="text-[9px] text-parchment-200/50">{selected.bonusLabel}</span>
            </div>
          </div>
        </div>
      )}
    </Panel>
  );
};

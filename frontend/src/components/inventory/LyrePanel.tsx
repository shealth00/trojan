import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import { LYRE_STRINGS, BUFF_ICONS } from '@/data/gameData';

const BUFF_COLORS: Record<string, string> = {
  Soothe:           'text-sky-300    bg-sky-900/30    border-sky-600/40',
  Inspire:          'text-orange-300 bg-orange-900/30 border-orange-600/40',
  'Divine Harmony': 'text-purple-300 bg-purple-900/30 border-purple-600/40',
  'Royal Blessing': 'text-gold-300   bg-gold-900/20   border-gold-600/40',
};

interface StringRowProps {
  name:        string;
  bonusLabel:  string;
  sound:       string;
  buffType:    string;
  locked?:     boolean;
  selected:    boolean;
  onSelect:    () => void;
}

const StringRow: React.FC<StringRowProps> = ({
  name, bonusLabel, sound, buffType, locked, selected, onSelect,
}) => {
  const icon = BUFF_ICONS[buffType] ?? '🎵';
  return (
    <button
      onClick={onSelect}
      disabled={locked}
      className={clsx(
        'w-full flex items-center gap-2 px-2 py-1.5 rounded border text-left transition-all duration-150',
        locked
          ? 'opacity-40 cursor-not-allowed border-stone-700 bg-stone-900/30'
          : selected
          ? 'selected-green border-forest-400 shadow-[0_0_6px_rgba(74,222,128,0.25)]'
          : 'border-gold-600/25 bg-stone-800/30 hover:border-gold-500/50 hover:bg-stone-700/40 cursor-pointer',
      )}
    >
      <span className="text-base flex-shrink-0">{locked ? '🔒' : icon}</span>
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline gap-1.5">
          <span className={clsx(
            'font-cinzel text-[9px] font-bold',
            selected ? 'text-forest-200' : 'text-gold-300',
          )}>
            {name}
          </span>
          {!locked && (
            <span className="text-[8px] text-green-400/70 truncate">{bonusLabel}</span>
          )}
        </div>
        <div className="flex items-center gap-1 mt-px">
          <span className="text-[8px] text-parchment-200/40 italic">{sound}</span>
          {locked && <span className="text-[8px] text-stone-500">· Locked</span>}
        </div>
      </div>
      {selected && <span className="text-forest-400 text-sm flex-shrink-0">✓</span>}
    </button>
  );
};

export const LyrePanel: React.FC = () => {
  const equippedString = useGameStore((s) => s.equippedString);
  const setLyreString  = useGameStore((s) => s.setLyreString);
  const active = LYRE_STRINGS.find((s) => s.id === equippedString);

  return (
    <div className="flex flex-col h-full panel-bg">
      <div className="flex items-center justify-between px-3 py-1.5 border-b border-gold-600/30 bg-stone-900/50">
        <span className="font-cinzel text-[9px] text-gold-400 tracking-[0.3em] uppercase">Lyre</span>
        <button className="w-5 h-5 flex items-center justify-center text-stone-500 hover:text-stone-300 text-xs border border-stone-600 rounded-sm transition-colors">✕</button>
      </div>
      <div className="flex flex-1 min-h-0">
        <div className="w-20 flex-shrink-0 flex flex-col items-center justify-center py-3 px-1 bg-stone-900/40 border-r border-gold-600/20">
          <div className="relative select-none" style={{ width: 64, height: 100 }}>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-5xl" style={{ filter: 'drop-shadow(0 2px 6px rgba(201,168,76,0.4))' }}>🎵</span>
            </div>
            {[0,1,2,3,4].map((i) => (
              <div key={i} className="absolute w-px bg-gradient-to-b from-gold-400/60 to-transparent"
                style={{ height: 60, left: `${28 + i * 10}%`, top: '20%' }} />
            ))}
          </div>
          <span className="font-cinzel text-[7px] text-gold-600/50 tracking-widest uppercase mt-1">Lyre</span>
        </div>
        <div className="flex-1 flex flex-col p-2 gap-1.5">
          <span className="font-cinzel text-[8px] text-gold-500/60 tracking-widest uppercase">String Materials</span>
          {LYRE_STRINGS.map((str) => (
            <StringRow
              key={str.id}
              {...str}
              selected={equippedString === str.id}
              onSelect={() => !str.locked && setLyreString(str.id)}
            />
          ))}
        </div>
      </div>
      {active && (
        <div className="border-t border-gold-600/30 p-2">
          <div className="font-cinzel text-[8px] text-gold-600/50 uppercase tracking-widest mb-1.5">Buff Type</div>
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              {LYRE_STRINGS.filter((s) => !s.locked).map((s) => (
                <div key={s.id} className={clsx(
                  'w-7 h-7 flex items-center justify-center rounded border text-xs transition-all',
                  equippedString === s.id
                    ? (BUFF_COLORS[s.buffType] ?? 'text-gold-300 bg-gold-900/20 border-gold-600/40')
                    : 'text-stone-600 bg-stone-900/40 border-stone-700',
                )}>
                  {BUFF_ICONS[s.buffType] ?? '🎵'}
                </div>
              ))}
            </div>
            <div className={clsx(
              'flex-1 flex items-center gap-1.5 px-2 py-1 rounded border',
              BUFF_COLORS[active.buffType] ?? 'text-gold-300 bg-gold-900/20 border-gold-600/40',
            )}>
              <span className="text-xs">{BUFF_ICONS[active.buffType] ?? '🎵'}</span>
              <div className="min-w-0">
                <div className="font-cinzel text-[8px] font-bold leading-tight truncate">{active.buffType}</div>
                <div className="text-[7px] leading-tight opacity-70 truncate">{active.bonusLabel}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

import React from 'react';
import { useGameStore } from '@/store/useGameStore';
import { HexSlot } from '@/components/ui/HexSlot';
import { GEAR_SLOTS, OUTFITS } from '@/data/gameData';

const STAT_CFG = [
  { key: 'attack'  as const, icon: '⚔️',  label: 'ATTACK',  color: 'text-orange-200' },
  { key: 'defense' as const, icon: '🛡️',  label: 'DEFENSE', color: 'text-blue-200'   },
  { key: 'stealth' as const, icon: '👁️',  label: 'STEALTH', color: 'text-green-200'  },
  { key: 'spirit'  as const, icon: '🔥',  label: 'SPIRIT',  color: 'text-sky-200'    },
];

export const CharacterPanel: React.FC = () => {
  const stats         = useGameStore((s) => s.stats);
  const currentOutfit = useGameStore((s) => s.currentOutfit);
  const outfit        = OUTFITS.find((o) => o.id === currentOutfit);

  return (
    <div className="flex" style={{ minHeight: 300 }}>

      {/* ── Stats column ────────────────────────────────────── */}
      <div className="flex flex-col justify-center gap-1 px-2 py-3 w-[72px] flex-shrink-0 bg-stone-900/60 border-r border-gold-600/20">
        {STAT_CFG.map(({ key, icon, label, color }) => (
          <div key={key} className="flex flex-col items-center gap-0.5 py-1.5 px-1 rounded bg-stone-950/60 border border-gold-600/20">
            <span className="text-base leading-none">{icon}</span>
            <span className={`font-cinzel font-bold text-base leading-none ${color}`}>{stats[key]}</span>
            <span className="font-cinzel text-[7px] text-gold-600/50 tracking-widest">{label}</span>
          </div>
        ))}
      </div>

      {/* ── Portrait + gear slots ────────────────────────────── */}
      <div className="relative flex-1 overflow-hidden">
        <div className="absolute inset-0"
          style={{ background: 'linear-gradient(180deg, #6b9ab8 0%, #a0c080 35%, #8b6540 65%, #5a3820 100%)' }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-stone-950/40" />
        <div className="absolute inset-2 border-2 border-gold-500/60 rounded"
          style={{ boxShadow: '0 0 12px rgba(201,168,76,0.25), inset 0 0 8px rgba(0,0,0,0.3)' }}
        />
        <div className="absolute inset-0 flex items-center justify-center pt-4">
          <span className="text-8xl select-none leading-none"
            style={{ filter: 'drop-shadow(0 4px 16px rgba(0,0,0,0.7))' }}>
            🧑
          </span>
        </div>
        {GEAR_SLOTS.map((slot) => (
          <div
            key={slot.id}
            className="absolute z-10"
            style={{ top: slot.pos.top, left: slot.pos.left, transform: 'translate(-50%,-50%)' }}
          >
            <HexSlot icon={slot.icon} size={38} equipped={slot.equipped != null} />
          </div>
        ))}
        <div className="absolute bottom-2 left-2 z-10">
          <div className="bg-stone-950/85 rounded px-2 py-1 border border-gold-600/40"
            style={{ backdropFilter: 'blur(4px)' }}>
            <div className="font-cinzel text-[8px] text-gold-600/60 uppercase tracking-widest">Current:</div>
            <div className="font-cinzel text-[9px] text-gold-300 font-bold leading-tight">{outfit?.name ?? '—'}</div>
            {outfit?.tags[0] && (
              <div className="text-[8px] text-green-400/80 leading-tight">({outfit.tags[0]})</div>
            )}
          </div>
        </div>
      </div>

      {/* ── Craft / Equip buttons ────────────────────────────── */}
      <div className="flex flex-col justify-end gap-2 px-1.5 py-3 w-12 flex-shrink-0 bg-stone-900/60 border-l border-gold-600/20">
        <button className="flex flex-col items-center gap-0.5 p-1 rounded border border-gold-600/40 bg-stone-800/60 hover:bg-stone-700/70 transition-colors">
          <span className="text-sm">🔨</span>
          <span className="font-cinzel text-[7px] text-gold-500 tracking-wider">Craft</span>
        </button>
        <button className="flex flex-col items-center gap-0.5 p-1 rounded border border-gold-400/70 bg-gold-600/20 hover:bg-gold-600/30 transition-colors pulse-gold">
          <span className="text-sm">🧥</span>
          <span className="font-cinzel text-[7px] text-gold-300 tracking-wider">Equip</span>
        </button>
      </div>

    </div>
  );
};

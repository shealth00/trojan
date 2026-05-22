import React from 'react';
import { useGameStore } from '@/store/useGameStore';
import { HexSlot } from '@/components/ui/HexSlot';
import { StatBadge } from '@/components/ui/StatBadge';
import { Panel } from '@/components/ui/Panel';
import { GEAR_SLOTS } from '@/data/gameData';

export const CharacterPanel: React.FC = () => {
  const stats = useGameStore((s) => s.stats);
  return (
    <Panel title="David" className="h-full">
      <div className="flex gap-3 h-full">
        <div className="relative flex-1 min-h-[320px]">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-24 h-40 rounded-full bg-gradient-to-b from-stone-600/40 to-stone-800/40 border border-gold-600/20 flex items-end justify-center pb-2">
              <span className="text-4xl select-none">🧍</span>
            </div>
          </div>
          {GEAR_SLOTS.map((slot) => (
            <div key={slot.id} className="absolute" style={{ top: slot.pos.top, left: slot.pos.left }}>
              <HexSlot icon={slot.icon} label={slot.label} size={44} equipped={slot.equipped != null} />
            </div>
          ))}
        </div>
        <div className="flex flex-col gap-1.5 justify-center">
          <StatBadge stat="attack"  value={stats.attack}  />
          <StatBadge stat="defense" value={stats.defense} />
          <StatBadge stat="stealth" value={stats.stealth} />
          <StatBadge stat="spirit"  value={stats.spirit}  />
        </div>
      </div>
    </Panel>
  );
};

import React from 'react';

type StatKey = 'attack' | 'defense' | 'stealth' | 'spirit';
const STAT_CFG = {
  attack:  { icon: '⚔️',  label: 'Attack',  color: 'text-orange-300', bg: 'bg-orange-900/30' },
  defense: { icon: '🛡️',  label: 'Defense', color: 'text-blue-300',   bg: 'bg-blue-900/30'   },
  stealth: { icon: '🌑',  label: 'Stealth', color: 'text-green-300',  bg: 'bg-green-900/30'  },
  spirit:  { icon: '🔥',  label: 'Spirit',  color: 'text-sky-300',    bg: 'bg-sky-900/30'    },
};

export const StatBadge: React.FC<{ stat: StatKey; value: number }> = ({ stat, value }) => {
  const cfg = STAT_CFG[stat];
  return (
    <div className={`flex items-center gap-1.5 px-2 py-1 rounded ${cfg.bg} border border-white/10`}>
      <span className="text-base leading-none">{cfg.icon}</span>
      <div className="flex flex-col leading-none">
        <span className={`font-cinzel font-bold text-sm ${cfg.color}`}>{value}</span>
        <span className="text-[9px] text-parchment-200/50 uppercase tracking-widest">{cfg.label}</span>
      </div>
    </div>
  );
};

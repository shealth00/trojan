import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import type { UpgradeTier } from '@/types/game';

const TIER_ICONS: Record<string, string> = {
  cured_goat:   '🐐',
  lion_skin:    '🦁',
  bear_hide:    '🐻',
  standard:     '🧵',
  braided_long: '🪢',
  woven_silk:   '🌊',
  river_smooth: '🪨',
  jagged:       '💠',
  fire_stones:  '🔥',
};

interface TierCardProps {
  tier:     UpgradeTier;
  selected: boolean;
  onSelect: () => void;
}

const TierCard: React.FC<TierCardProps> = ({ tier, selected, onSelect }) => (
  <button
    onClick={onSelect}
    disabled={tier.locked}
    className={clsx(
      'flex flex-col items-center gap-1 py-2 px-1.5 rounded border transition-all duration-150 flex-1',
      tier.locked
        ? 'opacity-40 cursor-not-allowed border-stone-700 bg-stone-900/40'
        : selected
        ? 'border-gold-400 bg-forest-900/70 shadow-[0_0_8px_rgba(74,222,128,0.3)] selected-green'
        : 'border-gold-600/30 bg-stone-800/50 hover:border-gold-500/60 hover:bg-stone-700/50 cursor-pointer',
    )}
  >
    <span className="text-2xl leading-none">
      {tier.locked ? '🔒' : (TIER_ICONS[tier.id] ?? '❓')}
    </span>
    <span className={clsx(
      'font-cinzel text-[9px] font-bold text-center leading-tight',
      selected ? 'text-forest-200' : 'text-gold-300',
    )}>
      {tier.name}
    </span>
    {tier.bonuses.length > 0 && (
      <div className="flex flex-col items-center gap-px">
        {tier.bonuses.map((b) => (
          <span key={b} className="text-[8px] text-green-400/70">{b}</span>
        ))}
      </div>
    )}
    {tier.cost && (
      <div className="flex items-center gap-1.5 mt-0.5">
        {tier.cost.gems != null && (
          <span className="text-[8px] text-sky-300">💎 {tier.cost.gems}</span>
        )}
        {tier.cost.coins != null && (
          <span className="text-[8px] text-yellow-400">🪙 {tier.cost.coins}</span>
        )}
      </div>
    )}
  </button>
);

const Arrow: React.FC = () => (
  <div className="flex items-center justify-center w-4 flex-shrink-0 text-gold-600/60 text-lg select-none">›</div>
);

export const SlingUpgradesPanel: React.FC = () => {
  const slingCategories = useGameStore((s) => s.slingCategories);
  const selectSlingTier = useGameStore((s) => s.selectSlingTier);

  return (
    <div className="h-full panel-bg p-3 flex flex-col gap-3">
      <div className="font-cinzel text-[10px] text-gold-400 tracking-[0.3em] uppercase pb-1 border-b border-gold-600/30">
        Sling Upgrades
      </div>
      {slingCategories.map((cat) => (
        <div key={cat.id} className="flex items-center gap-2">
          <div className="w-20 flex-shrink-0">
            <span className="font-cinzel text-[9px] text-gold-500/70 tracking-wide">{cat.label}</span>
          </div>
          <div className="flex items-stretch gap-0 flex-1">
            {cat.tiers.map((tier, idx) => (
              <React.Fragment key={tier.id}>
                {idx > 0 && <Arrow />}
                <TierCard
                  tier={tier}
                  selected={cat.selected === idx}
                  onSelect={() => selectSlingTier(cat.id, idx)}
                />
              </React.Fragment>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

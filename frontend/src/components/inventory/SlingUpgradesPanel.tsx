import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import { Panel, SectionLabel } from '@/components/ui/Panel';
import type { UpgradeTier } from '@/types/game';

const TierButton: React.FC<{ tier: UpgradeTier; selected: boolean; onSelect: () => void }> = ({ tier, selected, onSelect }) => (
  <button onClick={onSelect} disabled={tier.locked}
    className={clsx('flex-1 flex flex-col items-center gap-0.5 py-1.5 px-1 rounded border transition-all duration-150',
      tier.locked ? 'opacity-40 cursor-not-allowed border-stone-700 bg-stone-900/40'
        : selected ? 'selected-green border-forest-400 bg-forest-900/50'
        : 'border-gold-600/40 bg-stone-800/40 hover:border-gold-500 cursor-pointer')}>
    <span className={clsx('font-cinzel text-[10px] font-semibold tracking-wide', selected ? 'text-forest-300' : 'text-gold-300')}>{tier.name}</span>
    {tier.bonuses.length > 0 && tier.bonuses.map((b) => <span key={b} className="text-[9px] text-parchment-200/60">{b}</span>)}
    {tier.cost && (
      <div className="flex items-center gap-1 mt-0.5">
        {tier.cost.gems != null && <span className="text-[9px] text-gem-blue">💎{tier.cost.gems}</span>}
        {tier.cost.coins != null && <span className="text-[9px] text-yellow-400">🪙{tier.cost.coins}</span>}
      </div>
    )}
    {tier.locked && <span className="text-[9px] text-stone-500 mt-0.5">🔒 Locked</span>}
  </button>
);

const TierConnector: React.FC = () => (
  <div className="flex flex-col items-center justify-center gap-0.5 px-0.5">
    {[0,1,2].map((i) => <div key={i} className="w-1 h-1 rounded-full bg-gold-600/50" />)}
  </div>
);

export const SlingUpgradesPanel: React.FC = () => {
  const slingCategories = useGameStore((s) => s.slingCategories);
  const selectSlingTier = useGameStore((s) => s.selectSlingTier);
  return (
    <Panel title="Sling Upgrades" className="h-full">
      <div className="flex flex-col gap-3">
        {slingCategories.map((cat) => (
          <div key={cat.id}>
            <SectionLabel>{cat.label}</SectionLabel>
            <div className="flex items-stretch gap-1">
              {cat.tiers.map((tier, idx) => (
                <React.Fragment key={tier.id}>
                  {idx > 0 && <TierConnector />}
                  <TierButton tier={tier} selected={cat.selected === idx} onSelect={() => selectSlingTier(cat.id, idx)} />
                </React.Fragment>
              ))}
            </div>
          </div>
        ))}
      </div>
    </Panel>
  );
};

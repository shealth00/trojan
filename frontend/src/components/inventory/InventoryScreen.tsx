import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import type { GameState } from '@/types/game';
import { CharacterPanel } from './CharacterPanel';
import { SlingUpgradesPanel } from './SlingUpgradesPanel';
import { OutfitsPanel } from './OutfitsPanel';
import { LyrePanel } from './LyrePanel';

type Tab = 'gear' | 'back' | 'aerights' | 'stones';
const NAV_TABS: { id: Tab; label: string; icon: string }[] = [
  { id: 'gear', label: 'Gear', icon: '⚔️' }, { id: 'back', label: 'Back', icon: '🎒' },
  { id: 'aerights', label: 'Aerights', icon: '📜' }, { id: 'stones', label: 'Stones', icon: '🪨' },
];
const INVENTORY_TABS: { id: GameState['inventoryTab']; label: string }[] = [
  { id: 'outfits', label: 'Outfits' }, { id: 'weapons', label: 'Weapons' }, { id: 'consumables', label: 'Consumables' },
];

export const InventoryScreen: React.FC = () => {
  const activeTab       = useGameStore((s) => s.activeTab);
  const inventoryTab    = useGameStore((s) => s.inventoryTab);
  const setActiveTab    = useGameStore((s) => s.setActiveTab);
  const setInventoryTab = useGameStore((s) => s.setInventoryTab);

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col items-center justify-center p-4 font-lato">
      <div className="w-full max-w-5xl flex flex-col gap-0">
        <nav className="flex items-center gap-1 px-2 pt-2 pb-0 panel-bg border border-b-0 border-gold-600/50 rounded-t-sm">
          {NAV_TABS.map((t) => (
            <button key={t.id} onClick={() => setActiveTab(t.id)}
              className={clsx('flex items-center gap-1.5 px-3 py-1.5 rounded-t font-cinzel text-xs tracking-wide transition-colors',
                activeTab === t.id ? 'bg-stone-800 text-gold-300 border border-b-0 border-gold-600/50 -mb-px' : 'text-gold-500/60 hover:text-gold-400 hover:bg-stone-800/40')}>
              <span>{t.icon}</span>{t.label}
            </button>
          ))}
          <div className="ml-auto flex items-center gap-3 pr-1 pb-1">
            <div className="flex items-center gap-1 text-xs"><span>💎</span><span className="font-cinzel text-gem-blue font-bold">12</span></div>
            <div className="flex items-center gap-1 text-xs"><span>🪙</span><span className="font-cinzel text-yellow-400 font-bold">85</span></div>
          </div>
        </nav>
        <div className="panel-bg gold-border rounded-b-sm p-3">
          {activeTab === 'gear' && (
            <div className="flex gap-3">
              <div className="flex flex-col gap-3 w-[280px] flex-shrink-0">
                <CharacterPanel />
                <SlingUpgradesPanel />
              </div>
              <div className="flex flex-col gap-3 flex-1 min-w-0">
                <div className="flex gap-1 border-b border-gold-600/30 pb-2">
                  {INVENTORY_TABS.map((t) => (
                    <button key={t.id} onClick={() => setInventoryTab(t.id)}
                      className={clsx('px-3 py-1 font-cinzel text-[10px] tracking-widest uppercase rounded transition-colors',
                        inventoryTab === t.id ? 'bg-gold-600/20 text-gold-300 border border-gold-600/50' : 'text-gold-500/50 hover:text-gold-400')}>
                      {t.label}
                    </button>
                  ))}
                </div>
                {inventoryTab === 'outfits' && (
                  <div className="flex gap-3">
                    <div className="flex-1 min-w-0"><OutfitsPanel /></div>
                    <div className="w-56 flex-shrink-0"><LyrePanel /></div>
                  </div>
                )}
                {inventoryTab !== 'outfits' && (
                  <div className="flex items-center justify-center h-40 text-gold-500/30 font-cinzel text-sm tracking-widest uppercase">
                    — {INVENTORY_TABS.find((t) => t.id === inventoryTab)?.label} —
                  </div>
                )}
              </div>
            </div>
          )}
          {activeTab !== 'gear' && (
            <div className="flex items-center justify-center h-48 text-gold-500/30 font-cinzel text-sm tracking-widest uppercase">
              — {NAV_TABS.find((t) => t.id === activeTab)?.label} —
            </div>
          )}
        </div>
        <div className="text-center mt-2">
          <span className="font-cinzel text-[9px] text-gold-600/30 tracking-[0.3em] uppercase">Inventory &amp; Upgrades</span>
        </div>
      </div>
    </div>
  );
};

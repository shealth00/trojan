import React from 'react';
import clsx from 'clsx';
import { useGameStore } from '@/store/useGameStore';
import type { GameState } from '@/types/game';
import { CharacterPanel } from './CharacterPanel';
import { SlingUpgradesPanel } from './SlingUpgradesPanel';
import { OutfitsPanel } from './OutfitsPanel';
import { LyrePanel } from './LyrePanel';

type Tab = GameState['activeTab'];

const NAV_TABS: { id: Tab; label: string }[] = [
  { id: 'gear',     label: 'GEAR'     },
  { id: 'back',     label: 'BACK'     },
  { id: 'aerights', label: 'AERIGHTS' },
  { id: 'stones',   label: 'STTOES'   },
];

export const InventoryScreen: React.FC = () => {
  const activeTab    = useGameStore((s) => s.activeTab);
  const setActiveTab = useGameStore((s) => s.setActiveTab);

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col items-center justify-center p-3 font-lato">
      <div className="w-full max-w-4xl shadow-2xl">

        <div className="panel-bg gold-border-thick rounded-t px-4 py-2 flex items-center justify-between">
          <div>
            <h1 className="font-cinzel text-xl font-black text-gold-300 shimmer-gold tracking-wider">
              The Shepherd King
            </h1>
            <p className="font-cinzel text-[9px] text-gold-600/60 tracking-[0.3em] uppercase mt-0.5">
              Inventory &amp; Upgrades
            </p>
          </div>
          <div className="flex items-center gap-0.5">
            <span className="font-cinzel text-[10px] text-gold-600/40 px-1 select-none">◀</span>
            {NAV_TABS.map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={clsx(
                  'px-3 py-1.5 font-cinzel text-[10px] tracking-widest transition-colors border-b-2',
                  activeTab === t.id
                    ? 'text-gold-200 border-gold-400'
                    : 'text-gold-600/50 border-transparent hover:text-gold-400',
                )}
              >
                {t.label}
              </button>
            ))}
            <span className="font-cinzel text-[10px] text-gold-600/40 px-1 select-none">▶</span>
            <button className="ml-2 w-6 h-6 flex items-center justify-center text-stone-400 hover:text-red-400 text-xs border border-stone-600 rounded-sm transition-colors">
              ✕
            </button>
          </div>
        </div>

        {activeTab === 'gear' && (
          <>
            <div className="flex border-x border-gold-600/40">
              <div className="w-[42%] flex-shrink-0 border-r border-gold-600/40">
                <CharacterPanel />
              </div>
              <div className="flex-1 min-w-0">
                <SlingUpgradesPanel />
              </div>
            </div>
            <div className="flex border border-gold-600/40 rounded-b">
              <div className="flex-1 min-w-0 border-r border-gold-600/40">
                <div className="flex items-center gap-2 px-3 py-1.5 border-b border-gold-600/30 bg-stone-900/50">
                  <span>🛡️</span>
                  <span className="font-cinzel text-[9px] text-gold-400 tracking-[0.25em] uppercase">
                    Inventory &amp; Upgrad
                  </span>
                </div>
                <OutfitsPanel />
              </div>
              <div className="w-64 flex-shrink-0">
                <LyrePanel />
              </div>
            </div>
          </>
        )}

        {activeTab !== 'gear' && (
          <div className="panel-bg border border-gold-600/40 rounded-b flex items-center justify-center h-48 text-gold-500/30 font-cinzel text-sm tracking-widest uppercase">
            — {NAV_TABS.find((t) => t.id === activeTab)?.label} —
          </div>
        )}

      </div>
    </div>
  );
};

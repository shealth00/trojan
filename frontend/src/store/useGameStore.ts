import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import type { GameState, OutfitId, LyreStringId, UpgradeCategory } from '@/types/game';
import { BASE_STATS, SLING_CATEGORIES, OUTFITS } from '@/data/gameData';

interface Actions {
  equipOutfit:        (id: OutfitId)      => void;
  setLyreString:      (id: LyreStringId)  => void;
  selectSlingTier:    (categoryId: string, tierIndex: number) => void;
  setActiveTab:       (tab: GameState['activeTab'])       => void;
  setInventoryTab:    (tab: GameState['inventoryTab'])    => void;
}

export const useGameStore = create<GameState & Actions>()(
  immer((set) => ({
    /* ── Initial state ─────────────────────────────────────── */
    stats:           { ...BASE_STATS },
    currentOutfit:   'shepherd_rags',
    slingCategories: SLING_CATEGORIES,
    equippedString:  'silver',
    activeTab:       'gear',
    inventoryTab:    'outfits',

    /* ── Actions ───────────────────────────────────────────── */
    equipOutfit: (id) =>
      set((s) => {
        const prev = OUTFITS.find((o) => o.id === s.currentOutfit);
        const next = OUTFITS.find((o) => o.id === id);
        if (!next || next.locked) return;

        // Remove previous outfit bonuses/penalties
        if (prev) {
          Object.entries(prev.bonuses).forEach(([k, v]) => {
            (s.stats as Record<string, number>)[k] -= v ?? 0;
          });
          Object.entries(prev.penalties ?? {}).forEach(([k, v]) => {
            (s.stats as Record<string, number>)[k] += v ?? 0;
          });
        }

        // Apply new outfit
        Object.entries(next.bonuses).forEach(([k, v]) => {
          (s.stats as Record<string, number>)[k] += v ?? 0;
        });
        Object.entries(next.penalties ?? {}).forEach(([k, v]) => {
          (s.stats as Record<string, number>)[k] -= v ?? 0;
        });

        s.currentOutfit = id;
      }),

    setLyreString: (id) =>
      set((s) => {
        s.equippedString = id;
        // Spirit bonus from lyre strings
        const spiritMap: Record<LyreStringId, number> = {
          gut: 5, bronze: 0, silver: 10, gold: 20,
        };
        // Reset spirit to base + current outfit
        s.stats.spirit = BASE_STATS.spirit + (spiritMap[id] ?? 0);
      }),

    selectSlingTier: (categoryId, tierIndex) =>
      set((s) => {
        const cat = s.slingCategories.find((c: UpgradeCategory) => c.id === categoryId);
        if (!cat || cat.tiers[tierIndex]?.locked) return;
        cat.selected = tierIndex;
      }),

    setActiveTab: (tab) =>
      set((s) => { s.activeTab = tab; }),

    setInventoryTab: (tab) =>
      set((s) => { s.inventoryTab = tab; }),
  })),
);

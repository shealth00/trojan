export interface PlayerStats { attack: number; defense: number; stealth: number; spirit: number; }
export type OutfitId = 'shepherd_rags' | 'goliath_tunic' | 'jonathan_robe' | 'royal_armor';
export interface OutfitDef { id: OutfitId; name: string; subtitle?: string; incomplete?: boolean; locked?: boolean; bonuses: Partial<PlayerStats>; penalties?: Partial<PlayerStats>; tags: string[]; }
export interface UpgradeTier { id: string; name: string; cost?: { gems?: number; coins?: number }; bonuses: string[]; locked?: boolean; }
export interface UpgradeCategory { id: string; label: string; tiers: UpgradeTier[]; selected: number; }
export type LyreStringId = 'gut' | 'bronze' | 'silver' | 'gold';
export interface LyreStringDef { id: LyreStringId; name: string; bonusLabel: string; sound: string; description: string; buffType: string; locked?: boolean; }
export interface GearSlotDef { id: string; label: string; icon: string; equipped?: string; pos: { top: string; left: string }; }
export interface GameState { stats: PlayerStats; currentOutfit: OutfitId; slingCategories: UpgradeCategory[]; equippedString: LyreStringId; activeTab: 'gear' | 'back' | 'aerights' | 'stones'; inventoryTab: 'outfits' | 'weapons' | 'consumables'; }

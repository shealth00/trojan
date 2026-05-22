import type { OutfitDef, UpgradeCategory, LyreStringDef, GearSlotDef, PlayerStats } from '@/types/game';

export const BASE_STATS: PlayerStats = { attack: 25, defense: 10, stealth: 23, spirit: 9 };

export const OUTFITS: OutfitDef[] = [
  { id: 'shepherd_rags',  name: "Shepherd's Rags",    bonuses: { stealth: 10 }, penalties: { defense: 2 }, tags: ['+10 Stealth', '-2 Defense'] },
  { id: 'goliath_tunic',  name: "Goliath's Tunic",    subtitle: '(Incomplete)', incomplete: true, bonuses: { attack: 8, defense: 5 }, penalties: { stealth: 4 }, tags: ['+8 Attack', '+5 Defense', '-4 Stealth'] },
  { id: 'jonathan_robe',  name: "Jonathan's Robe",    subtitle: '+5 Courage', bonuses: { defense: 3, spirit: 3 }, tags: ['+3 Defense', '+3 Spirit'] },
  { id: 'royal_armor',    name: 'Royal Armor',         bonuses: { defense: 25 }, penalties: { stealth: 5 }, tags: ['+25 Defense', '-5 Stealth'], locked: true },
];

export const SLING_CATEGORIES: UpgradeCategory[] = [
  { id: 'leather', label: 'Leather Quality', selected: 1, tiers: [
    { id: 'cured_goat', name: 'Cured Goat', cost: { gems: 3, coins: 5 }, bonuses: [] },
    { id: 'lion_skin',  name: 'Lion Skin',  bonuses: ['+5 Damage', '+2 Range'] },
    { id: 'bear_hide',  name: 'Bear Hide',  cost: { gems: 3, coins: 10 }, bonuses: ['+12 Damage', '+4 Range'] },
  ]},
  { id: 'twine', label: 'Twine Length', selected: 1, tiers: [
    { id: 'standard',     name: 'Standard',     bonuses: [] },
    { id: 'braided_long', name: 'Braided Long', bonuses: ['+10 Range'] },
    { id: 'woven_silk',   name: 'Woven Silk',   bonuses: ['+20 Range', '+5% Crit'], locked: true },
  ]},
  { id: 'stone_pouch', label: 'Stone Pouch', selected: 0, tiers: [
    { id: 'river_smooth', name: 'River Smooth', bonuses: [] },
    { id: 'jagged',       name: 'Jagged',       bonuses: ['+3 Damage', 'Bleeds'] },
    { id: 'fire_stones',  name: 'Fire Stones',  bonuses: ['+8 Damage', '+Fire DoT'], locked: true },
  ]},
];

export const LYRE_STRINGS: LyreStringDef[] = [
  { id: 'gut',    name: 'Gut Strings',    bonusLabel: '+5 Spirit',           sound: 'Soothing Sound', description: 'Natural gut strings produce a warm, calming tone.', buffType: 'Soothe' },
  { id: 'bronze', name: 'Bronze Strings', bonusLabel: '+5 Attack Buff to Allies', sound: 'Resonant Sound', description: 'Bronze wire rings with a bold martial tone.', buffType: 'Inspire' },
  { id: 'silver', name: 'Silver Strings', bonusLabel: '+10 Spirit',          sound: 'Divine Sound',   description: 'Pure silver strings carry heavenly harmonics.', buffType: 'Divine Harmony' },
  { id: 'gold',   name: 'Gold Strings',   bonusLabel: 'Ultimate Buffs',      sound: 'Royal Lyre',     description: 'The legendary gold-strung lyre of the High King.', buffType: 'Royal Blessing', locked: true },
];

export const GEAR_SLOTS: GearSlotDef[] = [
  { id: 'weapon', label: 'Weapon', icon: '⚔️', pos: { top: '8%',  left: '10%' } },
  { id: 'sling',  label: 'Sling',  icon: '🪃', pos: { top: '8%',  left: '78%' } },
  { id: 'shield', label: 'Shield', icon: '🛡️', pos: { top: '38%', left: '4%'  } },
  { id: 'staff',  label: 'Staff',  icon: '🪄', pos: { top: '38%', left: '82%' } },
  { id: 'boots',  label: 'Boots',  icon: '👢', pos: { top: '70%', left: '10%' } },
  { id: 'cloak',  label: 'Cloak',  icon: '🧥', pos: { top: '70%', left: '78%' } },
  { id: 'lyre',   label: 'Lyre',   icon: '🎵', pos: { top: '80%', left: '62%' } },
  { id: 'pouch',  label: 'Pouch',  icon: '👜', pos: { top: '80%', left: '28%' } },
];

export const BUFF_ICONS: Record<string, string> = {
  Soothe: '🎵', Inspire: '⚔️', 'Divine Harmony': '✨', 'Royal Blessing': '👑',
};

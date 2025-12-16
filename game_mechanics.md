# Game Mechanics

## Character

### Main attributes
- Strength (STR)
- Agility (AGI)
- Mind (MND)

## Derived attributes

### Health Points (HP)
- Derived from STR. Maximum HP is equal to 5 * STR

### Attack Power (ATK)
- Bare Hand ATK is equal to 1d4
- Derived from STR or AGI based on the weapon.
    - Strength based: 1d6 + (STR / 2)
    - Agility based: 1d6 + (AGI / 2)

### Defense (DEF)
- No armor DEF (base DEF) is equal to 1. 
- Add the armor DEF value to the base DEF of 1

## Weapons
- STR/AGI based weapon: 1d6


## Armor
- Body: used to add DEF

## Magic
- Anyone can cast spell
- Spell casting is a MND based skill.
- Casting spells cost mana
- Mana regenerates over time
    - Mana regen rate: (2 * MND) per turn
- Mana capacity is equal to (5 * MND) 

For mage with MND stat == 8,
    mana capacity would be (5 * 8) = 40
    mana regen rate: (2 * 8) = 16 per turn

Fireball spell costs 25 mana and does 2d3 damage to the target.

## Spell slots
- Mage can cast up to 3 spells at a time.
- Each slot has its own cost in mana. 

| MND | Mana Capacity | Regen / turn | Net mana change per turn (regen − 25) | Max consecutive casts from full |
|-----:|---------------:|-------------:|--------------------------------------:|--------------------------------:|
| 1 | 5  | 2  | -23 | 0 |
| 2 | 10 | 4  | -21 | 0 |
| 3 | 15 | 6  | -19 | 0 |
| 4 | 20 | 8  | -17 | 0 |
| 5 | 25 | 10 | -15 | 1 |
| 6 | 30 | 12 | -13 | 1 |
| 7 | 35 | 14 | -11 | 1 |
| 8 | 40 | 16 | -9  | 2 |
| 9 | 45 | 18 | -7  | 3 |
| 10 | 50 | 20 | -5  | 6 |
| 11 | 55 | 22 | -3  | 11 |
| 12 | 60 | 24 | -1  | 36 |
| 13 | 65 | 26 | +1  | Sustained (infinite casts) |

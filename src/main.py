import argparse
import sys

# ============================================================
# USER CONFIGURATION – default save file location
SAVE_FILE_PATH = r"examples/sample.sav"
# ============================================================

SRAM_SIZE = 0x8000
BANK_SIZE = 0x2000

# Absolute offsets in a standard 32 KiB Gen I SRAM dump (bank 1 = 0x2000–0x3FFF)
OFFSETS = {
    "PLAYER_NAME": 0x2598,
    "MONEY": 0x25F3,
    "RIVAL_NAME": 0x25F6,
    "BADGES": 0x2602,
    "BAG_ITEMS": 0x25CA,
    "PC_ITEMS": 0x27E7,
    "PARTY": 0x2F2C,
    "CHECKSUM_START": 0x2598,
    "CHECKSUM_END": 0x3523,
    "MAIN_CHECKSUM": 0x3523,
}

# ---------- Gen I English Character Mapping (partial) ----------
CHAR_MAP = {
    0x50: '',        # terminator
    0x7F: ' ',
    0x80: 'A', 0x81: 'B', 0x82: 'C', 0x83: 'D', 0x84: 'E',
    0x85: 'F', 0x86: 'G', 0x87: 'H', 0x88: 'I', 0x89: 'J',
    0x8A: 'K', 0x8B: 'L', 0x8C: 'M', 0x8D: 'N', 0x8E: 'O',
    0x8F: 'P', 0x90: 'Q', 0x91: 'R', 0x92: 'S', 0x93: 'T',
    0x94: 'U', 0x95: 'V', 0x96: 'W', 0x97: 'X', 0x98: 'Y',
    0x99: 'Z',
    0xA0: 'a', 0xA1: 'b', 0xA2: 'c', 0xA3: 'd', 0xA4: 'e',
    0xA5: 'f', 0xA6: 'g', 0xA7: 'h', 0xA8: 'i', 0xA9: 'j',
    0xAA: 'k', 0xAB: 'l', 0xAC: 'm', 0xAD: 'n', 0xAE: 'o',
    0xAF: 'p', 0xB0: 'q', 0xB1: 'r', 0xB2: 's', 0xB3: 't',
    0xB4: 'u', 0xB5: 'v', 0xB6: 'w', 0xB7: 'x', 0xB8: 'y',
    0xB9: 'z',
    0xF6: '0', 0xF7: '1', 0xF8: '2', 0xF9: '3',
    0xFA: '4', 0xFB: '5', 0xFC: '6', 0xFD: '7',
    0xFE: '8', 0xFF: '9',
}

# ---------- Species ID to Name (Gen I) ----------
SPECIES_NAMES = {
    0x01: "Rhydon", 0x02: "Kangaskhan", 0x03: "Nidoran♂", 0x04: "Clefairy",
    0x05: "Spearow", 0x06: "Voltorb", 0x07: "Nidoking", 0x08: "Slowbro",
    0x09: "Ivysaur", 0x0A: "Exeggutor", 0x0B: "Lickitung", 0x0C: "Exeggcute",
    0x0D: "Grimer", 0x0E: "Gengar", 0x0F: "Nidoran♀", 0x10: "Nidoqueen",
    0x11: "Cubone", 0x12: "Rhyhorn", 0x13: "Lapras", 0x14: "Arcanine",
    0x15: "Mew", 0x16: "Gyarados", 0x17: "Shellder", 0x18: "Tentacool",
    0x19: "Gastly", 0x1A: "Scyther", 0x1B: "Staryu", 0x1C: "Blastoise",
    0x1D: "Pinsir", 0x1E: "Tangela", 0x1F: "MissingNo.", 0x20: "MissingNo.",
    0x21: "Growlithe", 0x22: "Onix", 0x23: "Fearow", 0x24: "Pidgey",
    0x25: "Slowpoke", 0x26: "Kadabra", 0x27: "Graveler", 0x28: "Chansey",
    0x29: "Machoke", 0x2A: "Mr. Mime", 0x2B: "Hitmonlee", 0x2C: "Hitmonchan",
    0x2D: "Arbok", 0x2E: "Parasect", 0x2F: "Psyduck", 0x30: "Drowzee",
    0x31: "Golem", 0x32: "MissingNo.", 0x33: "Magmar", 0x34: "MissingNo.",
    0x35: "Electabuzz", 0x36: "Magneton", 0x37: "Koffing", 0x38: "MissingNo.",
    0x39: "Mankey", 0x3A: "Seel", 0x3B: "Diglett", 0x3C: "Tauros",
    0x3D: "MissingNo.", 0x3E: "MissingNo.", 0x3F: "MissingNo.", 0x40: "Farfetch'd",
    0x41: "Venonat", 0x42: "Dragonite", 0x43: "MissingNo.", 0x44: "MissingNo.",
    0x45: "MissingNo.", 0x46: "Doduo", 0x47: "Poliwag", 0x48: "Jynx",
    0x49: "Moltres", 0x4A: "Articuno", 0x4B: "Zapdos", 0x4C: "Ditto",
    0x4D: "Meowth", 0x4E: "Krabby", 0x4F: "MissingNo.", 0x50: "MissingNo.",
    0x51: "MissingNo.", 0x52: "Vulpix", 0x53: "Ninetales", 0x54: "Pikachu",
    0x55: "Raichu", 0x56: "MissingNo.", 0x57: "MissingNo.", 0x58: "Dratini",
    0x59: "Dragonair", 0x5A: "Kabuto", 0x5B: "Kabutops", 0x5C: "Horsea",
    0x5D: "Seadra", 0x5E: "MissingNo.", 0x5F: "MissingNo.", 0x60: "Sandshrew",
    0x61: "Sandslash", 0x62: "Omanyte", 0x63: "Omastar", 0x64: "Jigglypuff",
    0x65: "Wigglytuff", 0x66: "Eevee", 0x67: "Flareon", 0x68: "Jolteon",
    0x69: "Vaporeon", 0x6A: "Machop", 0x6B: "Zubat", 0x6C: "Ekans",
    0x6D: "Paras", 0x6E: "Poliwhirl", 0x6F: "Poliwrath", 0x70: "Weedle",
    0x71: "Kakuna", 0x72: "Beedrill", 0x73: "MissingNo.", 0x74: "Dodrio",
    0x75: "Primeape", 0x76: "Dugtrio", 0x77: "Venomoth", 0x78: "Dewgong",
    0x79: "MissingNo.", 0x7A: "MissingNo.", 0x7B: "Caterpie", 0x7C: "Metapod",
    0x7D: "Butterfree", 0x7E: "Machamp", 0x7F: "MissingNo.", 0x80: "Golduck",
    0x81: "Hypno", 0x82: "Golbat", 0x83: "Mewtwo", 0x84: "Snorlax",
    0x85: "Magikarp", 0x86: "MissingNo.", 0x87: "MissingNo.", 0x88: "Muk",
    0x89: "MissingNo.", 0x8A: "Kingler", 0x8B: "Cloyster", 0x8C: "MissingNo.",
    0x8D: "Electrode", 0x8E: "Clefable", 0x8F: "Weezing", 0x90: "Persian",
    0x91: "Marowak", 0x92: "MissingNo.", 0x93: "Haunter", 0x94: "Abra",
    0x95: "Alakazam", 0x96: "Pidgeotto", 0x97: "Pidgeot", 0x98: "Starmie",
    0x99: "Bulbasaur", 0x9A: "Venusaur", 0x9B: "Tentacruel", 0x9C: "MissingNo.",
    0x9D: "Goldeen", 0x9E: "Seaking", 0x9F: "MissingNo.", 0xA0: "MissingNo.",
    0xA1: "MissingNo.", 0xA2: "MissingNo.", 0xA3: "Ponyta", 0xA4: "Rapidash",
    0xA5: "Rattata", 0xA6: "Raticate", 0xA7: "Nidorino", 0xA8: "Nidorina",
    0xA9: "Geodude", 0xAA: "Porygon", 0xAB: "Aerodactyl", 0xAC: "MissingNo.",
    0xAD: "Magnemite", 0xAE: "MissingNo.", 0xAF: "MissingNo.", 0xB0: "Charmander",
    0xB1: "Squirtle", 0xB2: "Charmeleon", 0xB3: "Wartortle", 0xB4: "Charizard",
    0xB5: "MissingNo.", 0xB6: "MissingNo.", 0xB7: "MissingNo.", 0xB8: "MissingNo.",
    0xB9: "Oddish", 0xBA: "Gloom", 0xBB: "Vileplume", 0xBC: "Bellsprout",
    0xBD: "Weepinbell", 0xBE: "Victreebel",
}

# ---------- Item ID to Name (Gen I) ----------
ITEM_NAMES = {
    0x01: "Master Ball", 0x02: "Ultra Ball", 0x03: "Great Ball", 0x04: "Poké Ball",
    0x05: "Town Map", 0x06: "Bicycle", 0x07: "S.S. Ticket", 0x08: "Escape Rope",
    0x09: "Repel", 0x0A: "Moon Stone", 0x0B: "Antidote", 0x0C: "Burn Heal",
    0x0D: "Ice Heal", 0x0E: "Awakening", 0x0F: "Parlyz Heal", 0x10: "Full Restore",
    0x11: "Max Potion", 0x12: "Hyper Potion", 0x13: "Super Potion", 0x14: "Potion",
    0x15: "BoulderBadge", 0x16: "CascadeBadge", 0x17: "ThunderBadge", 0x18: "RainbowBadge",
    0x19: "SoulBadge", 0x1A: "MarshBadge", 0x1B: "VolcanoBadge", 0x1C: "EarthBadge",
    0x1D: "Old Rod", 0x1E: "Good Rod", 0x1F: "Super Rod", 0x20: "Coin",
    0x21: "Fresh Water", 0x22: "Soda Pop", 0x23: "Lemonade", 0x24: "Rage Candy Bar",
    0x25: "PP Up", 0x26: "Dire Hit", 0x27: "Guard Spec.", 0x28: "X Attack",
    0x29: "X Defend", 0x2A: "X Speed", 0x2B: "X Special", 0x2C: "HP Up",
    0x2D: "Protein", 0x2E: "Iron", 0x2F: "Carbos", 0x30: "Calcium",
    0x31: "Nugget", 0x32: "Rare Candy", 0x33: "TM01", 0x34: "TM02",
    0x35: "TM03", 0x36: "TM04", 0x37: "TM05", 0x38: "TM06",
    0x39: "TM07", 0x3A: "TM08", 0x3B: "TM09", 0x3C: "TM10",
    0x3D: "TM11", 0x3E: "TM12", 0x3F: "TM13", 0x40: "TM14",
    0x41: "TM15", 0x42: "TM16", 0x43: "TM17", 0x44: "TM18",
    0x45: "TM19", 0x46: "TM20", 0x47: "TM21", 0x48: "TM22",
    0x49: "TM23", 0x4A: "TM24", 0x4B: "TM25", 0x4C: "TM26",
    0x4D: "TM27", 0x4E: "TM28", 0x4F: "TM29", 0x50: "TM30",
    0x51: "TM31", 0x52: "TM32", 0x53: "TM33", 0x54: "TM34",
    0x55: "TM35", 0x56: "TM36", 0x57: "TM37", 0x58: "TM38",
    0x59: "TM39", 0x5A: "TM40", 0x5B: "TM41", 0x5C: "TM42",
    0x5D: "TM43", 0x5E: "TM44", 0x5F: "TM45", 0x60: "TM46",
    0x61: "TM47", 0x62: "TM48", 0x63: "TM49", 0x64: "TM50",
    0x65: "HM01", 0x66: "HM02", 0x67: "HM03", 0x68: "HM04",
    0x69: "HM05", 0x6A: "Old Amber", 0x6B: "Dome Fossil", 0x6C: "Helix Fossil",
    0x6D: "Secret Key", 0x6E: "Itemfinder", 0x6F: "Poké Flute", 0x70: "Exp. Share",
    0x71: "Card Key", 0x72: "S.S. Ticket", 0x73: "Gold Teeth"
}

def decode_text(data):
    """Decode Gen I text bytes until terminator 0x50."""
    result = []
    for b in data:
        if b == 0x50:
            break
        result.append(CHAR_MAP.get(b, '?'))
    return ''.join(result)

def is_valid_gen1_text(data):
    """Return True if bytes look like a Gen I text field (0x50-terminated)."""
    if not data:
        return False
    valid = set(CHAR_MAP.keys()) - {0x50}
    saw_terminator = False
    for b in data:
        if b == 0x50:
            saw_terminator = True
            break
        if b not in valid:
            return False
    return saw_terminator


def calc_main_checksum(data):
    """Gen I main-data checksum: bitwise NOT of the 8-bit sum."""
    total = sum(data[OFFSETS["CHECKSUM_START"]:OFFSETS["CHECKSUM_END"]]) & 0xFF
    return (~total) & 0xFF


def score_save_layout(data):
    """Heuristic score for whether data is a valid Gen I international save."""
    if len(data) < OFFSETS["MAIN_CHECKSUM"] + 1:
        return 0

    score = 0
    name_bytes = data[OFFSETS["PLAYER_NAME"]:OFFSETS["PLAYER_NAME"] + 11]
    if is_valid_gen1_text(name_bytes):
        name = decode_text(name_bytes)
        if 1 <= len(name) <= 10:
            score += 10

    if data[OFFSETS["MAIN_CHECKSUM"]] == calc_main_checksum(data):
        score += 20

    party_count = data[OFFSETS["PARTY"]]
    if 0 <= party_count <= 6:
        score += 5
        party_start = OFFSETS["PARTY"] + 8
        for i in range(party_count):
            mon_offset = party_start + i * 44
            if mon_offset + 0x22 > len(data):
                break
            species_id = data[mon_offset]
            level = data[mon_offset + 0x21]
            if species_id == 0 or level == 0 or level > 100:
                break
        else:
            score += 5

    return score


def normalize_save(raw_data):
    """
    Normalize emulator save files to a standard 32 KiB SRAM layout.

    Handles:
    - Standard 32 KiB dumps (BGB, SameBoy, RetroArch, etc.)
    - Larger files with mGBA/RTC footers (uses first 32 KiB)
    - 64 KiB padded dumps (picks the valid half)
    - 8 KiB bank-1-only dumps (prepends empty bank 0)
    """
    if not raw_data:
        raise ValueError("Save file is empty.")

    candidates = []

    if len(raw_data) >= SRAM_SIZE:
        candidates.append(raw_data[:SRAM_SIZE])
        if len(raw_data) >= 2 * SRAM_SIZE:
            candidates.append(raw_data[SRAM_SIZE:2 * SRAM_SIZE])

    if len(raw_data) == BANK_SIZE:
        padded = b"\x00" * BANK_SIZE + raw_data + b"\x00" * (SRAM_SIZE - 2 * BANK_SIZE)
        candidates.append(padded)

    if len(raw_data) < SRAM_SIZE and len(raw_data) != BANK_SIZE:
        candidates.append(raw_data.ljust(SRAM_SIZE, b"\x00"))

    if not candidates:
        raise ValueError(f"Unsupported save file size: {len(raw_data)} bytes.")

    best = max(candidates, key=score_save_layout)
    if score_save_layout(best) == 0:
        # Fall back to the most common layout so partially corrupt saves still load.
        if len(raw_data) >= SRAM_SIZE:
            best = raw_data[:SRAM_SIZE]
        elif len(raw_data) == BANK_SIZE:
            best = b"\x00" * BANK_SIZE + raw_data + b"\x00" * (SRAM_SIZE - 2 * BANK_SIZE)
        else:
            best = raw_data.ljust(SRAM_SIZE, b"\x00")

    return best


def parse_item_list(data, start, capacity):
    """Parse a Gen I item list of [id, qty] pairs terminated by 0xFF."""
    items = []
    for i in range(capacity):
        offset = start + i * 2
        item_id = data[offset]
        quantity = data[offset + 1]
        if item_id == 0xFF or item_id == 0 or quantity == 0:
            break
        item_name = ITEM_NAMES.get(item_id, f"Unknown ({item_id})")
        items.append({
            "item_id": item_id,
            "item_name": item_name,
            "quantity": quantity,
        })
    return items

    """Decode Gen I text bytes until terminator 0x50."""
    result = []
    for b in data:
        if b == 0x50:
            break
        result.append(CHAR_MAP.get(b, '?'))
    return ''.join(result)

def bcd_to_int(bcd_bytes):
    """Convert 3‑byte BCD (big‑endian) to integer."""
    value = 0
    for byte in bcd_bytes:
        value = value * 100 + ((byte >> 4) * 10 + (byte & 0x0F))
    return value

def get_badges(badge_byte):
    """Return list of badge names obtained."""
    badge_names = [
        "Boulder", "Cascade", "Thunder", "Rainbow",
        "Soul", "Marsh", "Volcano", "Earth"
    ]
    return [name for i, name in enumerate(badge_names) if (badge_byte >> i) & 1]

class SaveFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_size = 0
        self.data = None
        self.load()
        self.parse()

    def load(self):
        with open(self.filepath, 'rb') as f:
            raw = f.read()
        self.raw_size = len(raw)
        self.data = normalize_save(raw)

    def parse(self):
        # Player name
        self.player_name = decode_text(
            self.data[OFFSETS["PLAYER_NAME"]:OFFSETS["PLAYER_NAME"] + 11]
        )

        # Rival name
        self.rival_name = decode_text(
            self.data[OFFSETS["RIVAL_NAME"]:OFFSETS["RIVAL_NAME"] + 11]
        )

        # Money
        money_bytes = self.data[OFFSETS["MONEY"]:OFFSETS["MONEY"] + 3]
        self.money = bcd_to_int(money_bytes)

        # Badges (bit 0 = Boulder, bit 7 = Earth per pokered)
        badge_byte = self.data[OFFSETS["BADGES"]]
        self.badges = get_badges(badge_byte)

        # Party Pokémon
        party_count = self.data[OFFSETS["PARTY"]]
        party_start = OFFSETS["PARTY"] + 8
        self.party = []
        for i in range(party_count):
            offset = party_start + i * 44
            species_id = self.data[offset]
            level = self.data[offset + 0x21]
            species_name = SPECIES_NAMES.get(species_id, f"Unknown ({species_id})")
            self.party.append({
                'species_id': species_id,
                'species_name': species_name,
                'level': level
            })

        # Bag items
        self.bag_items = parse_item_list(self.data, OFFSETS["BAG_ITEMS"], 20)

        # PC items
        self.pc_items = parse_item_list(self.data, OFFSETS["PC_ITEMS"], 50)

    def show_player(self):
        print(f"Player: {self.player_name}")

    def show_rival(self):
        print(f"Rival: {self.rival_name}")

    def show_money(self):
        print(f"Money: {self.money} ₽")

    def show_badges(self):
        if self.badges:
            print(f"Badges: {', '.join(self.badges)}")
        else:
            print("Badges: None")

    def show_party(self):
        print(f"Party ({len(self.party)} Pokémon):")
        for i, p in enumerate(self.party):
            print(f"  {i+1}. {p['species_name']} (Level {p['level']})")

    def show_bag(self):
        print(f"Bag items ({len(self.bag_items)} slots):")
        for item in self.bag_items:
            print(f"  {item['item_name']} x{item['quantity']}")

    def show_pc(self):
        print(f"PC items ({len(self.pc_items)} slots):")
        for item in self.pc_items:
            print(f"  {item['item_name']} x{item['quantity']}")

def main():
    parser = argparse.ArgumentParser(
        description="Consult a Pokémon Generation I (Red/Blue) save file."
    )
    parser.add_argument(
        "save_file",
        nargs="?",
        default=SAVE_FILE_PATH,
        help="Path to a .sav file (default: examples/sample.sav)",
    )
    args = parser.parse_args()

    try:
        save = SaveFile(args.save_file)
    except (OSError, ValueError) as exc:
        print(f"Error loading save file: {exc}", file=sys.stderr)
        sys.exit(1)

    if save.raw_size != SRAM_SIZE:
        print(
            f"Loaded {args.save_file} ({save.raw_size} bytes) "
            f"— normalized to standard 32 KiB layout."
        )

    while True:
        print("\n" + "="*40)
        print("CONSULT SAVE FILE")
        print("="*40)
        print("1. Player")
        print("2. Rival")
        print("3. Money")
        print("4. Badges")
        print("5. Party Pokémon")
        print("6. Bag items")
        print("7. PC items")
        print("8. Exit")
        print("-"*40)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            save.show_player()
        elif choice == '2':
            save.show_rival()
        elif choice == '3':
            save.show_money()
        elif choice == '4':
            save.show_badges()
        elif choice == '5':
            save.show_party()
        elif choice == '6':
            save.show_bag()
        elif choice == '7':
            save.show_pc()
        elif choice == '8':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()
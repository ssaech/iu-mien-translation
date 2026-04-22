import re
from dataclasses import dataclass
from typing import List, Dict

TONE_SUFFIXES = {"v", "h", "c", "x", "z"}

TONE_MAP = {
    "": "T0",
    "v": "TV",
    "h": "TH",
    "c": "TC",
    "x": "TX",
    "z": "TZ",
}

# Longest match first
ONSETS_V1 = sorted([
    "hny", "hng", "hm", "hn", "ny", "ng", "mb", "nd", "nq", "nz", "nj", "hl",
    "p", "b", "m", "t", "d", "n", "k", "g", "c", "z", "q", "j", "f", "s", "h", "y", "w", "l"
], key=len, reverse=True)

PHONEME_V1 = {
  "ON_M": 1,
  "ON_NG": 2,
  "FI_AAI": 100,
  "FI_IE": 101,
  "CODA_Q": 300,
  "T0": 400,
  "TV": 401,
  "TH": 402,
  "TC": 403,
  "TX": 404,
  "TZ": 405,
  "SYL_M": 500,
  "SYL_HM": 501
}

# Use stable IMUS-derived symbols first:
# ON_* for onsets
# FI_* for finals
# CODA_Q for syllable-final q
# T0/TV/TH/TC/TX/TZ for tones
# SYL_* for the small exception class

# remove loan words like Hello from TTS and STT

@dataclass
class ParsedSyllable:
    surface: str
    onset: str
    final: str
    has_final_q: bool
    tone_surface: str
    tone_symbol: str

    def symbol_sequence(self) -> List[str]:
        out = []
        if self.onset:
            out.append(f"ON_{self.onset.upper()}")
        out.append(f"FI_{self.final.upper()}")
        if self.has_final_q:
            out.append("CODA_Q")
        out.append(self.tone_symbol)
        return out


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("’", "'").replace("`", "'")
    text = re.sub(r"[^a-z'\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_into_syllable_like_units(text: str) -> List[str]:
    """
    Hyphen and apostrophe are treated as boundaries, not phoneme symbols.
    """
    text = normalize_text(text)
    parts = []
    for word in text.split():
        for piece in word.split("-"):
            for syl in piece.split("'"):
                syl = syl.strip()
                if syl:
                    parts.append(syl)
    return parts


def strip_tone(s: str):
    if s and s[-1] in TONE_SUFFIXES:
        return s[:-1], s[-1]
    return s, ""


def strip_final_q(s: str):
    if s.endswith("q"):
        return s[:-1], True
    return s, False


def detect_onset(core: str):
    for onset in ONSETS_V1:
        if core.startswith(onset):
            return onset, core[len(onset):]
    return "", core  # null onset allowed


def parse_syllable(s: str, finals_inventory: set[str]) -> ParsedSyllable:
    original = s
    core, tone_surface = strip_tone(s)
    core, has_final_q = strip_final_q(core)
    onset, final = detect_onset(core)

    if not final:
        raise ValueError(f"Missing final after onset parse: {original}")

    if final not in finals_inventory:
        raise ValueError(
            f"Unknown final '{final}' in syllable '{original}'. "
            f"Add it to FINALS_V1 after validation."
        )

    return ParsedSyllable(
        surface=original,
        onset=onset,
        final=final,
        has_final_q=has_final_q,
        tone_surface=tone_surface,
        tone_symbol=TONE_MAP[tone_surface],
    )
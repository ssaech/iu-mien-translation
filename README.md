# Iu Mien Translation

## Goal

This project starts with a **1,000-word English seed list**, but treats it as a **seed lexicon**, not the final dataset.

The long-term goal is to support:
- English ↔ Iu Mien dictionary lookup
- text → text translation
- speech → text transcription
- speech → translated text


## Why this project needs its own data

Iu Mien (ISO 639-3: `ium`; Glottolog: `iumi1238`) is a recognized language and appears in broader multilingual NLP and speech tooling. However, support is still mostly broad multilingual coverage rather than a mature Iu-Mien-first ecosystem. Because of that, the quality of this project will depend heavily on building clean bilingual concepts, sentence pairs, and transcript-aligned audio.

## Core Idea

The 1,000 words should not stay as flat pairs like:
```txt
say = gorngv
eat = nyanc
water = ...
```

They should become the foundation for:
- concepts
- sentence pairs
- transcript-aligned audio clips
- evaluation sets

## Data Files

Main files:
- `concepts.jsonl`
- `sentencePairs.jsonl`
- `audioClips.jsonl`

IDs:
- `CON_1`, `CON_2`
- `PAIR_1`, `PAIR_2`
- `CLIP_1`, `CLIP_2`

## Concepts

One row per concept
```json
{
  "conceptId": "CON_1",
  "engLemma": "say",
  "engPos": "verb",
  "engGloss": "to speak words; to tell someone something",
  "iumLemma": "gorngv",
  "iumVariants": [],
  "status": "gold",
  "notes": ""
}
```

This supports:
- English → Iu Mien lookup
- Iu Mien → English lookup
- later sentence and audio linking

## Sentence Pairs

One bilingual pair per row
```json
{
  "pairId": "PAIR_1",
  "engText": "Please say it again.",
  "iumText": "",
  "domain": "conversation",
  "conceptIds": ["CON_1"],
  "status": "draft",
  "notes": "Needs translation."
}
```

Later
```json
{
  "pairId": "PAIR_1",
  "engText": "Please say it again.",
  "iumText": "...",
  "domain": "conversation",
  "conceptIds": ["CON_1"],
  "status": "gold",
  "notes": ""
}
```

Sentence pairs are more valuable for translation than isolated word pairs.

## Audio Clips

Store audio with exact transcripts.
```json
{
  "clipId": "CLIP_1",
  "transcript": "gorngv",
  "normalizedTranscript": "gorngv",
  "audioPath": "audio/ium/CLIP_1.wav"
}
```

This is enough for:
- pronunciation playback
- transcript-aligned storage
- early ASR experiments

## How to Use the 1,000 Words

Split them into three buckets:

### Core concepts
About 300 to 500 words.

These should get:
- concept entries
- 3 to 5 sentence pairs each
- audio clips later

### Secondary vocabulary
About 300 to 400 words.

These should get:
- concept entries
- sentence pairs later if needed

### Long-tail vocabulary
The rest.

These can remain concept-only for now.

## Roadmap

### Phase 1: Build the dictionary MVP
- convert the 1,000 words into `concepts.jsonl`
- support English ↔ Iu Mien lookup

### Phase 2: Expand the top 300 to 500 concepts into sentence pairs
Priority domains:
- greetings
- family
- food
- doctor / clinic
- school
- work
- shopping
- directions
- emergencies
- common conversation

### Phase 3: Create held-out evaluation data
- hold out around 100 concepts
- hold out around 100 sentence pairs

### Phase 4: Collect audio tied to transcripts
- record isolated words
- record short phrases
- record full sentences

### Phase 5: Build the speech pipeline
- spoken English → English ASR → Iu Mien text
- spoken Iu Mien → Iu Mien ASR → English text
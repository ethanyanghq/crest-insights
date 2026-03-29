#!/usr/bin/env python3
"""
Convert sentinel_master.md to MP3 via ElevenLabs TTS.
Optimizes the markdown for spoken audio before sending.
"""

import os
import re
import struct
import sys
import time
import urllib.request
import json

API_KEY = os.environ.get("ELEVEN_LABS", "").strip()
if not API_KEY:
    print("ERROR: ELEVEN_LABS env var not set")
    sys.exit(1)

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel — clear, neutral, good for long-form
MODEL_ID = "eleven_turbo_v2_5"       # Fast + high quality
OUTPUT_FILE = "sentinel_master.mp3"
CHUNK_SIZE = 4500  # chars per API call (safe limit)


# ── 1. Read source ────────────────────────────────────────────────────────────
with open("sentinel_master.md", "r") as f:
    raw = f.read()


# ── 2. Convert markdown → spoken text ────────────────────────────────────────
def md_to_speech(text: str) -> str:
    # Remove strikethrough
    text = re.sub(r"~~(.+?)~~", "", text)

    # Convert headers to spoken section titles
    text = re.sub(r"^#{1,6}\s+(.*)", r"\1.", text, flags=re.MULTILINE)

    # Remove bold/italic markers
    text = re.sub(r"\*{1,3}(.+?)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", text)

    # Remove inline code backticks
    text = re.sub(r"`(.+?)`", r"\1", text)

    # Remove fenced code blocks entirely (replace with a brief note)
    text = re.sub(r"```[\s\S]*?```", "[technical code block omitted for audio]", text)

    # Convert blockquotes — remove the ">" marker
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)

    # Convert markdown tables to readable prose
    def table_to_prose(match):
        lines = match.group(0).strip().splitlines()
        # Drop separator row (---|---|---)
        data_lines = [l for l in lines if not re.match(r"^\s*[\|\-\s]+$", l)]
        result_parts = []
        for line in data_lines:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells = [c for c in cells if c]
            if cells:
                result_parts.append(", ".join(cells) + ".")
        return "\n".join(result_parts)

    text = re.sub(r"(\|.+\n)+", table_to_prose, text)

    # Remove horizontal rules
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)

    # Convert list bullets to natural sentences
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)

    # Remove links but keep text: [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

    # Remove leftover special chars
    text = re.sub(r"[⭐★]", "", text)

    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Clean up lines that are just punctuation
    text = re.sub(r"^\s*[,\.;:]+\s*$", "", text, flags=re.MULTILINE)

    return text.strip()


clean_text = md_to_speech(raw)

# Save the TTS-optimized text for reference
with open("sentinel_master_tts.txt", "w") as f:
    f.write(clean_text)
print(f"TTS text saved ({len(clean_text):,} chars) → sentinel_master_tts.txt")


# ── 3. Split into chunks at sentence/paragraph boundaries ────────────────────
def split_into_chunks(text: str, max_chars: int) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= max_chars:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            # Para itself might be too long — split at sentence boundaries
            if len(para) > max_chars:
                sentences = re.split(r"(?<=[.!?])\s+", para)
                current = ""
                for sent in sentences:
                    if len(current) + len(sent) + 1 <= max_chars:
                        current = (current + " " + sent).strip()
                    else:
                        if current:
                            chunks.append(current)
                        current = sent
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks


chunks = split_into_chunks(clean_text, CHUNK_SIZE)
print(f"Split into {len(chunks)} chunks")


# ── 4. Call ElevenLabs for each chunk ────────────────────────────────────────
def tts_chunk(text: str, chunk_idx: int) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "speed": 1.1,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    print(f"  Chunk {chunk_idx+1}/{len(chunks)} ({len(text):,} chars)...", end=" ", flush=True)
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    print(f"OK ({len(data):,} bytes)")
    return data


audio_parts = []
for i, chunk in enumerate(chunks):
    audio_parts.append(tts_chunk(chunk, i))
    if i < len(chunks) - 1:
        time.sleep(0.3)  # be gentle with the API


# ── 5. Concatenate MP3 frames ─────────────────────────────────────────────────
# Simple concatenation works for MP3 files with the same bitrate/sample rate
combined = b"".join(audio_parts)
with open(OUTPUT_FILE, "wb") as f:
    f.write(combined)

size_mb = len(combined) / (1024 * 1024)
print(f"\nDone! {OUTPUT_FILE} ({size_mb:.1f} MB)")

#!/usr/bin/env python3
"""
Convert sentinel_master.md to a WAV file via ElevenLabs TTS.

Requests raw PCM audio (pcm_22050) per chunk — raw samples concatenate
perfectly, no ID3 headers to confuse players. Each chunk is saved to disk
immediately so a mid-run failure can be resumed without re-spending credits.
"""

import os
import re
import struct
import sys
import time
import urllib.request
import urllib.error
import json

API_KEY = os.environ.get("ELEVEN_LABS", "").strip()
if not API_KEY:
    print("ERROR: ELEVEN_LABS env var not set")
    sys.exit(1)

VOICE_ID  = "21m00Tcm4TlvDq8ikWAM"  # Rachel — clear, neutral, good for long-form
MODEL_ID  = "eleven_turbo_v2_5"
OUTPUT_FORMAT = "pcm_22050"          # raw signed 16-bit LE PCM, 22050 Hz, mono
SAMPLE_RATE   = 22050
CHANNELS      = 1
SAMPLE_WIDTH  = 2                    # bytes (16-bit)
OUTPUT_FILE   = "sentinel_master.wav"
CHUNK_DIR     = "sentinel_audio_chunks"
CHUNK_SIZE    = 4500                 # chars per API call


# ── 1. Read pre-cleaned TTS text directly ────────────────────────────────────
with open("sentinel_master_tts.txt", "r") as f:
    clean_text = f.read()

print(f"TTS text ready ({len(clean_text):,} chars)")


# ── 3. Split into chunks ──────────────────────────────────────────────────────
def split_into_chunks(text: str, max_chars: int) -> list[str]:
    paragraphs = text.split("\n\n")
    chunks, current = [], ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 <= max_chars:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
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

os.makedirs(CHUNK_DIR, exist_ok=True)


# ── 4. Fetch each chunk (skip already-saved ones for resume safety) ───────────
def fetch_chunk(text: str, idx: int) -> str:
    path = os.path.join(CHUNK_DIR, f"chunk_{idx:03d}.pcm")
    if os.path.exists(path):
        print(f"  Chunk {idx+1}/{len(chunks)} — already on disk, skipping")
        return path

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        f"?output_format={OUTPUT_FORMAT}"
    )
    payload = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    print(f"  Chunk {idx+1}/{len(chunks)} ({len(text):,} chars)...", end=" ", flush=True)
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"FAILED — HTTP {e.code}: {body}")
        sys.exit(1)

    with open(path, "wb") as f:
        f.write(data)
    print(f"OK ({len(data):,} bytes → {path})")
    return path


chunk_paths = []
for i, chunk in enumerate(chunks):
    chunk_paths.append(fetch_chunk(chunk, i))
    if i < len(chunks) - 1:
        time.sleep(0.3)


# ── 5. Concatenate PCM files + write WAV header ───────────────────────────────
print("\nAssembling WAV...")
pcm_parts = []
for path in chunk_paths:
    with open(path, "rb") as f:
        pcm_parts.append(f.read())

raw_pcm   = b"".join(pcm_parts)
data_size = len(raw_pcm)
byte_rate = SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH
block_align = CHANNELS * SAMPLE_WIDTH

header = struct.pack(
    "<4sI4s4sIHHIIHH4sI",
    b"RIFF",
    36 + data_size,
    b"WAVE",
    b"fmt ",
    16,
    1,                   # PCM
    CHANNELS,
    SAMPLE_RATE,
    byte_rate,
    block_align,
    SAMPLE_WIDTH * 8,    # bits per sample
    b"data",
    data_size,
)

with open(OUTPUT_FILE, "wb") as f:
    f.write(header + raw_pcm)

size_mb      = (44 + data_size) / (1024 * 1024)
duration_min = (data_size / (byte_rate)) / 60
print(f"Done! {OUTPUT_FILE} ({size_mb:.1f} MB, ~{duration_min:.1f} min)")
print(f"Chunk files kept in {CHUNK_DIR}/ — delete them when satisfied with the output.")

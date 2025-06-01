import json
import os
import sys
import argparse
import re
from datetime import datetime

# Regex to match <v Speaker>text</v> format
VTT_LINE_REGEX = re.compile(r"<v\s+(.+?)>(.+?)</v>", re.DOTALL)

def sanitize_filename(filename):
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    sanitized = sanitized.strip().strip('.')
    return sanitized or "transcript"

def get_args():
    parser = argparse.ArgumentParser(description="Transcript Parser Tool")
    parser.add_argument("file", nargs="?", help="Input transcript file")
    parser.add_argument("-f", "--format", choices=["json", "txt"], default="txt", 
                        help="Output format (default: txt)")
    return parser.parse_args()

def main():
    args = get_args()
    interactive_mode = args.file is None

    if interactive_mode:
        print("Transcript Parser Tool")
        print("=====================\n")

    file_path = args.file or input("Please enter the name of the transcript file to parse: ")
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    output_format = args.format.lower()
    assert output_format in ["json", "txt"], f"Unexpected output format: {output_format}"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_lines = [line.strip().lstrip('\ufeff') for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Remove WEBVTT header if present
    if raw_lines and raw_lines[0].lower() == "webvtt":
        raw_lines = raw_lines[1:]

    # Parse raw_lines into blocks: (block_id, timestamp, full_text)
    blocks = []
    i = 0
    while i < len(raw_lines) - 1:
        if "-->" in raw_lines[i + 1]:
            block_id = raw_lines[i]
            timestamp = raw_lines[i + 1]
            text_lines = []
            i += 2
            while i < len(raw_lines) and "-->" not in raw_lines[i]:
                text_lines.append(raw_lines[i])
                i += 1
            full_text = " ".join(text_lines).strip()
            blocks.append((block_id, timestamp, full_text))
        else:
            i += 1  # Skip lines that don't match expected block format

    structured_transcript = []

    for idx, (block_id, timestamp, raw_text) in enumerate(blocks):
        try:
            if "-->" not in timestamp:
                raise ValueError(f"Invalid timestamp format -> '{timestamp}'")
            start, end = [t.strip() for t in timestamp.split("-->")]

            match = VTT_LINE_REGEX.match(raw_text)
            if match:
                speaker = match.group(1).strip()
                text = match.group(2).strip()
            else:
                speaker = "Unknown"
                text = raw_text.strip()

            structured_transcript.append({
                "speaker": speaker,
                "start": start,
                "end": end,
                "text": text
            })
        except ValueError as e:
            print(f"⚠️ Skipping block #{idx+1}: {e}")
        except Exception as e:
            print(f"⚠️ Error processing block #{idx+1}: {e}")


    # Merge consecutive blocks by the same speaker
    merged_transcript = []

    for entry in structured_transcript:
        if not merged_transcript:
            merged_transcript.append(entry)
        else:
            last = merged_transcript[-1]
            if entry["speaker"] == last["speaker"]:
                # Merge with last
                last["end"] = entry["end"]
                last["text"] += " " + entry["text"]
            else:
                # New speaker, start new block
                merged_transcript.append(entry)

    # Generate output filename
    base_name = sanitize_filename(os.path.splitext(os.path.basename(file_path))[0])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{base_name}_parsed_{timestamp}.{output_format}"

    # Save output
    try:
        if output_format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_transcript, f, indent=2, ensure_ascii=False)
        elif output_format == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                for entry in merged_transcript:
                    f.write(f"Speaker: {entry['speaker']}\n")
                    f.write(f"Time: {entry['start']} --> {entry['end']}\n")
                    f.write(f"Text: {entry['text']}\n")
                    f.write("\n\n")

        print(f"\nProcessing complete!")
        print(f"Processed {len(structured_transcript)} transcript entries.")
        print(f"Output saved to: {output_file}")

    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

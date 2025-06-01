# Transcript Parser

A command-line tool to parse and clean WebVTT transcripts, merge continuous speaker blocks, and export them into readable `.txt` or structured `.json` format.

## Features

- Parses transcripts formatted in WebVTT (3-line blocks)
- Extracts speaker name, timestamps, and text
- Handles multiline text and malformed speaker tags
- Merges consecutive utterances from the same speaker
- Outputs to TXT or JSON format with clean formatting
- CLI interface with interactive or scriptable usage

## Installation

Clone the repository:

    git clone https://github.com/PetroczyP/transcript_parser.git
    cd transcript_parser

Install locally in editable mode:

    pip install -e .

This will make the `transcript-parser` command available globally in your terminal.

## Usage

You can run the parser in two ways:

### 1. CLI with arguments

    transcript-parser path/to/your.vtt -f txt

### 2. Interactive mode (no arguments)

    transcript-parser

You’ll be prompted to enter the file name and choose the format (`json` or `txt`).

## Example Output

    Speaker: User_Full_Name_1
    Time: 00:00:12.261 --> 00:00:12.581
    Text: Hello.


    Speaker: User_Full_Name_2
    Time: 00:00:59.521 --> 00:01:01.161
    Text: Hi, Bianca. Hey there.

## License

MIT License – see the `LICENSE` file for details.

## Contact

For questions, suggestions, or issues, please open a GitHub Issue at:

https://github.com/PetroczyP/transcript_parser/issues
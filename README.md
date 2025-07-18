# ASS to SRT Converter

A Python utility to convert ASS (Advanced SubStation Alpha) subtitle files to SRT (SubRip Text) format.

## Features

- Batch conversion of ASS files to SRT format
- Preserves subtitle timing and text content
- Automatic input/output folder processing
- Clean, readable SRT output

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ass_to_srt
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your ASS files in the `input` folder
2. Run the converter:
```bash
python convert.py
```
3. Find your converted SRT files in the `output` folder

## Project Structure

```
ass_to_srt/
├── input/          # Place ASS files here
├── output/         # SRT files will be generated here
├── convert.py      # Main conversion script
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.6+
- pysubs2 (for subtitle parsing and conversion)

## License

MIT License 
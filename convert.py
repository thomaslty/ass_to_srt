#!/usr/bin/env python3
"""
ASS to SRT Converter

This script converts ASS (Advanced SubStation Alpha) subtitle files to SRT (SubRip Text) format.
It reads all ASS files from the 'input' folder and saves the converted SRT files to the 'output' folder.
"""

import os
import sys
from pathlib import Path
import chardet

try:
    import pysubs2
except ImportError:
    print("Error: pysubs2 library not found.")
    print("Please install it using: pip install pysubs2")
    sys.exit(1)


def create_directories():
    """Create input and output directories if they don't exist."""
    input_dir = Path("input")
    output_dir = Path("output")
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    return input_dir, output_dir


def detect_encoding(file_path):
    """
    Detect the encoding of a file using chardet library.
    
    Args:
        file_path (Path): Path to the file
        
    Returns:
        str: Detected encoding
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    except Exception:
        return None


def convert_ass_to_srt(ass_file_path, srt_file_path):
    """
    Convert a single ASS file to SRT format with encoding detection.
    
    Args:
        ass_file_path (Path): Path to the input ASS file
        srt_file_path (Path): Path to the output SRT file
    """
    # List of encodings to try, in order of preference
    encodings_to_try = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'gbk', 'big5', 'shift_jis', 'cp1252']
    
    # First, try to detect encoding using chardet
    detected_encoding = detect_encoding(ass_file_path)
    if detected_encoding:
        encodings_to_try.insert(0, detected_encoding)
    
    for encoding in encodings_to_try:
        try:
            # Try loading with the current encoding
            subs = pysubs2.load(str(ass_file_path), encoding=encoding)
            
            # Save as SRT
            subs.save(str(srt_file_path))
            
            print(f"✓ Converted: {ass_file_path.name} → {srt_file_path.name} (encoding: {encoding})")
            return True
            
        except (UnicodeDecodeError, UnicodeError):
            # This encoding didn't work, try the next one
            continue
        except Exception as e:
            # For other errors, continue trying other encodings
            if "codec can't decode" in str(e).lower():
                continue
            else:
                # If it's not an encoding error, report it and stop trying
                print(f"✗ Error converting {ass_file_path.name}: {str(e)}")
                return False
    
    # If we get here, none of the encodings worked
    print(f"✗ Error converting {ass_file_path.name}: Could not detect or decode file encoding")
    return False


def main():
    """Main function to process all ASS files in the input directory."""
    print("ASS to SRT Converter")
    print("=" * 40)
    
    # Create directories
    input_dir, output_dir = create_directories()
    
    # Find all ASS files in the input directory
    ass_files = list(input_dir.glob("*.ass"))
    
    if not ass_files:
        print(f"No ASS files found in '{input_dir}' directory.")
        print(f"Please place your ASS files in the '{input_dir}' folder and run again.")
        return
    
    print(f"Found {len(ass_files)} ASS file(s) to convert:")
    
    converted_count = 0
    failed_count = 0
    
    for ass_file in ass_files:
        # Create corresponding SRT filename
        srt_file = output_dir / (ass_file.stem + ".srt")
        
        # Convert the file
        if convert_ass_to_srt(ass_file, srt_file):
            converted_count += 1
        else:
            failed_count += 1
    
    print("\n" + "=" * 40)
    print(f"Conversion completed!")
    print(f"Successfully converted: {converted_count} file(s)")
    if failed_count > 0:
        print(f"Failed to convert: {failed_count} file(s)")
    print(f"Output files saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main() 
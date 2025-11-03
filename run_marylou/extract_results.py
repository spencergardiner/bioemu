#!/usr/bin/env python3
"""
Prepare BioEmu ensemble results for analysis.

For each subdirectory in the input path, this script creates a sister directory
named <sub_dir_name>_final_results and copies the essential files:
- topology.pdb
- samples.xtc
- sequence.fasta

Usage:
    python prepare_ensemble_results.py /path/to/ensembles

Example:
    python prepare_ensemble_results.py ./bioemu_runs
    
    This will process:
        ./bioemu_runs/run_1/ -> ./bioemu_runs/run_1_final_results/
        ./bioemu_runs/run_2/ -> ./bioemu_runs/run_2_final_results/
        etc.
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List


def copy_ensemble_files(source_dir: Path, dest_dir: Path, required_files: List[str]) -> dict:
    """
    Copy required files from source to destination directory.
    
    Args:
        source_dir: Source directory containing the files
        dest_dir: Destination directory to copy files to
        required_files: List of filenames to copy
    
    Returns:
        Dictionary with status information
    """
    results = {
        'copied': [],
        'missing': [],
        'errors': []
    }
    
    for filename in required_files:
        source_file = source_dir / filename
        dest_file = dest_dir / filename
        
        if source_file.exists():
            try:
                shutil.copy2(source_file, dest_file)
                results['copied'].append(filename)
                print(f"    ✓ Copied: {filename}")
            except Exception as e:
                results['errors'].append(f"{filename}: {str(e)}")
                print(f"    ✗ Error copying {filename}: {e}")
        else:
            results['missing'].append(filename)
            print(f"    ⚠ Missing: {filename}")
    
    return results


def process_ensembles(input_path: str, required_files: List[str] = None) -> None:
    """
    Process all subdirectories in the input path.
    
    Args:
        input_path: Path containing ensemble subdirectories
        required_files: List of files to copy (default: topology.pdb, samples.xtc, sequence.fasta)
    """
    if required_files is None:
        required_files = ['topology.pdb', 'samples.xtc', 'sequence.fasta']
    
    input_dir = Path(input_path).resolve()
    
    if not input_dir.exists():
        print(f"Error: Input path does not exist: {input_dir}")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}")
        sys.exit(1)
    
    # Find all subdirectories
    subdirs = [d for d in input_dir.iterdir() if d.is_dir() and not d.name.endswith('_final_results')]
    
    if not subdirs:
        print(f"No subdirectories found in: {input_dir}")
        sys.exit(0)
    
    print(f"\nProcessing {len(subdirs)} subdirectories in: {input_dir}")
    print(f"Required files: {', '.join(required_files)}\n")
    print("=" * 80)
    
    summary = {
        'processed': 0,
        'created': 0,
        'skipped': 0,
        'total_copied': 0,
        'total_missing': 0,
        'total_errors': 0
    }
    
    for subdir in sorted(subdirs):
        print(f"\n[{summary['processed'] + 1}/{len(subdirs)}] Processing: {subdir.name}")
        
        # Create destination directory name
        dest_dir_name = f"{subdir.name}_final_results"
        dest_dir = input_dir / dest_dir_name
        
        # Create destination directory
        if dest_dir.exists():
            print(f"  → Destination already exists: {dest_dir_name}")
            user_input = input(f"    Overwrite contents? (y/n): ").strip().lower()
            if user_input != 'y':
                print(f"    Skipped.")
                summary['skipped'] += 1
                summary['processed'] += 1
                continue
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            print(f"  → Created: {dest_dir_name}")
            summary['created'] += 1
        
        # Copy files
        print(f"  → Copying files...")
        results = copy_ensemble_files(subdir, dest_dir, required_files)
        
        summary['total_copied'] += len(results['copied'])
        summary['total_missing'] += len(results['missing'])
        summary['total_errors'] += len(results['errors'])
        summary['processed'] += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Directories processed: {summary['processed']}")
    print(f"Directories created:   {summary['created']}")
    print(f"Directories skipped:   {summary['skipped']}")
    print(f"Files copied:          {summary['total_copied']}")
    print(f"Files missing:         {summary['total_missing']}")
    print(f"Errors:                {summary['total_errors']}")
    print("=" * 80)
    
    if summary['total_errors'] > 0:
        print("\n⚠ Warning: Some errors occurred during processing.")
    elif summary['total_missing'] > 0:
        print("\n⚠ Warning: Some required files were missing.")
    else:
        print("\n✓ All operations completed successfully!")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Input path required")
        print("\nUsage:")
        print(f"  python {sys.argv[0]} <input_path>")
        print("\nExample:")
        print(f"  python {sys.argv[0]} ./bioemu_runs")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Optional: allow custom file list as additional arguments
    if len(sys.argv) > 2:
        required_files = sys.argv[2:]
        print(f"Custom file list provided: {required_files}")
    else:
        required_files = None  # Use defaults
    
    try:
        process_ensembles(input_path, required_files)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Create submission zip file including git-tracked files and checkpoints folder.
"""
import os
import subprocess
import zipfile
from pathlib import Path

def main():
    zip_path = "Group 1 parking vision.zip"
    
    # Remove existing zip if it exists
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"Removed existing {zip_path}")
    
    print(f"Creating {zip_path}...")
    
    # Get git-tracked files
    print("Getting git-tracked files...")
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True)
    git_files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
    print(f"Found {len(git_files)} git-tracked files")
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add git-tracked files
        for file_path in git_files:
            if os.path.exists(file_path):
                zipf.write(file_path)
                print(f"Added: {file_path}")
        
        # Add checkpoints folder
        checkpoints_dir = Path("Deployment/checkpoints")
        if checkpoints_dir.exists():
            print(f"\nAdding checkpoints folder...")
            for root, dirs, files in os.walk(checkpoints_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Use relative path from project root
                    arcname = file_path.as_posix()
                    zipf.write(file_path, arcname)
                    print(f"Added: {arcname}")
        else:
            print(f"Warning: {checkpoints_dir} does not exist")
    
    # Get file size
    if os.path.exists(zip_path):
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"\n✓ Zip file created successfully!")
        print(f"  Name: {zip_path}")
        print(f"  Size: {size_mb:.2f} MB")
        print(f"  Location: {os.path.abspath(zip_path)}")
    else:
        print("✗ Failed to create zip file")

if __name__ == "__main__":
    main()



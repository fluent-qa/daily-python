import zipfile
from pathlib import Path
import os


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing or replacing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Replace problematic characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length to avoid path length issues
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:96] + ext  # Keep extension, limit base name
        
    return filename


def extract_zip_with_encoding(zip_path: Path, extract_path: Path = None, remove_zip=False, flat_extract=False):
    """
    Extract a ZIP file with proper encoding handling for Chinese characters.
    
    Args:
        zip_path (Path): Path to the ZIP file
        extract_path (Path, optional): Directory to extract files to. If None, uses zip file name without extension
        remove_zip (bool, optional): Whether to remove the ZIP file after extraction. Defaults to False for safety
        flat_extract (bool, optional): If True, extracts all files to the target directory without creating subdirectories
    
    Warning:
        Be careful with remove_zip=True as it will permanently delete the source ZIP file!
    """
    try:
        zip_path = Path(zip_path)
        if extract_path is None:
            # Use zip file name without extension as the extract directory
            extract_path = zip_path.parent / sanitize_filename(zip_path.stem)
            
        extract_path = Path(extract_path)
        extract_path.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # First try to detect the correct encoding
            sample_name = next((f.filename for f in zip_ref.filelist if not f.filename.endswith('/')), None)
            detected_encoding = None
            
            if sample_name:
                for encoding in ['gbk', 'utf-8', 'cp437']:
                    try:
                        decoded = sample_name.encode('cp437').decode(encoding)
                        # Check if decoded string contains valid Chinese characters
                        decoded.encode('utf-8')
                        detected_encoding = encoding
                        break
                    except:
                        continue
            
            if not detected_encoding:
                detected_encoding = 'utf-8'  # fallback to utf-8
            
            # Extract files using detected encoding
            for file_info in zip_ref.filelist:
                # Skip directory entries (they end with '/')
                if file_info.filename.endswith('/'):
                    continue
                    
                try:
                    # Decode filename using detected encoding
                    filename = file_info.filename.encode('cp437').decode(detected_encoding)
                except:
                    # Fallback to original filename if decoding fails
                    filename = file_info.filename
                
                # Handle flat extraction by taking only the base name
                if flat_extract:
                    filename = Path(filename).name
                
                # Sanitize the filename
                safe_filename = sanitize_filename(filename)
                
                # Create target path
                target_path = extract_path / safe_filename
                
                # Handle filename conflicts in flat extraction
                if flat_extract and target_path.exists():
                    base, ext = os.path.splitext(safe_filename)
                    counter = 1
                    while target_path.exists():
                        new_name = f"{base}_{counter}{ext}"
                        target_path = extract_path / new_name
                        counter += 1
                else:
                    # Create parent directories if needed (for non-flat extraction)
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Extract the file only if it's not a directory
                if not target_path.is_dir():
                    with zip_ref.open(file_info) as source, open(target_path, 'wb') as target:
                        target.write(source.read())
            
            print(f"Extracted ZIP contents to {extract_path}")
        
        if remove_zip:
            print(f"WARNING: Removing ZIP file: {zip_path}")
            if zip_path.exists():
                zip_path.unlink()
                print(f"Removed ZIP file: {zip_path}")
            
    except Exception as e:
        print(f"Error extracting ZIP {zip_path}: {str(e)}")
        raise

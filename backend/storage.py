# backend/storage.py
from pathlib import Path
PHOTO_DIR = Path('photos')
def save_photo(watch_id: int, uploaded_file) -> str:
    """Save a Streamlit UploadedFile. Returns the file path as a string."""
    folder = PHOTO_DIR / str(watch_id)
    folder.mkdir(parents=True, exist_ok=True)
    # Use the original filename — add watch_id prefix to avoid collisions
    path = folder / uploaded_file.name
    with open(path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return str(path)
def get_photos(watch_id: int) -> list[Path]:
    """Return all photo Paths for a watch, sorted by name."""
    folder = PHOTO_DIR / str(watch_id)
    if not folder.exists():
        return []
    return sorted(folder.iterdir())
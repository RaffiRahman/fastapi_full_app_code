import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.schemas.file import UploadResponse

router = APIRouter()

@router.post("/", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    """Save an uploaded file and return its accessible URL.

    The upload directory is created with ``755`` permissions to ensure other
    processes can read files while preventing unauthorized writes.
    """
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    upload_dir.chmod(0o755)

    extension = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{extension}"
    file_path = upload_dir / unique_name

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    return UploadResponse(url=f"/uploads/{unique_name}")
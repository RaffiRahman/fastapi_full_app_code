from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ip_filter import verify_admin_ip
from app.crud import crud_user as crud
from app.dependencies import get_current_active_superuser
from app.schemas import user as schemas_user

router = APIRouter(dependencies=[Depends(verify_admin_ip)])


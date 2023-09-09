import time

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/long_operation')
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return 'Too much data'


@router.get('')
async def get_specific_operations(
        operation_type: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.all(),
            # [dict(zip(result.keys(), row)) for row in result.fetchall()],
            'details': None
        }

        # [dict(r._mapping) for r in result]

    except Exception:
        # send error to developer
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None})

    # return result.all() is returned error, answer at:
    # https://stackoverflow.com/questions/76322342/fastapi-sqlalchemy-cannot-convert-dictionary-update-sequence-element-0-to-a-seq


@router.post('')
async def add_specific_operations(
        new_operation: OperationCreate,
        session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


@router.get('/main')
async def main(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(1))
    return result.all()

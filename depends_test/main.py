from fastapi import FastAPI, Depends, Request, HTTPException, APIRouter

app = FastAPI()


async def get_async_session():
    print('Getting session')
    session = 'session'
    yield session
    print('Closing session')


@app.get('/items')
async def get_items(session=Depends(get_async_session)):
    print(session)
    return [{'id': 1}]


def pagination_params(limit: int = 10, skip: int = 0):
    return {'limit': limit, 'skip': skip}


@app.get('/subjects')
async def get_items(pages: dict = Depends(pagination_params)):
    return pages


class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


@app.get('/subjects_class')
async def get_subjects_class(pages: Paginator = Depends(Paginator)):
    return pages


class AuthGuard:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, request: Request):
        if 'super_cookie' not in request.cookies:
            raise HTTPException(status_code=403, detail='Forbidden')
        return True


auth_guard_payments = AuthGuard('payments')


router = APIRouter(
    dependencies=[Depends(auth_guard_payments)]
)


@app.get('/payments', dependencies=[Depends(auth_guard_payments)])
def get_payments():
    return 'my payments...'

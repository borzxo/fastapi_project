from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post('/operations', json={
        "id": 1,
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2004-10-19 12:23:54",
        "type": "Выплата купонов",
    })

    assert response.status_code == 200


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get('/operations', params={
        'operation_type': 'Выплата купонов',
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'success'
    assert len(response.json()['data']) == 1

import asyncio
import random
from typing import List

import httpcore
import httpx
from dadata import DadataAsync

from entity import Entity


TOKEN = '577e6e06ff78d3eaa2da1b750ddcabe7ee175f83'

PARTY_NAME = 'party'
REQUESTS_PER_SECOND = 10


def entity_from_json(data: dict) -> Entity:
    return Entity(
        Name=data['value'],
        INN=int(data['data']['inn']),
        OGRN=int(data['data']['ogrn']),
        IsActive=data['data']['state']['status'] == 'ACTIVE'
    )


async def get_entity_by_inn(inn: int, dadata: DadataAsync, task_id: int = 0, **filters) -> Entity:
    await asyncio.sleep(int(task_id / REQUESTS_PER_SECOND) + 1)
    while True:
        try:
            response = await dadata.find_by_id(PARTY_NAME, str(inn), **filters)
            if response:
                return entity_from_json(response[0])
        except (httpcore.ConnectTimeout, httpcore.ConnectError, httpx.ConnectTimeout, httpx.ConnectError):
            await asyncio.sleep(random.random())


async def get_entities_by_inn(inns: List[int], **filters) -> list[Entity]:
    dadata = DadataAsync(TOKEN)
    result = list(await asyncio.gather(
        *(get_entity_by_inn(inn, dadata, task_id=task_id, **filters) for task_id, inn in enumerate(inns, start=1)),
        return_exceptions=False
    ))
    await dadata.close()
    return result

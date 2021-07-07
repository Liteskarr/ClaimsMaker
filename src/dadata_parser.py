from typing import List

from dadata import Dadata

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


def get_entities_by_inn(inns: List[int], **filters) -> list[Entity]:
    result = []
    dadata = Dadata(TOKEN)
    for inn in inns:
        try:
            response = dadata.find_by_id(PARTY_NAME, str(inn), **filters)
            if response:
                result.append(entity_from_json(response[0]))
        except Exception:
            pass
    dadata.close()
    return result

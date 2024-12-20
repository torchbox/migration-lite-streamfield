import uuid

from typing import Any, Sequence


def convert_simple_streamfield_value_to_dicts(
    value: Sequence[tuple[str, Any]], *, add_ids: bool = False
) -> list[dict[str, Any]]:
    return_value = []
    for item in value:
        item_dict = {
            "type": item[0],
            "value": item[1],
        }
        if add_ids:
            item_dict["id"] = uuid.uuid4().hex
        return_value.append(item_dict)
    return return_value

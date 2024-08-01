from typing import Any

from pydantic import BaseModel


class Detail(BaseModel):
    detail: str


def get_responses_detail_dict(
    status_codes: list[int] | None = None,
) -> dict[int | str, dict[str, Any]]:
    if status_codes is None:
        return {}
    return {status_code: {"model": Detail} for status_code in status_codes}

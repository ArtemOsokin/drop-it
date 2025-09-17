from typing import Iterable
from pydantic import BaseModel

def apply_schema(
    model: object,
    schema: BaseModel,
    allowed_fields: Iterable[str] | None = None,
) -> object:
    """
    Применяет частичное обновление из Pydantic-схемы к SQLAlchemy-модели.
    - учитывает exclude_unset (только реально переданные поля)
    - mode='json' (HttpUrl/Email/Decimal → str/числа)
    - применяет white-list полей
    """
    data = schema.model_dump(exclude_unset=True, mode="json")

    if allowed_fields is not None:
        data = {k: v for k, v in data.items() if k in set(allowed_fields)}

    for field, value in data.items():
        if hasattr(model, field):
            setattr(model, field, value)

    return model

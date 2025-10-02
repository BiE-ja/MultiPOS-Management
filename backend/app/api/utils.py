# Champs autorisés pour le tri
from sqlalchemy.orm.attributes import InstrumentedAttribute


def getSortableFields() -> dict[str, InstrumentedAttribute[object]]:
    from app.dto.models.models import User

    return {
        "id": User.id,
        "last_name": User.last_name,
        "created_at": User.created_at,
    }

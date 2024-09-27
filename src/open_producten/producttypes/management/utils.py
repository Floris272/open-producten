import logging
from typing import Any, Dict, List

from open_producten.producttypes.models import UniformProductName

logger = logging.getLogger(__name__)


def load_upn(data: List[Dict[str, Any]]) -> int:
    """
    Loads UPNs based on a list of dictionaries.
    """
    count = 0
    upn_updated_list = []

    for obj in data:
        upn, created = UniformProductName.objects.update_or_create(
            uri=obj.get("URI"),
            defaults={"name": obj.get("UniformeProductnaam"), "is_deleted": False},
        )
        upn_updated_list.append(upn.id)

        if created:
            count += 1

    UniformProductName.objects.exclude(id__in=upn_updated_list).update(
        is_deleted=True,
    )
    return count

def check_for_duplicates_in_array(objects: list, field: str, errors):
    object_set = set()
    for idx, obj in enumerate(objects):
        if obj in object_set:
            errors[field] = (
                f"Duplicate {type(obj).__name__} id: {obj.id} at index {idx}"
            )

        object_set.add(obj)

def build_array_duplicates_error_message(objects: list, field: str, errors):
    object_set = set()
    errors_messages = []
    for idx, obj in enumerate(objects):
        if obj in object_set:
            errors_messages.append(
                f"Duplicate {type(obj).__name__} id: {obj.id} at index {idx}"
            )

        object_set.add(obj)

    if errors_messages:
        errors[field] = errors_messages

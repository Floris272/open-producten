def build_formset_data(form_name: str, *forms: dict, extra: dict | None = None):
    data = (extra if extra else {}) | {
        f"{form_name}-TOTAL_FORMS": len(forms),
        f"{form_name}-INITIAL_FORMS": "0",
    }

    for i, form in enumerate(forms):
        for key in form:
            data[f"{form_name}-{i}-{key}"] = form[key]

    return data

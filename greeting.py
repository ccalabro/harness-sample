def greet_person(name: str) -> str:
    """Return a greeting for a nonblank person's name."""
    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("name must not be blank")
    return f"Hello, {normalized_name}!"

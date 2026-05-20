def validate_create_room(data):
    if not isinstance(data, dict):
        return False, "Input data must be a JSON object"

    required_fields = ["key", "room_name", "password"]

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    return True, None
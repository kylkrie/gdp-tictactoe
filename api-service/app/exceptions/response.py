def error_response(error_type: str, message: str) -> dict:
    return {"error": {"type": error_type, "message": message}}

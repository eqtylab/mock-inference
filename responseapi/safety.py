"""Mock safety service; not a production guardrail."""


def check_content(text):
    return {"policy": "mock-safety", "result": "pass"}

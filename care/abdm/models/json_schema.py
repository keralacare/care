CARE_CONTEXTS = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "content": [
        {
            "type": "object",
            "properties": {
                "patientReference": {"type": "string"},
                "careContextReference": {"type": "string"},
            },
            "additionalProperties": False,
            "required": ["patientReference", "careContextReference"],
        }
    ],
}

CONSENT_ARTEFACTS = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "content": [
        {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
            },
            "additionalProperties": False,
            "required": ["id"],
        }
    ],
}

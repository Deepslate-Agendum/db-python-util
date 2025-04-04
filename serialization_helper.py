from mongoengine import Document
from typing import List, Optional

import json

def get_fields(object: Document, fields: Optional[List[str]] = None):
    # TODO: actually use fields and serialize IDs properly
    return json.loads(object.to_json())

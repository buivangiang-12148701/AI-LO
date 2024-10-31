from fastapi import Response
from typing import Any
import gzip
import json

class OptimizedResponse(Response):
    def __init__(
        self,
        content: Any,
        compress: bool = True,
        cache_control: str = "public, max-age=3600",
        *args,
        **kwargs
    ):
        if compress and isinstance(content, (dict, list)):
            content = gzip.compress(json.dumps(content).encode())
            headers = {
                "Content-Encoding": "gzip",
                "Cache-Control": cache_control
            }
        else:
            headers = {"Cache-Control": cache_control}
            
        super().__init__(
            content=content,
            headers=headers,
            *args,
            **kwargs
        ) 
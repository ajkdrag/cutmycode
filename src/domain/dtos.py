from dataclasses import dataclass
from src.domain.entities import Snippet
from src.domain.value_objects import SnippetMetadata


@dataclass(kw_only=True)
class SnippetWithMetadata(Snippet):
    metadata: SnippetMetadata

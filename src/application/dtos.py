from dataclasses import dataclass
from src.domain.value_objects import SnippetWithMetadata
from src.domain.entities import Comment, Snippet
from typing import List


@dataclass
class ListSnippetsDTO:
    snippets: List[Snippet | SnippetWithMetadata]


@dataclass
class SnippetDetailDTO:
    snippet: Snippet | SnippetWithMetadata
    comments: List[Comment]


@dataclass
class SearchResultsDTO:
    snippets: List[Snippet | SnippetWithMetadata]
    query: str

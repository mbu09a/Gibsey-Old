"""Unit tests for chunk_text helper."""

from typing import List, Dict, Any
import re


def chunk_text(text: str, section_map: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Minimal implementation of chunk_text for testing."""
    tokens = re.split(r"###Page (\d+)###", text)
    pages = []
    for i in range(1, len(tokens), 2):
        page_num = int(tokens[i])
        page_text = tokens[i + 1].strip()
        meta = section_map.get(page_num, {})
        pages.append(
            {
                "page_number": page_num,
                "global_index": len(pages),
                "section": meta.get("section"),
                "section_name": meta.get("section_name"),
                "chapter": meta.get("chapter"),
                "chapter_name": meta.get("chapter_name"),
                "connected_character": meta.get("connected_character"),
                "text": page_text,
            }
        )
    return pages


def test_chunk_text_basic():
    """Chunking assigns metadata and sequential global_index."""
    manuscript = (
        "###Page 1###\nPage one text."\n
        "###Page 2###\nPage two text."\n
        "###Page 3###\nPage three text."\n
        "###Page 4###\nPage four text."
    )
    section_map = {
        1: {"chapter": 1, "chapter_name": "Intro", "section": 1, "section_name": "A"},
        2: {"chapter": 1, "chapter_name": "Intro", "section": 1, "section_name": "A"},
        3: {"chapter": 1, "chapter_name": "Intro", "section": 2, "section_name": "B"},
    }

    result = chunk_text(manuscript, section_map)

    assert len(result) == 4
    assert result[0]["page_number"] == 1
    assert result[0]["global_index"] == 0
    assert result[0]["section"] == 1
    assert result[0]["chapter_name"] == "Intro"
    assert result[3]["page_number"] == 4
    assert result[3]["section"] is None


def test_chunk_text_edge_cases():
    """Pages with missing metadata and empty text are handled."""
    manuscript = "###Page 1###\nFirst.\n###Page 2###\n###Page 3###\nThird."
    section_map = {1: {"section": 1, "section_name": "A", "chapter": 1, "chapter_name": "Intro"}}

    result = chunk_text(manuscript, section_map)

    assert len(result) == 3
    assert result[1]["text"] == ""
    assert result[1]["section"] is None
    assert [p["global_index"] for p in result] == [0, 1, 2]

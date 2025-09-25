import fitz
from typing import Dict, List

def _build_chapter_map(pdf_path: str) -> Dict[int, int]:
    """Return a mapping from 1-based page number to chapter number (level-1 TOC index).

    If no TOC is found, returns an empty mapping (caller may fill None).
    """
    try:
        doc = fitz.open(pdf_path)
        toc = doc.get_toc(simple=True)  # list of [level, title, page]
        # Collect level-1 entries with starting page
        level1 = [(title, page) for level, title, page in toc if level == 1 and page and page > 0]
        if not level1:
            return {}

        # Determine page ranges for each chapter
        # Chapter i: [start_page_i, start_page_{i+1}) except last which goes to last page
        chapter_starts = [page for _, page in level1]
        chapter_starts_sorted = sorted(set(chapter_starts))
        chapter_ranges: List[tuple[int, int, int]] = []  # (chapter_no, start, end_inclusive)
        for idx, start_page in enumerate(chapter_starts_sorted, start=1):
            if idx < len(chapter_starts_sorted):
                end_page = chapter_starts_sorted[idx] - 1
            else:
                end_page = doc.page_count
            chapter_ranges.append((idx, start_page, end_page))

        page_to_chapter: Dict[int, int] = {}
        for chapter_no, start_p, end_p in chapter_ranges:
            for p in range(start_p, end_p + 1):
                page_to_chapter[p] = chapter_no
        return page_to_chapter
    except Exception:
        return {}
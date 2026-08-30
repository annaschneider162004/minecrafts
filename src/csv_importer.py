from __future__ import annotations

import csv
from pathlib import Path

from src.exporters import export_markdown, save_keyword_to_csv
from src.generators import create_video_plan
from src.models import VideoPlan
from src.production_kit import export_video_package


def _normalize_header(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")


def _read_number(value: str) -> float:
    return float(value.replace(",", "").strip())


def import_vidiq_csv(path: str | Path, create_packages: bool = False) -> list[VideoPlan]:
    """Import keyword rows from a vidIQ-style CSV file.

    Expected columns can be named:
    - keyword / Keyword
    - volume / search_volume / Search Volume
    - competition / Competition
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {csv_path}")

    plans: list[VideoPlan] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV không có header.")

        header_map = {_normalize_header(field): field for field in reader.fieldnames}
        keyword_col = header_map.get("keyword")
        volume_col = header_map.get("volume") or header_map.get("search_volume") or header_map.get("monthly_search_volume")
        competition_col = header_map.get("competition") or header_map.get("difficulty")

        if not keyword_col or not volume_col or not competition_col:
            raise ValueError(
                "CSV cần có cột keyword, volume/search_volume, competition. "
                f"Header hiện có: {', '.join(reader.fieldnames)}"
            )

        for row_number, row in enumerate(reader, start=2):
            keyword = (row.get(keyword_col) or "").strip()
            if not keyword:
                continue

            try:
                volume = int(_read_number(row.get(volume_col) or "0"))
                competition = float((row.get(competition_col) or "0").replace(",", "."))
            except ValueError as exc:
                raise ValueError(f"Dữ liệu số không hợp lệ ở dòng {row_number}: {row}") from exc

            plan = create_video_plan(keyword, volume, competition)
            save_keyword_to_csv(plan)
            export_markdown(plan)
            if create_packages:
                export_video_package(plan)
            plans.append(plan)

    plans.sort(key=lambda item: item.opportunity_score, reverse=True)
    return plans

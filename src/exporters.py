from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

from src.models import ModSetupPlan, ToolItem, VideoPlan

DATA_DIR = Path("output")
CSV_FILE = DATA_DIR / "minecraft_keywords.csv"


def ensure_output_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "video-plan"


def save_keyword_to_csv(plan: VideoPlan) -> None:
    ensure_output_dir()
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        fieldnames = [
            "date",
            "keyword",
            "volume",
            "competition",
            "competition_label",
            "opportunity_score",
            "priority",
            "build_type",
            "video_format",
            "best_title",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "keyword": plan.keyword,
                "volume": plan.volume,
                "competition": plan.competition,
                "competition_label": plan.competition_label,
                "opportunity_score": plan.opportunity_score,
                "priority": plan.priority,
                "build_type": plan.build_type,
                "video_format": plan.video_format,
                "best_title": plan.titles[0],
            }
        )


def markdown_list(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_markdown_list(items: Iterable[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def export_markdown(plan: VideoPlan) -> Path:
    ensure_output_dir()
    filename = DATA_DIR / f"{slugify(plan.keyword)}_video_plan.md"
    tags_text = ", ".join(plan.tags)

    markdown = f"""# Minecraft YouTube Video Plan

## Keyword

**{plan.keyword}**

## vidIQ Data

- Search volume/month: **{plan.volume}**
- Competition: **{plan.competition}/100**
- Competition level: **{plan.competition_label}**
- Opportunity score: **{plan.opportunity_score}/100**
- Priority: **{plan.priority}**

## Video Type

- Build type: **{plan.build_type}**
- Video format: **{plan.video_format}**

---

## Recommended Titles

{numbered_markdown_list(plan.titles)}

---

## Recommended Production Tools

{markdown_list(plan.production_tools)}

---

## AI Build Prompt

```text
{plan.ai_build_prompt}
```

---

## Description

```text
{plan.description}
```

---

## Tags

```text
{tags_text}
```

---

## Thumbnail Text Ideas

{markdown_list(plan.thumbnail_text)}

---

## Shot List

{markdown_list(plan.shot_list)}

---

## Editing Checklist

{markdown_list(plan.editing_checklist)}

---

## Shorts Ideas

{markdown_list(plan.shorts_ideas)}

---

## Script Outline

```text
{plan.script_outline}
```
"""

    filename.write_text(markdown, encoding="utf-8")
    return filename


def export_mod_setup_plan(plan: ModSetupPlan) -> Path:
    ensure_output_dir()
    filename = DATA_DIR / "minecraft_mod_recording_setup.md"

    tools_table = "| Tool/Mod | Nhóm | Bắt buộc? | Công dụng | Ghi chú |\n|---|---|---|---|---|\n"
    for tool in plan.recommended_tools:
        required = "Có" if tool.required else "Không"
        tools_table += f"| {tool.name} | {tool.category} | {required} | {tool.purpose} | {tool.notes} |\n"

    markdown = f"""# Minecraft Build + Recording Mod Setup

## Setup chính

- Edition: **{plan.minecraft_edition}**
- Mod loader khuyên dùng: **{plan.mod_loader}**

## Tool/Mod đề xuất

{tools_table}

---

## Các bước cài đặt

{numbered_markdown_list(plan.install_steps)}

---

## Workflow tự quay video / cinematic

{numbered_markdown_list(plan.recording_workflow)}

---

## Cấu trúc thư mục sản xuất video

```text
{chr(10).join(plan.folder_structure)}
```

---

## Lưu ý an toàn

{markdown_list(plan.safety_notes)}
"""

    filename.write_text(markdown, encoding="utf-8")
    return filename

#!/usr/bin/env python3
"""
Minecraft YouTube Keyword & Video Planner

A small standard-library-only CLI tool that helps plan Minecraft build videos
from keyword metrics gathered manually from tools such as vidIQ.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

DATA_DIR = Path("output")
CSV_FILE = DATA_DIR / "minecraft_keywords.csv"


@dataclass
class VideoPlan:
    keyword: str
    volume: int
    competition: float
    competition_label: str
    opportunity_score: float
    priority: str
    build_type: str
    video_format: str
    ai_build_prompt: str
    titles: list[str]
    description: str
    tags: list[str]
    thumbnail_text: list[str]
    shot_list: list[str]
    editing_checklist: list[str]
    shorts_ideas: list[str]
    script_outline: str


def ensure_output_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "video-plan"


def parse_int_input(value: str) -> int:
    cleaned = value.replace(",", "").strip()
    return int(float(cleaned))


def parse_float_input(value: str) -> float:
    return float(value.replace(",", ".").strip())


def volume_score(volume: int) -> int:
    """Convert monthly search volume into a 0-100 score."""
    if volume >= 300_000:
        return 100
    if volume >= 100_000:
        return 90
    if volume >= 50_000:
        return 80
    if volume >= 20_000:
        return 70
    if volume >= 10_000:
        return 60
    if volume >= 5_000:
        return 50
    if volume >= 1_000:
        return 35
    if volume >= 500:
        return 25
    return 15


def competition_label(competition: float) -> str:
    if competition <= 30:
        return "Low"
    if competition <= 55:
        return "Medium"
    return "High"


def calculate_opportunity_score(volume: int, competition: float) -> float:
    """
    Opportunity score rewards high search volume and low competition.

    Formula:
        score = volume_score(volume) - competition + 30
    """
    score = volume_score(volume) - competition + 30
    return round(max(0, min(100, score)), 1)


def priority_label(score: float) -> str:
    if score >= 75:
        return "Very High"
    if score >= 60:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def guess_build_type(keyword: str) -> str:
    keyword_lower = keyword.lower()

    rules = [
        (("survival", "base"), "survival base"),
        (("starter",), "starter house"),
        (("beginner",), "starter house"),
        (("modern",), "modern house"),
        (("underground",), "underground base"),
        (("secret",), "secret base"),
        (("castle",), "castle"),
        (("treehouse",), "treehouse"),
        (("tree house",), "treehouse"),
        (("farm",), "farm house"),
        (("village",), "village upgrade"),
        (("horror",), "haunted mansion"),
        (("scary",), "haunted mansion"),
        (("haunted",), "haunted mansion"),
        (("medieval",), "medieval house"),
        (("japanese",), "Japanese house"),
        (("mountain",), "mountain base"),
        (("ocean",), "ocean base"),
        (("desert",), "desert base"),
    ]

    for needles, build_type in rules:
        if all(needle in keyword_lower for needle in needles):
            return build_type

    return "survival base"


def guess_video_format(keyword: str) -> str:
    keyword_lower = keyword.lower()

    if "tutorial" in keyword_lower or "how to" in keyword_lower:
        return "tutorial"
    if "timelapse" in keyword_lower:
        return "timelapse"
    if "ai" in keyword_lower or "chatgpt" in keyword_lower:
        return "AI challenge"
    if "ideas" in keyword_lower:
        return "build ideas"
    if "horror" in keyword_lower or "scary" in keyword_lower or "haunted" in keyword_lower:
        return "horror build"
    if "survival" in keyword_lower:
        return "survival build"
    if "before" in keyword_lower or "after" in keyword_lower:
        return "before and after"

    return "tutorial"


def generate_ai_build_prompt(keyword: str, build_type: str) -> str:
    return f"""Design a Minecraft {build_type} for a YouTube video targeting the keyword: \"{keyword}\".

Requirements:
- Style: visually impressive but buildable in survival mode
- Include: storage room, bedroom, crafting area, furnace area, farm, enchanting room, and secret room
- Use mostly obtainable blocks
- Make the build look good from the front for thumbnail
- Keep the design clear enough for a tutorial or timelapse video

Give me:
1. Build concept
2. Block palette
3. Room layout
4. Step-by-step building plan
5. 5 details that make the build unique
6. Cinematic reveal ideas for Replay Mod
7. Thumbnail concept
"""


def generate_titles(keyword: str, build_type: str, video_format: str) -> list[str]:
    base = keyword.title()
    build_title = build_type.title()

    titles = [
        f"{base} Tutorial - Easy Minecraft Build",
        f"I Built the Perfect {build_title} in Minecraft",
        f"Easy {base} You Can Build Today",
        f"Minecraft {build_title} Build, But AI Designed It",
        f"I Asked AI to Design a {build_title} in Minecraft",
        "This Minecraft Build Looks Simple... But Has a Secret",
        f"{base}: Full Build Tutorial",
        f"How to Build a {build_title} in Minecraft",
        f"AI Designed My Minecraft {build_title}",
        f"Minecraft Build Tutorial: {build_title} Edition",
    ]

    if video_format == "AI challenge":
        titles = [
            f"I Asked AI to Design a Minecraft {build_title}",
            "Minecraft But AI Decides What I Build",
            f"ChatGPT Designed My Minecraft {build_title}",
        ] + titles

    if video_format == "horror build":
        titles = [
            f"I Built the Scariest {build_title} in Minecraft",
            "AI Designed a Haunted Minecraft Build",
            "Minecraft But Every Build Gets Scarier",
        ] + titles

    # Preserve order while deduplicating.
    deduped: list[str] = []
    for title in titles:
        if title not in deduped:
            deduped.append(title)

    return deduped[:10]


def generate_description(keyword: str, build_type: str) -> str:
    return f"""In this video, I build a Minecraft {build_type} based on the keyword \"{keyword}\".

This Minecraft build includes a full exterior, interior, storage area, survival features, and a final cinematic reveal. If you enjoy Minecraft build tutorials, Minecraft survival bases, Minecraft house builds, and AI Minecraft build challenges, this video is for you.

Comment what Minecraft build I should make next.

Main keyword: {keyword}

#Minecraft #MinecraftBuild #MinecraftBuildTutorial #MinecraftSurvival #MinecraftHouse #MinecraftAI
"""


def generate_tags(keyword: str, build_type: str) -> list[str]:
    tags = [
        keyword,
        "minecraft build",
        "minecraft build tutorial",
        "minecraft house build",
        "minecraft survival build",
        "minecraft survival base",
        "easy minecraft build",
        "minecraft building",
        "minecraft tutorial",
        "minecraft ideas",
        f"minecraft {build_type}",
        f"{build_type} minecraft",
        "ai minecraft build",
        "chatgpt minecraft",
        "minecraft ai",
        "minecraft timelapse",
        "minecraft shorts",
    ]

    clean_tags: list[str] = []
    for tag in tags:
        tag = tag.lower().strip()
        if tag and tag not in clean_tags:
            clean_tags.append(tag)

    return clean_tags


def generate_thumbnail_text(keyword: str) -> list[str]:
    keyword_lower = keyword.lower()
    ideas = [
        "AI BUILT THIS?",
        "SECRET BASE!",
        "EASY BUILD!",
        "INSANE BUILD!",
        "I BUILT THIS!",
        "HIDDEN ROOM!",
        "MINECRAFT BUILD",
        "AI DESIGN!",
        "SURVIVAL BASE!",
        "BEFORE / AFTER",
    ]

    if "horror" in keyword_lower or "scary" in keyword_lower or "haunted" in keyword_lower:
        ideas = ["SCARY BUILD!", "HAUNTED!"] + ideas

    if "secret" in keyword_lower:
        ideas = ["SECRET ROOM!"] + ideas

    if "starter" in keyword_lower or "easy" in keyword_lower:
        ideas = ["EASY!"] + ideas

    deduped: list[str] = []
    for idea in ideas:
        if idea not in deduped:
            deduped.append(idea)

    return deduped[:8]


def generate_shot_list() -> list[str]:
    return [
        "Hook shot: show the final build for 2 seconds, then cut before the full reveal",
        "Show the empty land before building",
        "Show the AI prompt or build plan on screen",
        "Foundation timelapse",
        "Wall construction timelapse",
        "Roof construction timelapse",
        "Interior design montage",
        "Secret room / special feature reveal",
        "Cinematic outside reveal with Replay Mod",
        "Cinematic inside tour",
        "Before vs after comparison",
        "End screen asking viewers what to build next",
    ]


def generate_editing_checklist() -> list[str]:
    return [
        "First 5 seconds must show the final result or a strong hook",
        "Cut slow parts from building footage",
        "Use speed ramps during timelapse",
        "Add captions for important steps",
        "Add zooms on secret features",
        "Use sound effects for reveals",
        "Keep background music lower than voice",
        "Add chapter text: Foundation, Walls, Roof, Interior, Reveal",
        "End with a strong final cinematic shot",
        "Add subscribe CTA only after value is delivered",
    ]


def generate_shorts_ideas(build_type: str) -> list[str]:
    return [
        f"Before vs after: Minecraft {build_type}",
        "AI designed this Minecraft build",
        f"Secret room inside my Minecraft {build_type}",
        f"Fast timelapse of a Minecraft {build_type}",
        "3 details that make this Minecraft build better",
        f"Minecraft build hack for {build_type}",
        f"The final reveal of my Minecraft {build_type}",
        "Can you build this in survival?",
        "Rate this Minecraft build from 1 to 10",
        "What should AI design next?",
    ]


def generate_script_outline(build_type: str) -> str:
    return f"""0:00 - Hook
Show the final build quickly.
Line: \"I asked AI to design a Minecraft {build_type}, and the result was actually insane.\"

0:10 - The Challenge
Explain the idea.
Line: \"The goal is simple: take an AI-generated design and turn it into a real Minecraft build.\"

0:30 - The AI Plan
Show the AI concept, block palette, and required rooms.

1:00 - Foundation
Start building the layout.
Mention why the size and shape matter.

2:00 - Walls and Structure
Build the main frame.
Retention line: \"The secret room is going under this part, but I don't want it to look obvious.\"

3:30 - Roof and Exterior Details
Add depth, stairs, slabs, trapdoors, leaves, lanterns, and texture.

5:00 - Interior
Add storage, crafting, furnace, bed, enchanting setup, and decorations.

6:30 - Secret Feature
Reveal the hidden room, hidden entrance, or trapdoor.

7:30 - Final Cinematic Reveal
Use Replay Mod cinematic shots.

8:00 - Outro
Ask viewers to comment the next build idea.
Line: \"Comment what AI should design next, and I'll build the best idea.\"
"""


def create_video_plan(keyword: str, volume: int, competition: float) -> VideoPlan:
    build_type = guess_build_type(keyword)
    video_format = guess_video_format(keyword)
    score = calculate_opportunity_score(volume, competition)

    return VideoPlan(
        keyword=keyword,
        volume=volume,
        competition=competition,
        competition_label=competition_label(competition),
        opportunity_score=score,
        priority=priority_label(score),
        build_type=build_type,
        video_format=video_format,
        ai_build_prompt=generate_ai_build_prompt(keyword, build_type),
        titles=generate_titles(keyword, build_type, video_format),
        description=generate_description(keyword, build_type),
        tags=generate_tags(keyword, build_type),
        thumbnail_text=generate_thumbnail_text(keyword),
        shot_list=generate_shot_list(),
        editing_checklist=generate_editing_checklist(),
        shorts_ideas=generate_shorts_ideas(build_type),
        script_outline=generate_script_outline(build_type),
    )


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


def print_plan(plan: VideoPlan) -> None:
    print("\n" + "=" * 60)
    print("MINECRAFT YOUTUBE VIDEO PLAN")
    print("=" * 60)
    print(f"\nKeyword: {plan.keyword}")
    print(f"Volume/month: {plan.volume}")
    print(f"Competition: {plan.competition}/100 - {plan.competition_label}")
    print(f"Opportunity Score: {plan.opportunity_score}/100")
    print(f"Priority: {plan.priority}")
    print(f"Build Type: {plan.build_type}")
    print(f"Video Format: {plan.video_format}")

    print("\nRecommended Titles:")
    for index, title in enumerate(plan.titles, start=1):
        print(f"{index}. {title}")

    print("\nBest Thumbnail Text:")
    for item in plan.thumbnail_text:
        print(f"- {item}")

    print("\nTags:")
    print(", ".join(plan.tags))

    print("\nAI Build Prompt:")
    print(plan.ai_build_prompt)

    print("\nShorts Ideas:")
    for item in plan.shorts_ideas:
        print(f"- {item}")

    print("\n" + "=" * 60)


def process_plan(keyword: str, volume: int, competition: float, show: bool = True) -> VideoPlan:
    plan = create_video_plan(keyword, volume, competition)
    save_keyword_to_csv(plan)
    markdown_file = export_markdown(plan)

    if show:
        print_plan(plan)
        print(f"\nĐã lưu CSV: {CSV_FILE.resolve()}")
        print(f"Đã xuất plan Markdown: {markdown_file.resolve()}")

    return plan


def batch_demo() -> None:
    """Generate demo plans using sample Minecraft keyword metrics."""
    demo_keywords = [
        {"keyword": "minecraft build", "volume": 309_968, "competition": 39.9},
        {"keyword": "minecraft survival base build", "volume": 45_000, "competition": 42},
        {"keyword": "minecraft starter house build", "volume": 38_000, "competition": 37},
        {"keyword": "minecraft build tutorial", "volume": 90_000, "competition": 48},
        {"keyword": "easy minecraft build", "volume": 70_000, "competition": 41},
        {"keyword": "minecraft secret base build", "volume": 30_000, "competition": 44},
        {"keyword": "ai minecraft build", "volume": 5_000, "competition": 24},
        {"keyword": "chatgpt minecraft build", "volume": 3_000, "competition": 22},
        {"keyword": "minecraft but ai builds my house", "volume": 1_500, "competition": 18},
        {"keyword": "minecraft horror build", "volume": 12_000, "competition": 35},
    ]

    plans: list[VideoPlan] = []
    for item in demo_keywords:
        plans.append(
            process_plan(
                keyword=item["keyword"],
                volume=item["volume"],
                competition=item["competition"],
                show=False,
            )
        )

    plans.sort(key=lambda item: item.opportunity_score, reverse=True)

    print("\nTop keyword opportunities:\n")
    for plan in plans:
        print(
            f"{plan.keyword} | "
            f"Volume: {plan.volume} | "
            f"Competition: {plan.competition} | "
            f"Score: {plan.opportunity_score} | "
            f"Priority: {plan.priority}"
        )

    print(f"\nFiles exported to: {DATA_DIR.resolve()}")


def interactive_mode() -> None:
    print("\nMinecraft YouTube Keyword & Video Planner")
    print("-" * 50)

    keyword = input("Nhập keyword, ví dụ 'minecraft build': ").strip()
    if not keyword:
        print("Keyword không được để trống.")
        return

    volume_input = input("Nhập search volume/tháng từ vidIQ, ví dụ 309968: ").strip()
    competition_input = input("Nhập competition từ vidIQ, ví dụ 39.9: ").strip()

    try:
        volume = parse_int_input(volume_input)
        competition = parse_float_input(competition_input)
    except ValueError:
        print("Volume hoặc competition không hợp lệ. Ví dụ đúng: 309968 và 39.9")
        return

    if volume < 0:
        print("Volume không được âm.")
        return

    if not 0 <= competition <= 100:
        print("Competition nên nằm trong khoảng 0 đến 100.")
        return

    process_plan(keyword, volume, competition, show=True)


def menu() -> None:
    while True:
        print("\n" + "=" * 60)
        print("MINECRAFT YOUTUBE TOOL")
        print("=" * 60)
        print("1. Tạo video plan từ keyword vidIQ")
        print("2. Chạy demo 10 keyword Minecraft")
        print("3. Thoát")

        choice = input("\nChọn chức năng: ").strip()

        if choice == "1":
            interactive_mode()
        elif choice == "2":
            batch_demo()
        elif choice == "3":
            print("Thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Hãy chọn 1, 2 hoặc 3.")


if __name__ == "__main__":
    menu()

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from src.exporters import DATA_DIR, ensure_output_dir, slugify
from src.models import VideoPlan, ProductionPackage


def generate_full_script(plan: VideoPlan) -> str:
    title = plan.titles[0]
    return f"""VIDEO TITLE: {title}
TARGET KEYWORD: {plan.keyword}
VIDEO LENGTH TARGET: 8-10 minutes
STYLE: fast-paced Minecraft build video, clear tutorial, strong final reveal

0:00 - HOOK
I asked AI to design a Minecraft {plan.build_type}, and I honestly didn't expect it to look this good. In the next few minutes, I'm going to turn this empty space into a full build with storage, a farm, an enchanting room, and a hidden secret room.

0:15 - SETUP
The keyword for this video is \"{plan.keyword}\". I want this build to work as both a real survival build and a cinematic YouTube video. So I'm using Minecraft Java Edition, planning the idea with AI, building faster with WorldEdit or Axiom, using Litematica if I need a blueprint, and recording the final shots with Replay Mod.

0:45 - AI CONCEPT
Here is the AI concept. The main idea is a {plan.build_type} that looks good from the front, has a practical interior, and includes one secret feature that viewers will want to see at the end.

1:15 - FOUNDATION
First, I need a clean foundation. This is where WorldEdit or Axiom saves a lot of time. I mark the corners, create the main shape, and make sure the entrance faces the camera so the thumbnail looks strong.

2:15 - WALLS AND SHAPE
Now I build the walls and main structure. The important thing is depth: stairs, slabs, logs, trapdoors, and small block variations make the build look much better than a flat box.

3:30 - ROOF AND EXTERIOR
The roof is where the build starts to look finished. I add overhangs, texture, windows, lanterns, leaves, and a path so the build feels like it belongs in the world.

4:45 - INTERIOR
Now I add the survival rooms: storage, crafting, furnaces, bed area, and enchanting setup. The goal is to make it useful, not just pretty.

6:00 - SECRET FEATURE
This is the part I wanted to hide until now. Behind this section, I added a secret room. This gives the video a payoff and makes people stay until the reveal.

7:00 - FINAL DETAILS
Before the cinematic reveal, I add small details: lighting, plants, barrels, item frames, carpets, trapdoors, and path blocks. These details make the build feel complete.

7:45 - CINEMATIC REVEAL
Now I use Replay Mod for the final reveal: one front camera push-in, one orbit shot, one top-down shot, and one interior walkthrough.

8:30 - OUTRO
That is the finished Minecraft {plan.build_type}. If you want the next build to be designed by AI too, comment the next idea below. Should AI design a castle, a secret base, or a horror mansion next?
"""


def generate_recording_timeline(plan: VideoPlan) -> str:
    return f"""# Detailed Recording Timeline

## Video: {plan.titles[0]}
## Keyword: {plan.keyword}

| Time | Scene | Tool | Notes |
|---|---|---|---|
| 0:00-0:05 | Final build teaser | Replay Mod | Show the best angle only briefly. Do not reveal everything. |
| 0:05-0:15 | Empty land before build | OBS/Replay Mod | Clean before shot for before/after. |
| 0:15-0:45 | AI prompt and challenge explanation | OBS | Record browser/AI prompt or show screenshot in edit. |
| 0:45-1:15 | Block palette and layout | OBS | Show chosen blocks and top-down layout. |
| 1:15-2:15 | Foundation timelapse | Replay Mod | Use WorldEdit/Axiom if needed. Speed up 400-800%. |
| 2:15-3:30 | Walls and structure | Replay Mod | Capture progress from 2 angles. |
| 3:30-4:45 | Roof and exterior details | Replay Mod | Add zooms on details in edit. |
| 4:45-6:00 | Interior montage | OBS/Replay Mod | Show storage, bed, furnaces, enchanting room. |
| 6:00-7:00 | Secret feature reveal | OBS/Replay Mod | Slow down and add sound effect. |
| 7:00-7:45 | Final polish | Replay Mod | Lanterns, leaves, path, texture, decoration. |
| 7:45-8:30 | Cinematic reveal | Replay Mod | Front push-in, orbit, top-down, interior walkthrough. |
| 8:30-8:45 | Outro | OBS/Replay Mod | Ask viewers what AI should build next. |

## Replay Mod camera paths

1. Front reveal: slow push toward the entrance.
2. Orbit shot: 180-360 degree circle around the build.
3. Top-down shot: show roof shape and environment.
4. Interior walkthrough: smooth movement through each important room.
5. Secret room shot: start normal, then reveal hidden entrance.

## Shorts cuts to export

- 15-25 sec before/after reveal.
- 20-35 sec secret room reveal.
- 15-30 sec timelapse of the roof.
- 15-30 sec AI prompt to final build transformation.
"""


def generate_thumbnail_prompt(plan: VideoPlan) -> str:
    thumbnail_text = plan.thumbnail_text[0] if plan.thumbnail_text else "AI BUILT THIS?"
    return f"""# Thumbnail Prompt

## Main text

{thumbnail_text}

## Concept

A high-contrast Minecraft YouTube thumbnail showing a beautiful {plan.build_type} in the center, dramatic lighting, strong depth, glowing windows, and a clear before/after or AI twist.

## Image prompt for AI/image planning

Minecraft {plan.build_type}, cinematic angle, bright colorful blocks, dramatic sunset lighting, glowing windows, detailed survival base, secret room hint, YouTube thumbnail style, high contrast, sharp focus, clean composition, empty space on left for bold text: \"{thumbnail_text}\"

## Thumbnail layout

- Left side: big bold text, 2-3 words maximum.
- Center/right: final Minecraft build.
- Add arrow or glow pointing to secret feature.
- Use yellow/white text with black outline.
- Keep the image readable on mobile.

## Screenshot checklist

- Take one front angle.
- Take one orbit/corner angle.
- Take one night shot with lanterns.
- Take one before/after screenshot.
- Keep UI hidden with F1.
"""


def generate_upload_metadata(plan: VideoPlan) -> str:
    return f"""TITLE OPTIONS
{chr(10).join(f'{index}. {title}' for index, title in enumerate(plan.titles, start=1))}

RECOMMENDED TITLE
{plan.titles[0]}

DESCRIPTION
{plan.description}

TAGS
{', '.join(plan.tags)}

PINNED COMMENT
What should AI design next in Minecraft: a castle, a secret base, a starter house, or a horror mansion?

HASHTAGS
#Minecraft #MinecraftBuild #MinecraftTutorial #MinecraftAI #ReplayMod

UPLOAD CHECKLIST
[ ] Main keyword appears in title
[ ] Main keyword appears in first 2 lines of description
[ ] Thumbnail text is readable on mobile
[ ] End screen added
[ ] 3-5 Shorts exported from the video
[ ] Comment question added
"""


def generate_shorts_plan(plan: VideoPlan) -> str:
    shorts = [
        ("Short 1", "AI prompt to final build", "Show AI idea first, then final build reveal."),
        ("Short 2", "Before vs after", "Start with empty land, cut to finished build."),
        ("Short 3", "Secret room reveal", "Show normal wall/floor, then reveal hidden room."),
        ("Short 4", "Replay Mod cinematic", "Use orbit shot with trending audio."),
        ("Short 5", "Build hack", "Show one detail from the build that viewers can copy."),
    ]

    table = "| Short | Hook | Content | CTA |\n|---|---|---|---|\n"
    for name, hook, content in shorts:
        table += f"| {name} | {hook} | {content} | Comment what to build next. |\n"

    return f"""# Shorts Plan

## Source video

{plan.titles[0]}

## Shorts to create

{table}

## Shorts caption templates

1. AI designed this Minecraft build... did it cook?
2. From empty land to full Minecraft {plan.build_type}.
3. I hid a secret room inside this Minecraft build.
4. Replay Mod makes Minecraft builds look insane.
5. Would you build this in survival?
"""


def generate_production_checklist(plan: VideoPlan) -> str:
    checklist = [
        "Keyword checked in vidIQ",
        "Video title selected",
        "AI build prompt generated",
        "Build concept approved",
        "Minecraft Java Edition profile ready",
        "WorldEdit/Axiom tested",
        "Litematica schematic ready if needed",
        "Replay Mod recording enabled",
        "OBS recording tested if voice/UI capture is needed",
        "World backup created before heavy WorldEdit/Axiom changes",
        "Foundation footage recorded",
        "Walls footage recorded",
        "Roof footage recorded",
        "Interior footage recorded",
        "Secret feature footage recorded",
        "Replay Mod cinematic render exported",
        "Voiceover recorded or generated",
        "Music and SFX added",
        "Captions/key text added",
        "Thumbnail created",
        "Description/tags copied",
        "Shorts exported",
        "Video uploaded or scheduled",
    ]

    return "# Production Checklist\n\n" + "\n".join(f"- [ ] {item}" for item in checklist) + "\n"


def export_video_package(plan: VideoPlan) -> ProductionPackage:
    folder = DATA_DIR / "videos" / slugify(plan.keyword)
    folder.mkdir(parents=True, exist_ok=True)

    full_script = generate_full_script(plan)
    recording_timeline = generate_recording_timeline(plan)
    thumbnail_prompt = generate_thumbnail_prompt(plan)
    upload_metadata = generate_upload_metadata(plan)
    shorts_plan = generate_shorts_plan(plan)
    production_checklist = generate_production_checklist(plan)

    files = {
        "01_keyword_summary.md": f"# Keyword Summary\n\n- Keyword: **{plan.keyword}**\n- Volume: **{plan.volume}**\n- Competition: **{plan.competition}**\n- Competition label: **{plan.competition_label}**\n- Opportunity score: **{plan.opportunity_score}**\n- Priority: **{plan.priority}**\n- Build type: **{plan.build_type}**\n- Video format: **{plan.video_format}**\n",
        "02_ai_build_prompt.md": f"# AI Build Prompt\n\n```text\n{plan.ai_build_prompt}\n```\n",
        "03_full_script.txt": full_script,
        "04_recording_timeline.md": recording_timeline,
        "05_thumbnail_prompt.md": thumbnail_prompt,
        "06_upload_metadata.txt": upload_metadata,
        "07_shorts_plan.md": shorts_plan,
        "08_production_checklist.md": production_checklist,
        "README.md": f"# Video Production Package\n\nKeyword: `{plan.keyword}`\n\nStart here:\n\n1. Read `01_keyword_summary.md`\n2. Copy `02_ai_build_prompt.md` into ChatGPT/AI\n3. Record using `04_recording_timeline.md`\n4. Create thumbnail using `05_thumbnail_prompt.md`\n5. Upload with `06_upload_metadata.txt`\n6. Cut Shorts using `07_shorts_plan.md`\n7. Track progress in `08_production_checklist.md`\n",
    }

    for filename, content in files.items():
        (folder / filename).write_text(content, encoding="utf-8")

    return ProductionPackage(
        plan=plan,
        full_script=full_script,
        recording_timeline=recording_timeline,
        thumbnail_prompt=thumbnail_prompt,
        upload_metadata=upload_metadata,
        shorts_plan=shorts_plan,
        production_checklist=production_checklist,
        folder_path=str(folder),
    )


def export_30_day_calendar(plans: list[VideoPlan], start: date | None = None) -> Path:
    if not plans:
        raise ValueError("Cần ít nhất 1 video plan để tạo lịch đăng.")

    ensure_output_dir()
    start_date = start or date.today()
    filename = DATA_DIR / "30_day_content_calendar.md"

    rows = "| Day | Date | Content | Keyword | Format | Notes |\n|---:|---|---|---|---|---|\n"
    long_video_days = {1, 3, 5, 8, 10, 12, 15, 17, 19, 22, 24, 26}
    plan_index = 0

    for day in range(1, 31):
        current_date = start_date + timedelta(days=day - 1)
        plan = plans[plan_index % len(plans)]
        if day in long_video_days:
            content = plan.titles[0]
            fmt = "Long video"
            notes = "Upload full video + create 3 Shorts from this footage"
            plan_index += 1
        else:
            content = plan.shorts_ideas[(day + plan_index) % len(plan.shorts_ideas)]
            fmt = "Shorts"
            notes = "15-35 seconds, strong first 2 seconds"

        rows += f"| {day} | {current_date.isoformat()} | {content} | {plan.keyword} | {fmt} | {notes} |\n"

    filename.write_text(f"# 30-Day Minecraft Content Calendar\n\n{rows}", encoding="utf-8")
    return filename

from __future__ import annotations

from src.models import VideoPlan
from src.scoring import calculate_opportunity_score, competition_label, priority_label


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


def recommended_production_tools(video_format: str) -> list[str]:
    tools = [
        "Minecraft Java Edition - bản chính để build và quay video",
        "WorldEdit - xây nhanh, copy/paste, fill, replace, tạo nền và tường nhanh",
        "Axiom - chỉnh world/build trực quan, rất tốt cho cinematic build",
        "Litematica - dùng schematic/blueprint để dựng lại build chính xác",
        "Replay Mod - mod tự quay/replay camera để tạo timelapse và cinematic reveal",
        "OBS Studio - quay màn hình hoặc thu audio nếu cần",
    ]

    if video_format in {"AI challenge", "tutorial"}:
        tools.append("ChatGPT/AI - tạo concept build, block palette, script và title")
    if video_format in {"timelapse", "horror build"}:
        tools.append("Shader pack + Replay Mod camera path - làm cảnh reveal đẹp hơn")

    return tools


def generate_ai_build_prompt(keyword: str, build_type: str) -> str:
    return f"""Design a Minecraft {build_type} for a YouTube video targeting the keyword: \"{keyword}\".

Requirements:
- Style: visually impressive but buildable in survival mode
- Include: storage room, bedroom, crafting area, furnace area, farm, enchanting room, and secret room
- Use mostly obtainable blocks
- Make the build look good from the front for thumbnail
- Keep the design clear enough for a tutorial or timelapse video
- Suggest where WorldEdit, Axiom, and Litematica can speed up the build
- Suggest Replay Mod camera shots for the final reveal

Give me:
1. Build concept
2. Block palette
3. Room layout
4. Step-by-step building plan
5. 5 details that make the build unique
6. WorldEdit/Axiom speed-build notes
7. Litematica/schematic notes
8. Cinematic reveal ideas for Replay Mod
9. Thumbnail concept
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

    deduped: list[str] = []
    for title in titles:
        if title not in deduped:
            deduped.append(title)

    return deduped[:10]


def generate_description(keyword: str, build_type: str) -> str:
    return f"""In this video, I build a Minecraft {build_type} based on the keyword \"{keyword}\".

This Minecraft build includes a full exterior, interior, storage area, survival features, and a final cinematic reveal. I use a Minecraft Java Edition workflow with building tools like WorldEdit, Axiom, Litematica, and Replay Mod for cinematic recording.

If you enjoy Minecraft build tutorials, Minecraft survival bases, Minecraft house builds, Minecraft timelapses, and AI Minecraft build challenges, this video is for you.

Comment what Minecraft build I should make next.

Main keyword: {keyword}

#Minecraft #MinecraftBuild #MinecraftBuildTutorial #MinecraftSurvival #MinecraftHouse #MinecraftAI #ReplayMod #WorldEdit
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
        "worldedit minecraft",
        "axiom minecraft",
        "litematica minecraft",
        "replay mod minecraft",
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
        "WorldEdit/Axiom setup shot: outline the foundation and main shape",
        "Foundation timelapse",
        "Wall construction timelapse",
        "Roof construction timelapse",
        "Interior design montage",
        "Litematica/blueprint comparison shot if using a schematic",
        "Secret room / special feature reveal",
        "Replay Mod camera path: slow front reveal",
        "Replay Mod camera path: orbit shot around the full build",
        "Replay Mod camera path: inside tour with smooth movement",
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
        "Add labels when using WorldEdit, Axiom, Litematica, or Replay Mod",
        "Use sound effects for reveals",
        "Keep background music lower than voice",
        "Add chapter text: Foundation, Walls, Roof, Interior, Reveal",
        "Add at least 2 Replay Mod cinematic shots in the final reveal",
        "End with a strong final cinematic shot",
        "Add subscribe CTA only after value is delivered",
    ]


def generate_shorts_ideas(build_type: str) -> list[str]:
    return [
        f"Before vs after: Minecraft {build_type}",
        "AI designed this Minecraft build",
        f"Secret room inside my Minecraft {build_type}",
        f"Fast Replay Mod timelapse of a Minecraft {build_type}",
        "3 details that make this Minecraft build better",
        f"Minecraft build hack for {build_type}",
        "WorldEdit made this build 10x faster",
        "Axiom cinematic build reveal",
        "Litematica blueprint vs final build",
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
Show the AI concept, block palette, required rooms, and build rules.

1:00 - Tool Setup
Mention Minecraft Java Edition and the build tools used: WorldEdit/Axiom for fast building, Litematica for blueprint planning, and Replay Mod for cinematic recording.

1:30 - Foundation
Start building the layout.
Mention why the size and shape matter.

2:30 - Walls and Structure
Build the main frame.
Retention line: \"The secret room is going under this part, but I don't want it to look obvious.\"

4:00 - Roof and Exterior Details
Add depth, stairs, slabs, trapdoors, leaves, lanterns, and texture.

5:30 - Interior
Add storage, crafting, furnace, bed, enchanting setup, and decorations.

6:45 - Secret Feature
Reveal the hidden room, hidden entrance, or trapdoor.

7:30 - Final Cinematic Reveal
Use Replay Mod cinematic shots: front reveal, orbit shot, interior tour, and before/after.

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
        production_tools=recommended_production_tools(video_format),
    )

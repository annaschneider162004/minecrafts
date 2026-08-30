from __future__ import annotations

from dataclasses import dataclass


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
    production_tools: list[str]


@dataclass
class ToolItem:
    name: str
    category: str
    purpose: str
    required: bool
    notes: str


@dataclass
class ModSetupPlan:
    minecraft_edition: str
    mod_loader: str
    recommended_tools: list[ToolItem]
    install_steps: list[str]
    recording_workflow: list[str]
    folder_structure: list[str]
    safety_notes: list[str]

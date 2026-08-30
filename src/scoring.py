from __future__ import annotations


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

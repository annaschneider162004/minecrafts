from __future__ import annotations

from datetime import date

from src.csv_importer import import_vidiq_csv
from src.exporters import CSV_FILE, DATA_DIR, export_markdown, export_mod_setup_plan, save_keyword_to_csv
from src.generators import create_video_plan
from src.mod_tools import build_mod_setup_plan
from src.models import VideoPlan
from src.production_kit import export_30_day_calendar, export_video_package


def parse_int_input(value: str) -> int:
    cleaned = value.replace(",", "").strip()
    return int(float(cleaned))


def parse_float_input(value: str) -> float:
    return float(value.replace(",", ".").strip())


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

    print("\nRecommended Production Tools:")
    for item in plan.production_tools:
        print(f"- {item}")

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


def read_keyword_metrics() -> tuple[str, int, float] | None:
    keyword = input("Nhập keyword, ví dụ 'minecraft build': ").strip()
    if not keyword:
        print("Keyword không được để trống.")
        return None

    volume_input = input("Nhập search volume/tháng từ vidIQ, ví dụ 309968: ").strip()
    competition_input = input("Nhập competition từ vidIQ, ví dụ 39.9: ").strip()

    try:
        volume = parse_int_input(volume_input)
        competition = parse_float_input(competition_input)
    except ValueError:
        print("Volume hoặc competition không hợp lệ. Ví dụ đúng: 309968 và 39.9")
        return None

    if volume < 0:
        print("Volume không được âm.")
        return None

    if not 0 <= competition <= 100:
        print("Competition nên nằm trong khoảng 0 đến 100.")
        return None

    return keyword, volume, competition


def process_plan(keyword: str, volume: int, competition: float, show: bool = True) -> VideoPlan:
    plan = create_video_plan(keyword, volume, competition)
    save_keyword_to_csv(plan)
    markdown_file = export_markdown(plan)

    if show:
        print_plan(plan)
        print(f"\nĐã lưu CSV: {CSV_FILE.resolve()}")
        print(f"Đã xuất plan Markdown: {markdown_file.resolve()}")

    return plan


def demo_plans() -> list[VideoPlan]:
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
    return plans


def batch_demo() -> None:
    plans = demo_plans()

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
    values = read_keyword_metrics()
    if values is None:
        return
    process_plan(*values, show=True)


def production_package_mode() -> None:
    print("\nFull Minecraft Video Production Kit")
    print("-" * 50)
    values = read_keyword_metrics()
    if values is None:
        return

    plan = process_plan(*values, show=False)
    package = export_video_package(plan)
    print_plan(plan)
    print(f"\nĐã tạo full production package: {package.folder_path}")
    print("Bao gồm script đầy đủ, recording timeline, thumbnail prompt, upload metadata, shorts plan và checklist.")


def import_csv_mode() -> None:
    print("\nImport keyword CSV từ vidIQ")
    print("-" * 50)
    path = input("Nhập đường dẫn CSV, ví dụ examples/sample_keywords.csv: ").strip()
    create_packages_input = input("Tạo full production package cho từng keyword? (y/N): ").strip().lower()
    create_packages = create_packages_input == "y"

    try:
        plans = import_vidiq_csv(path, create_packages=create_packages)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Lỗi: {exc}")
        return

    print(f"\nĐã import {len(plans)} keyword. Top cơ hội:")
    for plan in plans[:20]:
        print(f"- {plan.keyword} | Volume: {plan.volume} | Competition: {plan.competition} | Score: {plan.opportunity_score}")
    print(f"\nFiles exported to: {DATA_DIR.resolve()}")


def calendar_mode() -> None:
    print("\nTạo lịch đăng 30 ngày")
    print("-" * 50)
    print("Tool sẽ dùng 10 keyword demo để tạo lịch. Bạn có thể sửa file output sau.")
    plans = demo_plans()
    try:
        filename = export_30_day_calendar(plans, start=date.today())
    except ValueError as exc:
        print(f"Lỗi: {exc}")
        return
    print(f"Đã xuất lịch đăng 30 ngày: {filename.resolve()}")


def mod_setup_mode() -> None:
    plan = build_mod_setup_plan()
    filename = export_mod_setup_plan(plan)

    print("\n" + "=" * 60)
    print("MINECRAFT MOD + RECORDING SETUP")
    print("=" * 60)
    print(f"\nEdition: {plan.minecraft_edition}")
    print(f"Mod loader: {plan.mod_loader}")

    print("\nTool/Mod khuyên dùng:")
    for tool in plan.recommended_tools:
        required = "Bắt buộc" if tool.required else "Tuỳ chọn"
        print(f"- {tool.name} ({required}): {tool.purpose}")

    print("\nWorkflow quay video:")
    for index, step in enumerate(plan.recording_workflow, start=1):
        print(f"{index}. {step}")

    print(f"\nĐã xuất setup file: {filename.resolve()}")


def menu() -> None:
    while True:
        print("\n" + "=" * 60)
        print("MINECRAFT YOUTUBE TOOL")
        print("=" * 60)
        print("1. Tạo video plan từ keyword vidIQ")
        print("2. Chạy demo 10 keyword Minecraft")
        print("3. Tạo setup WorldEdit/Axiom/Litematica/Replay Mod")
        print("4. Tạo FULL Video Production Kit cho 1 keyword")
        print("5. Import CSV keyword từ vidIQ")
        print("6. Tạo lịch đăng 30 ngày")
        print("7. Thoát")

        choice = input("\nChọn chức năng: ").strip()

        if choice == "1":
            interactive_mode()
        elif choice == "2":
            batch_demo()
        elif choice == "3":
            mod_setup_mode()
        elif choice == "4":
            production_package_mode()
        elif choice == "5":
            import_csv_mode()
        elif choice == "6":
            calendar_mode()
        elif choice == "7":
            print("Thoát.")
            break
        else:
            print("Lựa chọn không hợp lệ. Hãy chọn từ 1 đến 7.")

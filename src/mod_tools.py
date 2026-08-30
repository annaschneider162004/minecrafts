from __future__ import annotations

from src.models import ModSetupPlan, ToolItem


def build_mod_setup_plan() -> ModSetupPlan:
    tools = [
        ToolItem(
            name="Minecraft Java Edition",
            category="Game",
            required=True,
            purpose="Chạy thế giới build, cài mod, shader, resource pack và quay video.",
            notes="Nên dùng một profile riêng cho sản xuất video để tránh lỗi mod.",
        ),
        ToolItem(
            name="Fabric Loader",
            category="Mod loader",
            required=True,
            purpose="Chạy các mod client-side phổ biến như Replay Mod và Litematica.",
            notes="Dễ dùng cho setup quay cinematic. Có thể đổi sang Forge nếu mod bạn cần chỉ có Forge.",
        ),
        ToolItem(
            name="WorldEdit",
            category="Build tool",
            required=False,
            purpose="Xây nhanh bằng lệnh: fill, replace, copy, paste, sphere, cylinder, walls.",
            notes="Rất tốt để tạo nền, tường, terraforming và duplicate chi tiết lặp lại.",
        ),
        ToolItem(
            name="Axiom",
            category="Build tool",
            required=False,
            purpose="Chỉnh sửa world trực quan, build nhanh, tạo shape lớn, polish cảnh quay.",
            notes="Phù hợp với video timelapse/cinematic vì thao tác trực quan hơn nhiều lệnh.",
        ),
        ToolItem(
            name="Litematica",
            category="Blueprint/Schematic",
            required=False,
            purpose="Hiện blueprint/schematic trong game để dựng build chính xác từng block.",
            notes="Thường cần MaLiLib đi kèm. Hữu ích nếu bạn thiết kế build trước rồi quay quá trình dựng.",
        ),
        ToolItem(
            name="MaLiLib",
            category="Dependency",
            required=False,
            purpose="Thư viện phụ thuộc cho Litematica và một số mod Masa khác.",
            notes="Cài cùng version Minecraft/mod loader với Litematica.",
        ),
        ToolItem(
            name="Replay Mod",
            category="Recording mod",
            required=True,
            purpose="Mod tự ghi lại gameplay/replay để sau đó đặt camera cinematic, timelapse, orbit shot, reveal shot.",
            notes="Đây là mod quan trọng nhất cho kênh Minecraft build vì giúp quay lại cảnh đẹp sau khi build xong.",
        ),
        ToolItem(
            name="OBS Studio",
            category="Screen/audio recording",
            required=False,
            purpose="Quay màn hình, thu voice, quay phần UI/prompt AI, hoặc backup khi Replay Mod không đủ.",
            notes="Không phải mod Minecraft, nhưng nên dùng để thu intro, voice hoặc thao tác ngoài game.",
        ),
        ToolItem(
            name="Iris + Sodium",
            category="Performance/Shaders",
            required=False,
            purpose="Tăng FPS và bật shader để cảnh cinematic đẹp hơn.",
            notes="Kiểm tra tương thích với version Minecraft và các mod còn lại.",
        ),
        ToolItem(
            name="Chunky",
            category="Thumbnail/Render",
            required=False,
            purpose="Render ảnh build đẹp để làm thumbnail hoặc showcase.",
            notes="Dùng sau khi build xong để tạo ảnh chất lượng cao.",
        ),
    ]

    install_steps = [
        "Cài Minecraft Java Edition và tạo một profile riêng tên `YouTube Build Recording`.",
        "Chọn một phiên bản Minecraft ổn định mà các mod bạn cần đều hỗ trợ.",
        "Cài Fabric Loader cho đúng phiên bản Minecraft đã chọn.",
        "Tải và đặt các file mod vào thư mục `.minecraft/mods`: Replay Mod, Litematica, MaLiLib, WorldEdit, Axiom, Sodium/Iris nếu dùng shader.",
        "Mở game một lần để kiểm tra không crash trước khi quay video thật.",
        "Tạo một world test riêng để kiểm tra WorldEdit, Axiom, Litematica và Replay Mod.",
        "Tạo thư mục dự án cho từng video: `footage/`, `replay/`, `screenshots/`, `voice/`, `edit/`, `export/`.",
        "Trước khi build thật, bật Replay Mod recording và quay thêm OBS nếu cần thu UI/voice.",
    ]

    recording_workflow = [
        "Mở world trống hoặc world survival/build đã chuẩn bị.",
        "Bật Replay Mod recording trước khi bắt đầu build.",
        "Dùng WorldEdit hoặc Axiom để tạo foundation, terrain, walls và shape lớn.",
        "Dùng Litematica nếu bạn có schematic/blueprint cần dựng chính xác.",
        "Trong lúc build, tạo vài khoảnh khắc rõ ràng: before, foundation, walls, roof, interior, secret room, final reveal.",
        "Sau khi build xong, mở replay và tạo camera path: front reveal, orbit shot, top-down shot, interior walkthrough, before/after.",
        "Render các đoạn cinematic/timelapse từ Replay Mod.",
        "Dùng OBS để quay phần intro, AI prompt, hoặc cảnh bạn giải thích nếu cần.",
        "Đưa footage vào CapCut/DaVinci Resolve: cắt nhanh, thêm voice, captions, zoom, nhạc và sound effects.",
        "Chụp ảnh final build hoặc render bằng Chunky để làm thumbnail.",
    ]

    folder_structure = [
        "video-projects/",
        "  minecraft-build-keyword/",
        "    01-ai-prompt/",
        "    02-world-files/",
        "    03-replay-files/",
        "    04-obs-footage/",
        "    05-screenshots/",
        "    06-voiceover/",
        "    07-edit-project/",
        "    08-thumbnail/",
        "    09-final-export/",
    ]

    safety_notes = [
        "Chỉ tải mod từ nguồn chính thức/đáng tin cậy như trang mod chính thức hoặc Modrinth/CurseForge.",
        "Không tải file `.jar` từ link lạ trong comment YouTube/Discord.",
        "Luôn kiểm tra mod đúng phiên bản Minecraft và đúng mod loader.",
        "Backup world trước khi dùng WorldEdit/Axiom để tránh phá hỏng build.",
        "Không dùng schematic/build của người khác trong video kiếm tiền nếu không có quyền hoặc không biến đổi đủ nhiều.",
        "Nếu nội dung dùng AI, hãy thêm giá trị gốc: gameplay tự quay, build tự làm, voice/script riêng và editing riêng.",
    ]

    return ModSetupPlan(
        minecraft_edition="Minecraft Java Edition",
        mod_loader="Fabric Loader",
        recommended_tools=tools,
        install_steps=install_steps,
        recording_workflow=recording_workflow,
        folder_structure=folder_structure,
        safety_notes=safety_notes,
    )

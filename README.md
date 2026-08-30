# Minecraft YouTube Keyword & Video Production Kit

Tool Python CLI giúp lập kế hoạch và chuẩn bị sản xuất video YouTube cho ngách **Minecraft Build**, đặc biệt là hướng:

```text
Minecraft Build + AI + Tutorial + Timelapse + Replay Mod cinematic
```

Tool phù hợp khi bạn lấy dữ liệu keyword từ vidIQ, ví dụ:

- Keyword: `minecraft build`
- Search volume/tháng: `309968`
- Competition: `39.9`

## Tool làm được gì?

### 1. Keyword/video planning

Khi nhập keyword + volume + competition, tool tự tạo:

- Điểm cơ hội keyword
- Mức cạnh tranh: Low / Medium / High
- Mức ưu tiên: Low / Medium / High / Very High
- Loại build phù hợp
- Format video phù hợp
- 10 tiêu đề YouTube đề xuất
- Prompt để dùng với ChatGPT/AI tạo concept build
- Description YouTube
- Tags
- Text thumbnail
- Shot list để quay bằng Replay Mod
- Checklist dựng video
- Ý tưởng Shorts
- Outline kịch bản video
- File CSV tổng hợp
- File Markdown kế hoạch chi tiết cho từng keyword

### 2. Video Production Kit

Chức năng nâng cấp tạo full package cho một video:

```text
output/videos/<keyword-slug>/
├── 01_keyword_summary.md
├── 02_ai_build_prompt.md
├── 03_full_script.txt
├── 04_recording_timeline.md
├── 05_thumbnail_prompt.md
├── 06_upload_metadata.txt
├── 07_shorts_plan.md
├── 08_production_checklist.md
└── README.md
```

Package này giúp bạn đi từ keyword đến gần như toàn bộ bộ tài liệu sản xuất video.

### 3. Minecraft mod/tool setup

Tool có chức năng tạo setup cho workflow sản xuất video bằng:

- **Minecraft Java Edition**
- **WorldEdit**
- **Axiom**
- **Litematica**
- **MaLiLib**
- **Replay Mod** - mod tự ghi replay để quay timelapse/cinematic
- **OBS Studio**
- **Iris + Sodium**
- **Chunky**

### 4. Import CSV từ vidIQ

Bạn có thể nhập CSV có cột:

```csv
keyword,volume,competition
minecraft build,309968,39.9
```

Tool sẽ tạo plan hàng loạt, sort theo opportunity score, và có thể tạo full production package cho từng keyword.

### 5. Lịch đăng 30 ngày

Tool có thể tạo file:

```text
output/30_day_content_calendar.md
```

Lịch gồm video dài và Shorts từ các keyword Minecraft mẫu.

## Yêu cầu

Chỉ cần Python 3.10+.

Tool dùng **Python standard library**, không cần API key, không cần cài package ngoài.

## Cách chạy

```bash
python minecraft_youtube_tool.py
```

Menu hiện tại:

```text
1. Tạo video plan từ keyword vidIQ
2. Chạy demo 10 keyword Minecraft
3. Tạo setup WorldEdit/Axiom/Litematica/Replay Mod
4. Tạo FULL Video Production Kit cho 1 keyword
5. Import CSV keyword từ vidIQ
6. Tạo lịch đăng 30 ngày
7. Thoát
```

## Ví dụ nhanh với keyword `minecraft build`

Chọn chức năng `4`, sau đó nhập:

```text
Nhập keyword: minecraft build
Nhập search volume/tháng từ vidIQ: 309968
Nhập competition từ vidIQ: 39.9
```

Tool sẽ tạo full package tại:

```text
output/videos/minecraft-build/
```

Trong đó có:

- `03_full_script.txt` để đọc voiceover
- `04_recording_timeline.md` để quay footage
- `05_thumbnail_prompt.md` để làm thumbnail
- `06_upload_metadata.txt` để upload YouTube
- `07_shorts_plan.md` để cắt Shorts
- `08_production_checklist.md` để kiểm tra tiến độ

## Import CSV

Có file mẫu:

```text
examples/vidiq_import_template.csv
```

Chạy tool, chọn `5`, nhập:

```text
examples/vidiq_import_template.csv
```

Nếu muốn tạo full package cho từng keyword, nhập:

```text
y
```

## Công thức Opportunity Score

Tool dùng công thức đơn giản:

```text
Opportunity Score = Volume Score - Competition + 30
```

Trong đó `Volume Score` được quy đổi theo search volume/tháng:

| Volume/tháng | Volume Score |
|---:|---:|
| >= 300,000 | 100 |
| >= 100,000 | 90 |
| >= 50,000 | 80 |
| >= 20,000 | 70 |
| >= 10,000 | 60 |
| >= 5,000 | 50 |
| >= 1,000 | 35 |
| >= 500 | 25 |
| < 500 | 15 |

Ví dụ:

```text
minecraft build
Volume = 309,968
Competition = 39.9
Volume Score = 100
Opportunity Score = 100 - 39.9 + 30 = 90.1
```

=> Đây là keyword ưu tiên rất cao.

## Workflow làm video Minecraft Build

### Bước 1: Chọn keyword

Ví dụ:

```text
minecraft survival base build
minecraft build
minecraft starter house build
minecraft secret base build
ai minecraft build
```

### Bước 2: Nhập số từ vidIQ vào tool

Lấy:

- Search volume
- Competition

Sau đó chạy tool để tạo video plan hoặc full production package.

### Bước 3: Dùng AI tạo concept

Copy phần `02_ai_build_prompt.md` trong package và đưa vào ChatGPT hoặc AI bạn dùng.

### Bước 4: Xây trong Minecraft

Setup khuyên dùng:

- Minecraft Java Edition
- Fabric Loader
- WorldEdit
- Axiom
- Litematica + MaLiLib

Công dụng:

- **WorldEdit**: tạo nền, tường, copy/paste, replace block, terraform nhanh.
- **Axiom**: chỉnh world trực quan, rất hợp build cinematic.
- **Litematica**: hiện blueprint/schematic để dựng build chính xác.

### Bước 5: Tự quay video / cinematic

Dùng:

- **Replay Mod**: mod tự ghi replay trong Minecraft để sau đó đặt camera path, quay timelapse, orbit shot, reveal shot.
- **OBS Studio**: quay intro, voice, màn hình, thao tác với AI prompt hoặc backup footage.

Workflow:

```text
1. Bật Replay Mod recording trước khi build.
2. Xây bằng WorldEdit/Axiom/Litematica.
3. Mở replay sau khi build xong.
4. Tạo camera path: front reveal, orbit shot, top-down shot, interior tour.
5. Render clip cinematic/timelapse.
6. Dựng video trong CapCut hoặc DaVinci Resolve.
```

### Bước 6: Thumbnail

Dùng một trong các cách:

- Screenshot trong game
- Replay Mod cinematic frame
- Chunky render
- Canva/Photopea/Photoshop để thêm text

Text thumbnail gợi ý:

```text
AI BUILT THIS?
SECRET BASE!
EASY BUILD!
INSANE BUILD!
```

### Bước 7: Upload YouTube

Copy từ package:

- Title
- Description
- Tags
- Thumbnail text
- Pinned comment

## Chiến lược kênh đề xuất

Nên xây kênh theo concept:

```text
AI Minecraft Builder
```

Nội dung chính:

1. Minecraft build tutorial
2. Minecraft build ideas
3. AI Minecraft build challenge
4. Minecraft timelapse bằng Replay Mod
5. Minecraft horror/secret base build

Lịch đăng gợi ý:

```text
2 video dài/tuần: tutorial hoặc build ideas
1 video dài/tuần: AI build challenge
5-7 Shorts/tuần: timelapse, before/after, secret room, final reveal
```

## Cấu trúc project

```text
minecrafts/
├── minecraft_youtube_tool.py
├── README.md
├── examples/
│   ├── sample_keywords.csv
│   └── vidiq_import_template.csv
└── src/
    ├── __init__.py
    ├── cli.py
    ├── csv_importer.py
    ├── exporters.py
    ├── generators.py
    ├── mod_tools.py
    ├── models.py
    ├── production_kit.py
    └── scoring.py
```

## Lưu ý

- Dữ liệu volume/competition nên lấy từ vidIQ hoặc công cụ keyword bạn tin tưởng.
- Tool không scrape vidIQ và không cần đăng nhập.
- Đây là tool planning/sản xuất tài liệu; nó chưa tự điều khiển Minecraft hoặc tự dựng video hoàn chỉnh.
- Chỉ tải mod từ nguồn chính thức/đáng tin cậy.
- Backup world trước khi dùng WorldEdit/Axiom.

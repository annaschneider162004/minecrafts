# Minecraft YouTube Keyword & Video Planner

Tool Python CLI giúp lập kế hoạch video YouTube cho ngách **Minecraft Build**, đặc biệt là hướng:

```text
Minecraft Build + AI + Tutorial + Timelapse + Replay Mod cinematic
```

Tool này phù hợp nếu bạn đang lấy dữ liệu keyword từ vidIQ, ví dụ:

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

### 2. Minecraft mod/tool setup

Tool có thêm chức năng tạo setup cho workflow sản xuất video bằng:

- **Minecraft Java Edition**
- **WorldEdit**
- **Axiom**
- **Litematica**
- **MaLiLib**
- **Replay Mod** - mod tự ghi replay để quay timelapse/cinematic
- **OBS Studio**
- **Iris + Sodium**
- **Chunky**

## Yêu cầu

Chỉ cần Python 3.10+.

Tool dùng **Python standard library**, không cần API key, không cần cài package ngoài.

## Cách chạy

```bash
python minecraft_youtube_tool.py
```

Sau khi chạy, bạn sẽ thấy menu:

```text
1. Tạo video plan từ keyword vidIQ
2. Chạy demo 10 keyword Minecraft
3. Tạo setup WorldEdit/Axiom/Litematica/Replay Mod
4. Thoát
```

## Ví dụ với keyword `minecraft build`

Chọn chức năng `1`, sau đó nhập:

```text
Nhập keyword: minecraft build
Nhập search volume/tháng từ vidIQ: 309968
Nhập competition từ vidIQ: 39.9
```

Tool sẽ tính gần như:

```text
Keyword: minecraft build
Volume/month: 309968
Competition: 39.9/100 - Medium
Opportunity Score: 90.1/100
Priority: Very High
Build Type: survival base
Video Format: tutorial
```

## File xuất ra

Tool tự tạo thư mục `output/` và xuất:

```text
output/minecraft_keywords.csv
output/minecraft-build_video_plan.md
output/minecraft_mod_recording_setup.md
```

Trong file Markdown video plan sẽ có:

- Recommended Titles
- Recommended Production Tools
- AI Build Prompt
- Description
- Tags
- Thumbnail Text Ideas
- Shot List
- Editing Checklist
- Shorts Ideas
- Script Outline

Trong file setup mod sẽ có:

- Danh sách tool/mod nên dùng
- Các bước cài đặt
- Workflow quay video bằng Replay Mod
- Cấu trúc thư mục sản xuất video
- Lưu ý an toàn khi dùng mod/schematic

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

Sau đó chạy tool để tạo video plan.

### Bước 3: Dùng AI tạo concept

Copy phần `AI Build Prompt` trong file Markdown và đưa vào ChatGPT hoặc AI bạn dùng.

Ví dụ prompt được tool tạo:

```text
Design a Minecraft survival base for a YouTube video targeting the keyword: "minecraft build".

Requirements:
- Style: visually impressive but buildable in survival mode
- Include: storage room, bedroom, crafting area, furnace area, farm, enchanting room, and secret room
- Use mostly obtainable blocks
- Make the build look good from the front for thumbnail
- Suggest where WorldEdit, Axiom, and Litematica can speed up the build
- Suggest Replay Mod camera shots for the final reveal
```

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

Copy từ file Markdown:

- Title
- Description
- Tags
- Thumbnail text

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

## Demo batch

Chọn chức năng `2` để tạo kế hoạch mẫu cho 10 keyword:

- `minecraft build`
- `minecraft survival base build`
- `minecraft starter house build`
- `minecraft build tutorial`
- `easy minecraft build`
- `minecraft secret base build`
- `ai minecraft build`
- `chatgpt minecraft build`
- `minecraft but ai builds my house`
- `minecraft horror build`

## Cấu trúc project

```text
minecrafts/
├── minecraft_youtube_tool.py
├── README.md
├── examples/
│   └── sample_keywords.csv
└── src/
    ├── __init__.py
    ├── cli.py
    ├── exporters.py
    ├── generators.py
    ├── mod_tools.py
    ├── models.py
    └── scoring.py
```

## Lưu ý

- Dữ liệu volume/competition nên lấy từ vidIQ hoặc công cụ keyword bạn tin tưởng.
- Tool không scrape vidIQ và không cần đăng nhập.
- Đây là bản MVP offline. Có thể nâng cấp sau để import CSV từ vidIQ hoặc kết nối YouTube Data API.
- Chỉ tải mod từ nguồn chính thức/đáng tin cậy.
- Backup world trước khi dùng WorldEdit/Axiom.

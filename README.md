# Biometric Geo-Visualization with Spectrograms

> An interactive Mapbox-based demo connecting timestamped GPS records with
> physiological measurements, event annotations, street images, and audio spectrograms.

**Live demo:** https://jiakun323.github.io/geodata-visualization/  
**Repository:** https://github.com/jiakun323/geodata-visualization

---

## 中文说明

### 项目内容

本项目使用地图上的 3D 柱体呈现连续采集的生理数据。使用者可以：

- 在 22 个生理指标之间切换；
- 通过柱体高度和颜色比较不同记录；
- 点击柱体查看时间、坐标、事件和精确数值；
- 查看时间戳对应的街景图片；
- 查看时间戳对应的音频频谱图；
- 查看哪些数据字段经过插值处理。

当前 GeoJSON 包含 **349 条记录**。

### 仓库结构

```text
.
├── index.html
├── config.js
├── config.example.js
├── data/
│   └── biometric_multi_metric_with_spectrogram.geojson
├── extracted_frames/
│   ├── README.md
│   └── YYYY-MM-DD_HH-MM-SS.jpg
├── spectrogram/
│   ├── README.md
│   └── YYYY-MM-DD_HH-MM-SS.png
├── scripts/
│   └── validate_data.py
├── PRIVACY_CHECKLIST.md
├── LICENSE
├── .nojekyll
└── README.md
```

### 更新现有 GitHub 仓库

1. 解压本压缩包。
2. 进入解压后的 `geodata-visualization-github-ready` 文件夹。
3. 将其中的文件和文件夹上传到仓库根目录：
   `https://github.com/jiakun323/geodata-visualization`
4. 选择覆盖旧的 `index.html`、`config.js`、`README.md` 和 `data/` 数据文件。
5. 上传对应的街景图片到 `extracted_frames/`。
6. 上传对应的频谱图到 `spectrogram/`。
7. 提交到 `main` 分支。

你的 GitHub Pages 已设置为从 `main / (root)` 发布，因此提交后会自动重新部署：

```text
https://jiakun323.github.io/geodata-visualization/
```

### 重要：不要直接上传 ZIP

GitHub Pages 不会自动解压 ZIP。请先在电脑上解压，然后把压缩包内部的文件上传到仓库根目录。仓库首页应直接看到：

```text
index.html
config.js
README.md
data/
extracted_frames/
spectrogram/
```

### 媒体路径

街景图片：

```text
extracted_frames/2026-07-17_12-56-16.jpg
```

频谱图：

```text
spectrogram/2026-07-17_12-56-16.png
```

路径和文件名必须与 GeoJSON 完全一致。GitHub Pages 区分大小写。

本压缩包没有包含实际的 JPG 和 PNG 媒体文件，因为本轮只收到 HTML 和 GeoJSON。
缺少媒体时地图仍可运行，信息面板会显示未找到对应图片或频谱图。

### 数据规范化

本版本完成了以下整理：

- 将 `familarity` 规范为 `familiarity`；
- 为每条记录加入稳定的 `record_id`；
- 保留最新 spectrogram 路径；
- 将 GeoJSON 统一放到 `data/`；
- 将所有资源路径改为仓库相对路径；
- 增加数据加载提示和错误提示；
- 自动根据路线范围调整地图视角；
- 增加缓存更新参数，减少 GitHub Pages 显示旧数据的问题；
- 增加插值字段说明；
- 增加媒体文件路径校验脚本。

### 本地预览

不要直接双击 `index.html`。请在仓库目录中运行：

```bash
python -m http.server 8000
```

打开：

```text
http://localhost:8000/
```

### 数据检查

仅检查 GeoJSON：

```bash
python scripts/validate_data.py
```

同时严格检查图片和频谱图是否齐全：

```bash
python scripts/validate_data.py --strict-assets
```

### Mapbox Token

`config.js` 使用浏览器端 Mapbox public token。公开网页必须在客户端读取 public token，
但建议在 Mapbox 后台将 token 限制到：

```text
https://jiakun323.github.io/geodata-visualization/*
```

不要把带 secret scopes 的 token 上传到公开仓库。

### 隐私

该数据可能包含精确坐标、时间戳、生理数据和可识别图片。
公开发布前请查看 [`PRIVACY_CHECKLIST.md`](PRIVACY_CHECKLIST.md)。

---

## English overview

This static GitHub Pages demo visualizes timestamped biometric data as interactive
3D map pillars. Users can switch physiological metrics and inspect a selected
record's exact value, event annotation, street image, spectrogram, timestamp,
coordinate, and interpolation note.

### Local preview

```bash
python -m http.server 8000
```

Open `http://localhost:8000/`.

### Validate

```bash
python scripts/validate_data.py
python scripts/validate_data.py --strict-assets
```

### Deployment

The repository is intended for GitHub Pages using the `main` branch and repository
root. Every commit to `main` triggers a new Pages deployment.

## License

Code is released under the MIT License. Data and media may require separate
permissions from their owners or research participants.

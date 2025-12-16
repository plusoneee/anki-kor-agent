# AnkiKor Dashboard - Bauhaus Design

Bauhaus 風格的韓語學習管理儀表板，用於追蹤和管理 Anki 學習進度。

## 設計原則

本專案遵循 Bauhaus (包浩斯) 設計原則：

- **不對稱但平衡的網格**: 使用非對稱的版面配置，但保持視覺平衡
- **三原色**: 紅色 (#e63946)、黃色 (#ffd60a)、藍色 (#0077b6)
- **黑白基調**: 黑色 (#1a1a1a) 和白色 (#f8f9fa)
- **幾何形狀**: 使用圓形和矩形作為核心視覺元素
- **功能性字體**: 乾淨的無襯線字體，強調功能性

## 功能特點 (Phase 1 - MVP)

### 1. 學習進度儀表板
- 覆蓋率視覺化圖表
- 目標單字清單選擇器
- 統計數據顯示

### 2. 連線狀態監控
- API 連線狀態
- Anki 連線狀態
- 即時狀態更新

### 3. 快速建立介面
- 單字卡片快速建立
- 聽力卡片快速建立
- 即時結果反饋

### 4. 已學單字列表
- 可搜尋的單字列表
- 顯示所有已學習的單字

### 5. 目標清單管理
- 查看所有可用的目標清單
- 檢查覆蓋率
- 顯示待學習單字

## 技術棧

- **React 19** - UI 框架
- **Vite** - 建置工具
- **Tailwind CSS v4** - 樣式框架
- **Recharts** - 圖表庫
- **Axios** - HTTP 客戶端

## 開發指令

### 安裝依賴
```bash
npm install
```

### 啟動開發伺服器
```bash
npm run dev
```

伺服器將運行在 `http://localhost:5173`

### 建置生產版本
```bash
npm run build
```

### 預覽生產建置
```bash
npm run preview
```

## 環境配置

創建 `.env` 檔案並設置以下變數：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 專案結構

```
frontend/
├── src/
│   ├── components/          # React 元件
│   │   ├── BauhausShapes.jsx      # Bauhaus 幾何形狀元件
│   │   ├── Navbar.jsx             # 導航列
│   │   ├── Dashboard.jsx          # 儀表板
│   │   ├── VocabQuickCreate.jsx   # 單字快速建立
│   │   ├── ListeningQuickCreate.jsx  # 聽力快速建立
│   │   ├── VocabList.jsx          # 單字列表
│   │   └── TargetListManager.jsx  # 目標清單管理
│   ├── hooks/               # 自定義 Hooks
│   │   └── useConnectionStatus.js # 連線狀態 Hook
│   ├── utils/               # 工具函數
│   │   └── api.js          # API 客戶端
│   ├── App.jsx             # 主應用元件
│   ├── index.css           # Bauhaus 設計系統樣式
│   └── main.jsx            # 應用入口點
├── public/                  # 靜態資源
├── .env                     # 環境變數
└── package.json            # 專案依賴
```

## 前置需求

在啟動前端之前，請確保：

1. 後端 API 正在運行 (`http://127.0.0.1:8000`)
2. Anki Connect 已安裝並運行 (`http://127.0.0.1:8765`)

## 瀏覽器支援

- Chrome/Edge (最新版本)
- Firefox (最新版本)
- Safari (最新版本)

## 貢獻

歡迎提交 Issue 和 Pull Request！

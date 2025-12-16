# AnkiKor Frontend

Modern glassmorphism web interface for Korean language learning, inspired by Arc Browser's translucent aesthetic.

## Design Philosophy

The interface adopts a glassmorphism design language focused on creating a calm, distraction-free learning environment:

- **Translucent Glass Surfaces**: Frosted-glass cards with backdrop blur effects
- **Subtle Gradient Background**: Rose-to-indigo gradient optimized for long study sessions
- **Minimalist Interaction**: Smooth animations with purposeful transitions (300-500ms)
- **Typography**: Inter for Latin characters, Noto Sans KR for Korean, optimized for readability
- **Accessibility**: ARIA attributes, semantic HTML, keyboard navigation support

## Features

### Learning Center (`/learning`)
- **Quick Create Forms**: Instant vocabulary and listening card creation
- **Collapsible Tips**: Contextual usage tips with persistent state
- **Dual-Column Layout**: Vocabulary and listening forms side by side

### Vocabulary Library (`/vocabulary`)
- **Vocabulary List**: Searchable list of learned words with real-time filtering
- **Coverage Visualization**: Interactive chart showing learning progress
- **Target List Management**: Track progress against custom word lists
- **Statistics Dashboard**: Total words, coverage percentage, and learning insights

### Global Features
- **Connection Status**: Real-time monitoring of API and Anki connectivity
- **Responsive Design**: Mobile-first approach with adaptive navigation
- **Persistent UI State**: LocalStorage integration for user preferences

## Technical Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS with custom glassmorphism tokens
- **React Router** - Client-side routing
- **Recharts** - Data visualization
- **Axios** - HTTP client

## Development

### Prerequisites

Before starting the frontend:
1. Backend API running at `http://127.0.0.1:8000`
2. Anki Connect installed and running at `http://127.0.0.1:8765`

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```
Server runs at `http://localhost:5173`

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Environment Configuration

Create a `.env` file with the following variables:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

See `.env.example` for reference.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── GlassComponents.jsx      # Reusable glassmorphism UI primitives
│   │   ├── Dashboard.jsx            # Coverage visualization widget
│   │   ├── VocabQuickCreate.jsx     # Vocabulary card creation form
│   │   ├── ListeningQuickCreate.jsx # Listening card creation form
│   │   ├── VocabList.jsx            # Learned vocabulary list
│   │   ├── TargetListManager.jsx    # Target list management
│   │   └── layout/
│   │       ├── Sidebar.jsx          # Desktop navigation sidebar
│   │       └── MobileTopBar.jsx     # Mobile navigation header
│   ├── pages/
│   │   ├── LearningCenterPage.jsx   # Quick create interface (/learning)
│   │   └── VocabularyLibraryPage.jsx # Library and coverage (/vocabulary)
│   ├── layouts/
│   │   └── MainLayout.jsx           # App shell with navigation
│   ├── contexts/
│   │   └── CoverageContext.jsx      # Coverage data state management
│   ├── hooks/
│   │   └── useConnectionStatus.js   # API/Anki connection monitoring
│   ├── routes/
│   │   └── index.jsx                # Route configuration
│   ├── utils/
│   │   └── api.js                   # Axios API client
│   ├── index.css                    # Glassmorphism design system
│   └── main.jsx                     # Application entry point
├── public/
│   └── vite.svg                     # Vite logo
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore patterns
├── tailwind.config.js               # Tailwind customization with glass tokens
├── postcss.config.js                # PostCSS configuration
├── vite.config.js                   # Vite configuration
├── eslint.config.js                 # ESLint configuration
├── package.json                     # Dependencies and scripts
└── package-lock.json                # Dependency lock file
```

## Design System

### Color Palette
- **Glass Rose**: `#fff1f2` → `#e11d48` (accents, listening cards)
- **Glass Indigo**: `#eef2ff` → `#4338ca` (accents, vocabulary cards)
- **Glass Lavender**: `#b8a9d4` (decorative elements)
- **Text Primary**: `#2d2d3a` (main content)
- **Text Secondary**: `#6b6b7b` (supporting text)

### Glassmorphism Components
All components use the `GlassCard`, `GlassButton`, `GlassInput` primitives with:
- `backdrop-filter: blur(16px)`
- Subtle borders with `rgba(255, 255, 255, 0.3)`
- Smooth hover transitions
- Shadow depth variations

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Notes

Frontend implementation generated with Claude Code. Includes responsive design patterns, accessibility features, and optimized user experience for extended learning sessions.

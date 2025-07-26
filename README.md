# SLAFAI - AI Engineering from Scratch

A modern, Next.js-based learning platform for AI engineering education.

## Features

- **20 Phases, 260+ Lessons**: Complete curriculum from math foundations to production AI
- **Dynamic Content Loading**: Lessons fetched directly from GitHub and rendered with markdown
- **Progress Tracking**: localStorage-based progress tracking
- **Orange/Dark Theme**: Beautiful dark theme with orange accents
- **Responsive Design**: Works on all devices

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + Custom CSS variables
- **Fonts**: Space Grotesk (headings) + Inter (body) + JetBrains Mono (code)
- **Icons**: Lucide React
- **Markdown**: react-markdown + remark-gfm

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── lessons/           # Dynamic lesson viewer
│   ├── ai/                 # AI chat page
│   ├── catalog/            # Lesson catalog
│   └── glossary/          # AI glossary
├── components/              # Reusable React components
├── data/                   # Phases and glossary data
└── lib/                    # Utility functions
```

## Content Source

This platform uses content from [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) by rohitg00, licensed under MIT.

## License

MIT License - See original repository for details.

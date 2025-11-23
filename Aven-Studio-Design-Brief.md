# Aven Studio: Self-Build Navigator
## Comprehensive Design Brief

**Version:** 1.0  
**Date:** November 2025  
**Status:** Planning & Design Phase

---

## 1. Project Overview

### What is Aven Studio?

Aven Studio is a project management platform designed specifically for UK self-builders. It helps people manage the complexity of building their own home by providing a calm, organised space to track budgets, timelines, tasks, materials, documents, and contacts.

### The Problem We're Solving

Building your own home in the UK is one of the most rewarding experiences you can have, but it's also incredibly complex. Self-builders face:

- Overwhelming amounts of information to track
- Multiple contractors and professionals to coordinate
- Planning regulations and building controls to navigate
- Budget pressures and cost management challenges
- Timeline dependencies that can derail the whole project

Most project management tools are either too corporate (designed for construction companies) or too simple (basic to-do lists). Self-builders need something that understands the unique nature of building a home.

### Our Solution

A thoughtfully designed platform that:

- Reduces cognitive load by keeping everything in one reliable place
- Guides users through the UK-specific planning and building process
- Provides structure without feeling rigid or corporate
- Feels calm and human, not technical or overwhelming
- Respects that users are managing one of the biggest projects of their lives

---

## 2. Brand Identity

### Brand Name

**AvenStudio** (styled as one word, or Aven Studio)

The name conveys:
- Professional studio/workspace connotation
- Clean, modern, memorable
- UK-appropriate (doesn't sound American or corporate)

### Brand Personality

**How we want users to feel:**

- **Reassured** — "You're not alone in this"
- **Capable** — "You can manage this"
- **Organised** — Everything has its place
- **Calm** — No overwhelm, no stress

**Tone of voice:**

- Warm, concise, confident
- Practical and grounded (no jargon)
- Gives reality checks when needed
- Uses plain English construction terms

**What we're NOT:**

- Corporate or "enterprise software"
- Techy or developer-focused
- Construction-industry specific
- Overly cheerful or patronising

### Brand Values

1. **Clarity over complexity** — Simplify without dumbing down
2. **Calm authority** — Confident but approachable
3. **Considered craft** — Every detail matters
4. **Honest partnership** — We support decisions, not make them
5. **UK-native** — Aligned with British planning language and constraints

---

## 3. Visual Design System

### Colour Palette

**Primary colours:**

- **Navy** (#304F5D) — Primary brand colour, replaces black throughout
  - Used for: Text, headers, buttons, primary UI elements
  - Evokes: Trust, stability, professionalism

- **Bronze** (#A57F62) — Accent colour
  - Used for: Logo accent, active states, links, highlights
  - Evokes: Warmth, craft, natural materials

**Secondary colours:**

- **Mint** (#98D0D3) — In-progress states, info backgrounds
- **Sand** (#EEE5DC) — Background colour, card surfaces
- **Plum** (#823755) — Blocked states, dependencies
- **Tangerine** (#F37045) — M&E tasks, energy items

**Semantic colours:**

- **Success** (#4A7C59) — Completed tasks, positive states
- **Warning** (#C17F24) — Due soon, high priority
- **Danger** (#9E3B3B) — Overdue, urgent, errors

**Key principle:** Colours should evoke materials and landscape (wood, stone, steel, clay) in a restrained, modern way.

### Typography

**Single typeface system:**

AvenStudio uses **DM Sans** exclusively throughout the entire application - both logo and interface. This creates a clean, consistent, modern feel.

**DM Sans characteristics:**
- Geometric sans-serif with slightly rounded terminals
- Friendly and approachable while maintaining professionalism
- Excellent readability at all sizes
- Clean enough for data-heavy interfaces
- Warm enough for a consumer-facing tool

**Weights used:**
- **Regular (400)** for body text, labels, general UI
- **Medium (500)** for headings, emphasis, navigation, the logo

**Accessibility option:**
- **Dyslexia-friendly toggle** available in settings
- When activated, switches to: **Lexend** or **OpenDyslexic**
- Alternatively: increases letter spacing on DM Sans

**Type scale:**
- Logo: 1.375rem (Medium 500)
- Page titles: 1.5rem (Medium 500)
- Section headings: 1.25rem (Medium 500)
- Body text: 0.9375rem (Regular 400)
- UI labels: 0.8125rem (Regular 400)
- Tags/captions: 0.75rem (Regular 400)
- Stats: 2.5rem (Medium 500)

### UI Style

**Layout principles:**

- Minimal ornamentation
- Soft, wide spacing (whitespace is not wasted space)
- Clear sections, consistent structure
- No clutter, no "dashboard overwhelm"
- Progressive disclosure (show complexity gradually)

**Component style:**

- Cards: White background, 8px radius, subtle borders
- Icons: Architectural line drawings (thin, geometric, calm)
- Buttons: Clear states, no heavy shadows
- Spacing: Generous, breathing room

**Responsive approach:**

- Mobile-first styling
- Breakpoints: 800px, 1000px, 1200px
- Timeline requires minimum 900px (horizontal scroll on mobile)

---

## 4. User Experience Principles

### Core UX Philosophy

1. **Clarity first** — Every screen answers "what can I do here?" and "why does this matter?"
2. **Consistency** — Single source of truth for spacing, typography, colour, controls
3. **Progressive disclosure** — Show only what's needed; hide advanced options until required
4. **Accessibility by default** — Keyboard navigation, ARIA labels, 4.5:1 contrast, semantic markup
5. **Predictable patterns** — Small set of reusable interactions (list, card, modal, drawer)
6. **Performance** — Fast loading, lazy load attachments, efficient queries

### Design Patterns

**Essential components:**

- Top bar / app shell (global search, navigation, user menu)
- Collapsible sidebar (projects, filters, quick create)
- View switcher (Dashboard / Tasks / Timeline / Calendar / Budget / etc.)
- Task cards (compact and expanded detail drawer)
- Modals (settings, confirmations, create/edit forms)
- Toasts (non-blocking success/error messages)
- Empty states (teach users what to do next)

**Interaction patterns:**

- Inline editing (quick changes without opening drawers)
- Drag and drop (with keyboard alternative)
- Bulk actions (select multiple for batch operations)
- Filtering and saved views
- Version history for documents
- Audit trail for changes

---

## 5. Target Audience

### Primary Users

UK-based individuals and couples undertaking:
- Self-build projects
- Custom-build projects
- Significant home renovations

**Experience range:**

- First-time self-builders (need guidance and structure)
- Experienced DIY enthusiasts (value efficiency)
- Occasional professional developers (need professional-grade tools)

**Characteristics:**

- Detail-oriented and research-driven
- Appreciate quality design
- Investing significant time, money, and emotional energy
- Don't want cheap-feeling software
- Don't want unnecessary complexity
- Managing stress and cognitive load

**What unites them:**

They're building a home, not running a construction company.

---

## 6. Feature Set & User Stories

### Planning & Early Concept

**As a self-builder, I want to:**

- Capture early ideas and shape them into a clear brief
- Understand planning constraints (conservation areas, permitted development)
- Record building regulations requirements
- Get gentle guidance without feeling patronised
- Explore ideas before speaking to professionals

### Budget & Financial Management

**As a user, I want to:**

- Set an overall budget and break it into categories
- Record and compare quotes from contractors
- Track actual spend vs estimates
- Get alerts when costs exceed budget
- See automatic variance calculations
- Understand where my money is going

### Timeline & Phase Management

**As a user, I want to:**

- Visualise the build timeline in phases
- Understand the sequence of construction (groundworks → structure → first fix, etc.)
- Track dependencies (roof must finish before windows)
- Get reminders for key dates
- See how delays impact the rest of the project
- Adjust timelines when things change

### Tasks & To-Dos

**As a user, I want to:**

- See all tasks in one organised place
- Group tasks by phase so I can focus on what matters now
- Assign tasks to contractors or family members
- Set reminders and due dates
- Mark tasks as blocked when dependencies exist
- Archive completed tasks cleanly

### Materials & Procurement

**As a user, I want to:**

- Maintain a list of materials with quantities and costs
- Track supplier contacts and lead times
- Schedule deliveries to align with the timeline
- Get alerts for overdue deliveries
- Store warranties and specifications
- Avoid reordering or under-ordering

### Documents & Specifications

**As a user, I want to:**

- Store all drawings, approvals, and certificates in one place
- Maintain version history (know which drawing is current)
- Link documents to specific phases or tasks
- Filter by type (planning, building regs, certificates)
- Access documents easily from site (mobile-friendly)
- Never lose track of important paperwork

### Contacts & Contractors

**As a user, I want to:**

- Keep all professionals in a centralised directory
- Log meetings, site visits, and decisions
- Store contracts, insurance, and certificates
- Track contractor performance
- Link contacts to relevant tasks

### Dashboard & Insights

**As a user, I want to:**

- See project health at a glance
- Know what needs attention today
- Track overall progress
- Get alerts for risks, delays, or overruns
- Feel in control, not overwhelmed

### Reporting & Exporting

**As a user, I want to:**

- Generate simple reports (budget, timeline, tasks)
- Share updates with family, lenders, or contractors
- Export to PDF for inspections or meetings
- Create document bundles when needed

---

## 7. Information Architecture

### Main Sections

#### Dashboard (Home)
- Project progress overview
- Stats cards (total tasks, in progress, completed, blocked)
- High priority tasks
- Upcoming due dates
- Quick links to key sections

#### Planning & Brief
- Brief builder (guided questions)
- Room-by-room requirements
- Planning constraints
- Building regulations notes
- Priority tagging (must-have / nice-to-have)

#### Tasks
- List view (sortable, filterable)
- Kanban board (drag and drop between statuses)
- Calendar view (tasks on due dates)
- Timeline/Gantt view (duration bars)
- Task detail drawer (full metadata, comments, attachments)

#### Budget
- Category breakdown
- Line items (cost, actual, variance)
- Quote comparison
- Alerts for overspend
- Cashflow by phase

#### Timeline
- Gantt-style chart
- Pre-set UK construction phases
- Milestone tracking
- Dependency indicators
- Delay impact calculations

#### Materials
- Materials list (item, quantity, cost, supplier)
- Lead time tracking
- Delivery scheduling
- Warranty storage

#### Documents
- Upload, tag, categorise
- Version history
- Link to phases/tasks
- Filter by type
- Mobile-friendly viewer

#### Contacts
- Contact profiles (builders, architects, engineers)
- Notes log (timestamped)
- Contracts and certificates
- Performance tracking

#### Reports
- Budget reports
- Timeline summaries
- Task lists
- Document bundles
- PDF exports

#### Settings
- Project preferences
- Storage location
- Interface complexity (simple/advanced)
- Notifications and reminders
- Theme switcher
- Export/import data

---

## 8. Technical Approach

### Technology Stack Decision

After careful consideration of React, Django, and Electron options, **the decision is made:**

**Desktop application using Electron + Python backend**

This gives us:
- ✅ Click-to-run desktop app (exe for Windows, .app for macOS)
- ✅ Fully offline-first with SQLite
- ✅ Professional desktop experience
- ✅ No server needed - everything runs locally
- ✅ Python for business logic (your preferred language)
- ✅ Modern UI capabilities when needed

### Architecture

**Frontend (Electron):**
- HTML, CSS for structure and styling
- Vanilla JavaScript for interactions (progressive enhancement)
- Electron wraps everything into a native desktop app
- Clean, fast, no heavy framework overhead

**Backend (Python):**
- FastAPI or simple Python server running locally
- Handles all business logic
- Communicates with SQLite database
- Runs automatically when app launches (users never see it)

**Data Layer:**
- **SQLite** - single file database
- Stored locally on user's machine
- Portable (can be backed up, moved, synced)
- No cloud dependency
- Fast, reliable, proven technology

### Why This Stack Works for AvenStudio

**For users:**
- Double-click icon to launch
- Everything works offline
- Data stays on their machine (privacy)
- Fast and responsive
- Familiar desktop app experience

**For you (developer):**
- Python for all logic (clean, readable, your preference)
- No JavaScript framework complexity
- Clear separation: UI (Electron) / Logic (Python) / Data (SQLite)
- Can bundle everything into single installer
- Cross-platform (Windows, macOS, Linux)

**For the project:**
- Professional feel from day one
- Can add features incrementally
- Future cloud sync option possible
- Easy to maintain
- Good performance

### Development Approach

**Phase 1: Core functionality**
- Set up Electron shell
- Python FastAPI backend
- SQLite database setup
- Basic UI (Dashboard, Tasks)
- Data flows working end-to-end

**Phase 2: Essential features**
- Full CRUD for all entities
- File handling (documents, attachments)
- Basic reporting
- Settings and preferences

**Phase 3: Polish & distribution**
- Packaging for Windows (.exe)
- Packaging for macOS (.app, .dmg)
- Auto-updater
- Installation experience
- User testing and refinement

### Technical Structure

```
aven-studio/
├── electron/                 # Electron main process
│   ├── main.js              # App entry point
│   └── preload.js           # Bridge to renderer
├── ui/                      # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── styles/
│   │   ├── tokens.css       # Design system variables
│   │   └── components.css
│   └── scripts/
│       └── app.js
├── backend/                 # Python FastAPI
│   ├── main.py              # API server
│   ├── models.py            # Database models
│   ├── database.py          # SQLite connection
│   └── routes/
│       ├── tasks.py
│       ├── budget.py
│       └── documents.py
├── data/                    # SQLite database location
│   └── aven.db
└── package.json             # Electron configuration
```

### Database Schema (Core Tables)

**projects**
- id, name, location, start_date, status, created_at

**tasks**
- id, project_id, title, description, status, priority, assignee_id
- due_date, start_date, completion_percent, blocked_by
- phase, created_at, updated_at

**budget_items**
- id, project_id, category, item_name, estimated_cost, actual_cost
- supplier, quote_date, variance

**documents**
- id, project_id, filename, file_path, document_type, version
- linked_task_id, linked_phase, upload_date

**contacts**
- id, project_id, name, role, company, email, phone
- notes, contracts

**milestones**
- id, project_id, name, target_date, actual_date, status, phase

**materials**
- id, project_id, item_name, quantity, unit, supplier_id
- cost, lead_time_days, delivery_date, status

### Packaging & Distribution

**Windows:**
- electron-builder creates .exe installer
- Includes Python runtime
- Single-click installation
- Shortcuts created automatically

**macOS:**
- electron-builder creates .app bundle
- Includes Python runtime  
- Optional .dmg for distribution
- Code signing for security

**File locations:**
- Windows: `C:\Users\[username]\AppData\Roaming\AvenStudio`
- macOS: `~/Library/Application Support/AvenStudio`
- Database, documents, preferences stored here

### Offline-First Strategy

**Everything works offline:**
- No internet required
- No account sign-up
- No cloud dependency
- Data privacy guaranteed

**Future cloud sync (optional):**
- User chooses to enable
- Encrypted backup to cloud storage
- Sync across multiple devices
- Still works offline-first

### Accessibility Requirements

**Keyboard navigation:**
- All interactions accessible via keyboard
- Focus indicators clearly visible
- Logical tab order

**Screen readers:**
- Semantic HTML
- ARIA labels where needed
- Alt text for images

**Visual:**
- 4.5:1 contrast ratio minimum
- Dyslexia-friendly font option
- High contrast mode
- Reduced motion option

**Inclusive design:**
- Clear labels and instructions
- Consistent layout and patterns
- Progressive disclosure (don't overwhelm)
- Plain language (avoid jargon)

---

## 9. Development Phases

### Phase 1: Foundation (MVP)

**Focus:** Core task and budget management

**Deliverables:**
- Onboarding flow
- Minimal dashboard
- Task creation and management
- Basic budget tracking
- Simple timeline view

**Goal:** Get something usable quickly

### Phase 2: Structure

**Focus:** Enhanced organisation

**Deliverables:**
- Milestones and phases
- Document upload and tagging
- Contact management
- Budget categories and variance
- Enhanced dashboard

**Goal:** Make it properly useful

### Phase 3: Polish

**Focus:** Advanced features and refinement

**Deliverables:**
- Progressive disclosure system
- Advanced filtering and saved views
- Bulk actions
- Reporting and exports
- Integration possibilities

**Goal:** Professional-grade tool

### Phase 4: Intelligence (Future)

**Focus:** AI assistance and automation

**Deliverables:**
- AI workbook (planning assistance)
- Smart suggestions
- Automated reminders
- Risk detection
- Reference database (building regs, etc.)

**Goal:** Intelligent partner

---

## 10. UI Specifications

### Layout Structure

**Sidebar (Collapsible):**
- Expanded: 260px width
- Collapsed: 72px width
- Fixed position, full height
- Sections: Navigation, Quick stats, Collapse toggle

**Main content:**
- Flex layout, fills remaining space
- Top bar (sticky): Search, filters, actions
- Content area: Scrollable, responsive

**Cards:**
- White background
- 1px border (sand-dark)
- 8px border radius
- 24px padding (1.5rem)
- Hover state: Bronze border, subtle shadow

**Buttons:**
- Primary: Navy background, white text, 6px radius
- Ghost: Transparent, sand-dark border, navy text
- Heights: 32px (small), 40px (default)
- Icon + label pattern

**Tags:**
- Font size: 0.6875rem (11px)
- Padding: 0.25rem 0.625rem
- 4px border radius
- Colour-coded by status/priority

### States & Interactions

**Task statuses:**
- To Do (default)
- In Progress (mint background)
- Review (bronze-light background)
- Blocked (plum background)
- Done (success-light background)

**Priority levels:**
- Urgent (danger-light background)
- High (warning-light background)
- Medium (sand background)
- Low (subtle)

**Interactive states:**
- Hover: Border colour change, subtle background shift
- Active: Bronze accent, distinct background
- Focus: Clear outline (accessibility)
- Disabled: Reduced opacity, cursor not-allowed

---

## 11. Content Guidelines

### Writing Style

**General principles:**
- Write for humans, not robots
- Use active voice
- Keep sentences short and clear
- Avoid construction jargon where possible
- When using technical terms, provide context

**Examples:**

**Good:** "Submit your building regulations application"  
**Bad:** "Initiate building control notification process"

**Good:** "This task is blocked because the groundworks aren't finished"  
**Bad:** "Dependencies prevent task execution"

### UK-Specific Language

Use British English and UK construction terminology:

- Building regulations (not building codes)
- Planning permission (not zoning approval)
- First fix / second fix
- Snagging (not punch list)
- Groundworks
- Building control
- SAP calculations
- Part L, Part M (building regs)

### Error Messages

**Pattern:** Explain what happened + what to do next

**Good:** "We couldn't save your budget. Check your internet connection and try again."  
**Bad:** "Error 500: Internal server exception"

### Empty States

**Pattern:** Explain why it's empty + what to do

**Good:** "You haven't created any tasks yet. Click 'New Task' to get started."  
**Bad:** "No data available"

---

## 12. Success Metrics

### User Success

- Users complete project setup within 15 minutes
- Users create their first task within 5 minutes
- Users return to the platform at least weekly
- Users report feeling "more in control" of their project

### Product Quality

- Page load under 2 seconds
- Zero accessibility errors (WCAG AA compliance)
- Mobile responsive on all views
- Works offline (with sync when connected)

### Business Goals

- 80% of users complete onboarding
- Average session time: 10+ minutes
- User retention after 30 days: 60%+
- Positive user feedback (surveys, interviews)

---

## 13. Design Deliverables

### Required Outputs

**Phase 1 (Now):**
1. This consolidated design brief
2. Colour palette tokens (CSS variables)
3. Typography system (CSS)
4. Component library (HTML/CSS)
5. Wireframes for core screens
6. Interactive prototype (Dashboard + Tasks)

**Phase 2 (Next):**
1. Full UI kit (all components)
2. Accessibility audit report
3. User testing findings
4. Refined specifications
5. Developer handoff documentation

---

## 14. Decisions Made & Open Questions

### ✅ Decisions Made

**Brand:**
- Name: **AvenStudio** (confirmed)
- Typography: **DM Sans** throughout (no serif)
- Dyslexia-friendly toggle available

**Technology:**
- **Electron** for desktop shell
- **Python + FastAPI** for backend
- **SQLite** for data layer
- **Offline-first** architecture
- Packaged as **.exe** (Windows) and **.app** (macOS)

### ⏳ Open Questions

**Features:**
- Which features are MVP vs Phase 2?
- How much AI assistance in early versions?
- Budget categories: pre-defined or fully custom?

**User Experience:**
- Onboarding flow complexity (quick start vs comprehensive setup)?
- Default dashboard layout (simple vs detailed)?
- Mobile companion app needed, or desktop-only?

**Business:**
- Pricing model (free, one-time purchase, subscription)?
- Beta testing approach and timeline
- Target launch date

---

## Appendix: Reference Materials

### Included Documents
1. Aven Studio - Brand.md
2. Aven Studio - Project Outline.md
3. Aven Concept Planning.md
4. selfbuild-dashboard.html (visual reference - mockup only)
5. selfbuild-timeline.html (visual reference - mockup only)

**Note:** The HTML mockups used "Ground+Flow" branding - this was exploratory work only. The actual product name is **AvenStudio**.

### External References
- UK Building Regulations (gov.uk)
- RIBA Plan of Work 2020
- WCAG 2.1 Level AA Guidelines
- DM Sans font (Google Fonts)
- Electron documentation (electronjs.org)
- FastAPI documentation (fastapi.tiangolo.com)
- SQLite documentation (sqlite.org)

---

**End of Design Brief**

*This document consolidates project vision, brand identity, UX principles, and technical specifications into a single, coherent reference. Use it as the foundation for all design and development decisions.*

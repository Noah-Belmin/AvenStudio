# AvenStudio - Technical Stack Decision
## Summary Document

**Date:** November 2025  
**Status:** ✅ Decided

---

## The Decision

**AvenStudio will be built as a desktop application using:**

```
Electron (desktop shell)
    ↓
HTML/CSS/JavaScript (interface)
    ↓
Python + FastAPI (business logic)
    ↓
SQLite (data storage)
```

**Distribution:**
- Windows: `.exe` installer
- macOS: `.app` bundle (with optional `.dmg`)

---

## Why This Stack?

### What You Asked For

✅ Click-to-run desktop app  
✅ Can be packaged as .exe or macOS app  
✅ SQLite data layer  
✅ Fully offline-first  
✅ Python for backend (your preferred language)

### What This Gives You

**For users:**
- Professional desktop experience
- No installation complexity
- No internet required
- Data stays private and local
- Fast and responsive

**For you:**
- Python for all business logic (clean, familiar)
- No JavaScript framework complexity
- Clear separation of concerns
- Can build incrementally
- Cross-platform by default

**For the project:**
- Professional quality from day one
- Easy to maintain and extend
- Good performance
- Future cloud sync possible (optional)
- Industry-standard approach

---

## What Each Technology Does

### Electron
**Role:** Desktop application wrapper

**What it does:**
- Creates the window and menus
- Handles file system access
- Bundles everything into .exe/.app
- Manages updates
- Provides native OS integration

**What it doesn't do:**
- Your business logic (that's Python)
- Database queries (that's SQLite)
- Complex UI frameworks (just clean HTML/CSS/JS)

**Think of it as:** The container that turns your web-like interface into a proper desktop app.

---

### Python + FastAPI
**Role:** Backend server (runs locally, invisibly)

**What it does:**
- Handles all business logic
- Processes data
- Talks to SQLite database
- Validates inputs
- Generates reports
- Manages file operations

**What it doesn't do:**
- Draw the interface (that's HTML/CSS)
- Show up to the user (runs silently in background)

**Think of it as:** The brain of the application - does all the thinking and data work.

---

### HTML/CSS/JavaScript
**Role:** User interface

**What it does:**
- Displays information
- Captures user input
- Shows forms, buttons, lists
- Provides visual feedback
- Handles clicks and interactions

**What it doesn't do:**
- Store data (that's SQLite)
- Run business logic (that's Python)

**Think of it as:** The face of the application - what users see and click.

---

### SQLite
**Role:** Database

**What it does:**
- Stores all project data
- Handles queries
- Manages relationships
- Ensures data integrity
- Creates backups

**What it doesn't do:**
- Need a server (it's just a file)
- Require configuration (works out of the box)
- Need internet (completely local)

**Think of it as:** The filing cabinet - reliably stores everything.

---

## How They Work Together

**When user opens AvenStudio:**

1. Electron launches the app window
2. Python backend starts automatically (user never sees this)
3. HTML/CSS interface loads in the window
4. User interacts with the interface
5. JavaScript sends requests to Python backend
6. Python queries SQLite database
7. Python sends data back to interface
8. Interface updates to show results

**All of this happens locally, on the user's computer.**

---

## File Structure

```
AvenStudio.app (or AvenStudio.exe)
│
├── Electron Shell
│   └── Creates the window
│
├── UI Layer (HTML/CSS/JS)
│   └── What users see and click
│
├── Python Backend (FastAPI)
│   └── Handles logic and data
│
└── SQLite Database
    └── Stores everything
```

**User's data location:**
- Windows: `C:\Users\[username]\AppData\Roaming\AvenStudio\`
- macOS: `~/Library/Application Support/AvenStudio/`

Contains:
- `aven.db` (SQLite database)
- `documents/` (uploaded files)
- `preferences.json` (user settings)

---

## Alternatives You Considered (and why we didn't pick them)

### Django (Python web framework)
**Why not:**
- Would require packaging with PyInstaller or Briefcase
- Harder to create polished desktop UI
- More web-like than app-like
- Less familiar desktop patterns

**When it would make sense:**
- If you were building a web app
- If desktop UI wasn't important

---

### Pure React (JavaScript framework)
**Why not:**
- Requires learning JavaScript ecosystem
- Still needs a backend (would need Python anyway)
- Still needs Electron for desktop (so same complexity)
- More moving parts than necessary

**When it would make sense:**
- If you wanted maximum UI flexibility
- If you were comfortable with JavaScript
- If you had a large team

---

### React + FastAPI + Electron
**Why not:**
- Most complex option
- React adds framework overhead
- Same end result as simpler approach
- Harder to maintain

**When it would make sense:**
- If UI needed to be extremely dynamic
- If you had React expertise
- If targeting web AND desktop from same code

---

## Development Roadmap

### Phase 1: Foundation (2-3 months)
**Goal:** Get basic app running

- Set up Electron shell
- Create Python FastAPI backend
- Connect to SQLite
- Build basic Dashboard
- Implement Tasks CRUD
- Get packaging working

**Deliverable:** Installable app that can create and manage tasks

---

### Phase 2: Core Features (2-3 months)
**Goal:** Full feature set

- Budget management
- Timeline/Gantt view
- Document upload
- Contact management
- All CRUD operations
- Basic reporting

**Deliverable:** Complete MVP ready for beta testing

---

### Phase 3: Polish (1-2 months)
**Goal:** Production ready

- Auto-updates
- Settings and preferences
- Performance optimization
- Bug fixes from beta
- Installer improvements
- Documentation

**Deliverable:** Public release v1.0

---

### Phase 4: Future (ongoing)
**Goal:** Advanced features

- Optional cloud sync
- AI assistance
- Mobile companion app
- Integration with other tools
- Advanced analytics

---

## Why This Approach Reduces Cognitive Load

**For development:**
- Python is your comfortable language
- Clear boundaries between layers
- Each piece has one job
- Can test each part separately
- Good error messages

**For learning:**
- One technology at a time
- Lots of documentation available
- Clear examples for each part
- Can build incrementally
- Easy to debug

**For maintenance:**
- Code organized logically
- Easy to find what needs changing
- Can update parts independently
- Future you will understand it

---

## Common Concerns Addressed

### "Isn't Electron heavy/bloated?"
**Reality:** Modern Electron apps are fine. VS Code, Slack, Discord all use it. Users expect desktop apps to use ~100-200MB. The benefits outweigh the cost.

### "Do I need to learn JavaScript?"
**Reality:** Minimal JS needed. Just enough for UI interactions. The complex logic stays in Python where you're comfortable.

### "Can SQLite handle this?"
**Reality:** Yes, easily. SQLite can handle databases up to 281 TB. Your average self-build project will be <10MB. It's used in browsers, phones, everywhere.

### "What about cloud sync?"
**Reality:** Local-first for now. Cloud sync can be added later as optional feature. Users appreciate having control of their data.

### "Can I distribute this legally?"
**Reality:** Yes. All technologies chosen are open source with permissive licenses. No licensing fees. You can sell the app if you want.

---

## Next Steps

1. **Set up development environment**
   - Install Node.js (for Electron)
   - Install Python 3.11+
   - Install VS Code or your editor
   - Install Git

2. **Create basic skeleton**
   - Initialize Electron app
   - Set up FastAPI backend
   - Create SQLite database
   - Connect them together

3. **Build one feature end-to-end**
   - Create Task (UI → Python → SQLite → back to UI)
   - Proves everything works
   - Template for other features

4. **Iterate and expand**
   - Add more features
   - Improve UI
   - Test with real users
   - Refine based on feedback

---

## Resources

**Electron:**
- Official docs: https://www.electronjs.org/docs/latest
- Electron Forge: https://www.electronforge.io/ (easier setup)

**FastAPI:**
- Official docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

**SQLite:**
- Official docs: https://www.sqlite.org/docs.html
- Python sqlite3: https://docs.python.org/3/library/sqlite3.html

**Electron + Python Integration:**
- zerorpc: https://github.com/0rpc/zerorpc-python
- python-shell: https://github.com/extrabacon/python-shell

**Packaging:**
- electron-builder: https://www.electron.build/
- Works for both Windows and macOS

---

**This decision gives you the clearest path forward with minimal complexity and maximum control.**

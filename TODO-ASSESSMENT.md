# AvenStudio: Complete TODO Assessment
**Based on Design Brief Analysis**
**Current Status:** 5% of full vision complete

---

## 📊 Current State vs Full Vision

### ✅ What's Built (5% Complete)

**Backend Infrastructure:**
- ✅ Electron desktop shell
- ✅ Python FastAPI server (basic)
- ✅ SQLite database layer
- ✅ Modular orchestrator pattern
- ✅ Basic task CRUD API
- ✅ Stats/analytics API
- ✅ Categories API
- ✅ Automation rules API (stub)

**Frontend:**
- ✅ Design system (Navy/Bronze/Mint colors, DM Sans typography)
- ✅ Dashboard view (stats cards, task lists, progress bar)
- ✅ Component library (buttons, cards, tags, sidebar)

**Missing:** 95% of features described in design brief

---

## 🎯 Phase 1: MVP Foundation (2-3 months)

### Core Database Schema - 🔴 Not Started

**projects table** - Critical, blocking everything
```sql
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT,
    project_type TEXT CHECK(project_type IN ('self-build', 'custom-build', 'renovation')),
    start_date TEXT,
    target_completion TEXT,
    status TEXT DEFAULT 'planning',
    budget_total REAL,
    created_at TEXT,
    updated_at TEXT
);
```

**Current status:** No project concept exists - users can't create/manage multiple projects

**tasks table** - 🟡 Partially complete
```sql
-- NEED TO ADD:
- project_id (FK to projects)
- assignee_id (who's responsible)
- start_date (not just due date)
- blocked_by (task dependencies)
- phase (which build phase: groundworks, structure, etc.)
- attachments (file links)
```

**budget_items table** - 🔴 Not started
```sql
CREATE TABLE budget_items (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    category TEXT,  -- groundworks, structure, M&E, finishes, etc.
    item_name TEXT,
    estimated_cost REAL,
    actual_cost REAL,
    variance REAL GENERATED,
    supplier TEXT,
    quote_date TEXT,
    status TEXT,  -- quoted, approved, ordered, paid
    notes TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

**documents table** - 🔴 Not started
```sql
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    filename TEXT,
    file_path TEXT,
    document_type TEXT,  -- planning, building_regs, certificate, drawing, etc.
    version INTEGER,
    linked_task_id TEXT,
    linked_phase TEXT,
    upload_date TEXT,
    tags TEXT,  -- JSON array
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

**contacts table** - 🔴 Not started
```sql
CREATE TABLE contacts (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT,
    role TEXT,  -- architect, builder, engineer, supplier, etc.
    company TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    notes TEXT,
    contracts TEXT,  -- JSON array of contract details
    performance_rating INTEGER,  -- 1-5 stars
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

**milestones table** - 🔴 Not started
```sql
CREATE TABLE milestones (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    name TEXT,
    phase TEXT,  -- pre-planning, planning, groundworks, structure, etc.
    target_date TEXT,
    actual_date TEXT,
    status TEXT,
    dependencies TEXT,  -- JSON array of milestone IDs
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

**materials table** - 🔴 Not started
```sql
CREATE TABLE materials (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    item_name TEXT,
    quantity REAL,
    unit TEXT,  -- m², linear m, tonnes, units, etc.
    supplier_id TEXT,
    cost REAL,
    lead_time_days INTEGER,
    delivery_date TEXT,
    delivery_status TEXT,
    warranty_info TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (supplier_id) REFERENCES contacts(id)
);
```

---

### 1. Project Management Core - 🔴 CRITICAL

**Onboarding Flow** - Essential first experience
- [ ] Welcome screen with brand introduction
- [ ] Project creation wizard:
  - [ ] Project name and location
  - [ ] Project type (self-build, custom-build, renovation)
  - [ ] Start date and target completion
  - [ ] Budget (optional at this stage)
- [ ] Initial setup:
  - [ ] Import standard UK build phases (18 phases from design brief)
  - [ ] Create default categories
  - [ ] Set up basic milestones
- [ ] Quick tour (progressive disclosure)

**Project Switcher** - Multiple projects support
- [ ] Project list view
- [ ] Create new project
- [ ] Switch between projects
- [ ] Archive/delete projects
- [ ] Project settings per project

**Estimated time:** 1 week

---

### 2. Enhanced Dashboard - 🟡 Started, needs expansion

**Current:** Basic stats, task lists
**Needed:**
- [ ] Project health indicators (on track, at risk, delayed)
- [ ] Budget vs actual spend (mini chart)
- [ ] Timeline visualization (% complete by phase)
- [ ] Weather widget (for UK - affects builds)
- [ ] Action items (what needs attention TODAY)
- [ ] Recent activity feed
- [ ] Quick create buttons (task, budget item, contact)

**Estimated time:** 1 week

---

### 3. Full Task Management - 🟡 Started (20% complete)

**Needed:**

**Task List View** - Complete overhaul
- [ ] Full CRUD (create, read, update, delete) via UI
- [ ] Sortable columns (date, priority, status, phase)
- [ ] Multi-level filtering:
  - [ ] By phase (groundworks, structure, first fix, etc.)
  - [ ] By assignee (me, architect, builder, etc.)
  - [ ] By status, priority, date range
  - [ ] Saved filter views
- [ ] Bulk actions (select multiple, batch update)
- [ ] Search functionality
- [ ] Group by phase/assignee/status
- [ ] Export to CSV/PDF

**Kanban Board View**
- [ ] Columns: To Do, In Progress, Review, Blocked, Done
- [ ] Drag-and-drop to change status
- [ ] Card shows: title, priority, due date, assignee, tags
- [ ] Quick edit on card click
- [ ] Filter by phase/assignee while in Kanban
- [ ] WIP limits (optional)

**Calendar View**
- [ ] Month/week/day views
- [ ] Tasks displayed on due dates
- [ ] Color-coded by priority or phase
- [ ] Click date to create task with that due date
- [ ] Drag to reschedule
- [ ] Milestone markers

**Timeline/Gantt View**
- [ ] Horizontal bars showing task duration
- [ ] Dependencies shown as connecting lines
- [ ] Phase grouping
- [ ] Critical path highlighting
- [ ] Baseline vs actual dates
- [ ] Delay impact calculations
- [ ] Zoom levels (day, week, month)

**Task Detail Drawer** - Critical missing piece
- [ ] Full metadata form:
  - [ ] Title, description (rich text)
  - [ ] Phase selection
  - [ ] Status, priority
  - [ ] Start date, due date
  - [ ] Assignee (contact picker)
  - [ ] Tags
  - [ ] Blocked by (other tasks)
  - [ ] Attachments (link documents)
  - [ ] Completion percentage
- [ ] Comments/notes section
- [ ] Activity log (who changed what, when)
- [ ] Related tasks
- [ ] Delete task (with confirmation)

**New Task Modal** - Critical missing piece
- [ ] Quick create form
- [ ] Smart defaults based on phase
- [ ] Template system (common task types)
- [ ] Duplicate existing task
- [ ] Create subtasks

**Estimated time:** 3 weeks

---

### 4. Budget Management - 🔴 Not Started

**Budget Overview Screen**
- [ ] Total budget vs actual spend
- [ ] Category breakdown (pie chart):
  - [ ] Land
  - [ ] Groundworks
  - [ ] Structure (foundations, walls, roof)
  - [ ] First fix (electrics, plumbing, insulation)
  - [ ] Second fix (kitchens, bathrooms, flooring)
  - [ ] External works
  - [ ] Professional fees
  - [ ] Contingency
- [ ] Variance indicators (over/under budget per category)
- [ ] Cashflow by month/phase
- [ ] Alerts for overspend

**Budget Items List**
- [ ] Line item management:
  - [ ] Item name, category
  - [ ] Estimated cost
  - [ ] Actual cost (when paid)
  - [ ] Variance calculation
  - [ ] Supplier
  - [ ] Status (quoted, approved, ordered, paid)
- [ ] Quote comparison view:
  - [ ] Upload multiple quotes
  - [ ] Side-by-side comparison
  - [ ] Mark preferred supplier
- [ ] Filtering by category, status, supplier
- [ ] Export budget report

**Budget Entry Forms**
- [ ] Add budget item modal
- [ ] Quick edit inline
- [ ] Bulk import from CSV
- [ ] Link to tasks/phases

**Estimated time:** 2 weeks

---

### 5. Timeline & Phases - 🔴 Not Started

**UK Construction Phases** (Pre-defined)
```
1. Pre-planning & Feasibility
2. Planning Application
3. Building Regulations
4. Tender & Procurement
5. Site Setup
6. Groundworks & Foundations
7. Substructure
8. Superstructure (walls, roof)
9. External Envelope
10. First Fix Carpentry
11. First Fix Electrics
12. First Fix Plumbing & Heating
13. Insulation
14. Plastering
15. Second Fix Carpentry
16. Second Fix Electrics
17. Second Fix Plumbing
18. Finishes & Snagging
```

**Timeline View**
- [ ] Gantt-style chart
- [ ] Phase bars with start/end dates
- [ ] Milestone markers
- [ ] Dependency lines
- [ ] Drag to adjust dates
- [ ] See impact of delays
- [ ] Critical path highlighting
- [ ] Baseline vs actual timeline
- [ ] Export to PDF/image

**Phase Management**
- [ ] View tasks by phase
- [ ] Set phase dates
- [ ] Mark phase as complete
- [ ] Phase templates (standard UK build sequence)
- [ ] Phase dependencies

**Milestone Tracking**
- [ ] Create milestones
- [ ] Link to phases
- [ ] Target vs actual dates
- [ ] Milestone alerts
- [ ] Completion checklist

**Estimated time:** 2-3 weeks

---

### 6. Simple Settings - 🔴 Not Started

**Project Settings**
- [ ] Project name, location
- [ ] Date preferences
- [ ] Budget currency (£ default)
- [ ] Phase customization

**App Preferences**
- [ ] Theme (light/dark mode toggle)
- [ ] Dyslexia-friendly font toggle
- [ ] Notification preferences
- [ ] Data backup location
- [ ] Export/import project data

**Estimated time:** 3-4 days

---

## 🏗️ Phase 2: Structure & Organization (2-3 months)

### 7. Document Management - 🔴 Critical for real use

**Document Library**
- [ ] Upload files (PDF, images, CAD, spreadsheets)
- [ ] Organize by type:
  - [ ] Planning documents
  - [ ] Building regulations
  - [ ] Drawings (architectural, structural, M&E)
  - [ ] Certificates (FENSA, SAP, warranties)
  - [ ] Contracts
  - [ ] Invoices
  - [ ] Site photos
- [ ] Version control:
  - [ ] Track revisions
  - [ ] Mark latest version
  - [ ] Version history
- [ ] Tagging system
- [ ] Link documents to:
  - [ ] Tasks
  - [ ] Phases
  - [ ] Budget items
  - [ ] Contacts
- [ ] Search and filter
- [ ] Mobile-friendly viewer
- [ ] Download/export bundles

**Document Upload Flow**
- [ ] Drag-and-drop upload
- [ ] Multiple file support
- [ ] Auto-categorization suggestions
- [ ] OCR for PDFs (extract text for search)

**Storage Management**
- [ ] Show storage used
- [ ] Cleanup old versions
- [ ] Backup to external location

**Estimated time:** 2-3 weeks

---

### 8. Contact Management - 🔴 Essential for coordination

**Contact Directory**
- [ ] Create contact profiles:
  - [ ] Name, company
  - [ ] Role (architect, structural engineer, builder, plumber, electrician, supplier, etc.)
  - [ ] Email, phone, address
  - [ ] Website, social media
  - [ ] Insurance details
  - [ ] Certifications
- [ ] Contact categories (professional, supplier, contractor, etc.)
- [ ] Performance rating (1-5 stars)
- [ ] Notes and observations
- [ ] Contract storage (link documents)

**Contact Interaction Log**
- [ ] Timestamped notes
- [ ] Meeting records
- [ ] Site visit logs
- [ ] Decisions made
- [ ] Email integration (future)

**Task Assignment**
- [ ] Assign tasks to contacts
- [ ] View all tasks per contact
- [ ] Workload visualization

**Contact List Views**
- [ ] All contacts
- [ ] By role
- [ ] Search and filter
- [ ] Export contact list

**Estimated time:** 1-2 weeks

---

### 9. Materials & Procurement - 🔴 Not Started

**Materials List**
- [ ] Item catalog:
  - [ ] Item name, description
  - [ ] Quantity and unit (m², linear m, tonnes, etc.)
  - [ ] Supplier
  - [ ] Cost per unit
  - [ ] Total cost
  - [ ] Lead time (days)
  - [ ] Delivery date
- [ ] Delivery status tracking:
  - [ ] On order
  - [ ] In transit
  - [ ] Delivered
  - [ ] Overdue alerts
- [ ] Link to budget items
- [ ] Link to tasks (what needs this material)

**Supplier Management**
- [ ] Supplier contacts (subset of contacts)
- [ ] Track lead times
- [ ] Performance ratings
- [ ] Warranty information storage

**Materials Planning**
- [ ] Schedule deliveries to align with timeline
- [ ] Alert when material needed soon
- [ ] Avoid over-ordering or under-ordering

**Estimated time:** 1-2 weeks

---

### 10. Enhanced Dashboard Widgets - 🟡 Expand existing

**Additional Widgets**
- [ ] Budget burn rate chart
- [ ] Timeline progress bar
- [ ] Upcoming milestones
- [ ] Weather forecast (UK-specific, affects builds)
- [ ] Blocked tasks requiring attention
- [ ] Documents awaiting approval
- [ ] Overdue deliveries
- [ ] Contractor schedule (who's on site when)

**Dashboard Customization**
- [ ] Drag-and-drop widget layout
- [ ] Show/hide widgets
- [ ] Widget settings

**Estimated time:** 1 week

---

## 🎨 Phase 3: Polish & Distribution (1-2 months)

### 11. Reporting & Export - 🔴 Not Started

**Report Generator**
- [ ] Budget report (detailed breakdown, variance analysis)
- [ ] Timeline summary (phases, milestones, delays)
- [ ] Task list exports (by phase, assignee, status)
- [ ] Document bundles (for inspections, lenders)
- [ ] Project status report (for sharing with family/lenders)

**Export Formats**
- [ ] PDF (formatted, print-ready)
- [ ] CSV (for Excel)
- [ ] JSON (for backup/migration)

**Sharing**
- [ ] Generate shareable PDF
- [ ] Email integration (future)
- [ ] Print-optimized layouts

**Estimated time:** 1-2 weeks

---

### 12. Advanced Features - 🔴 Not Started

**Search**
- [ ] Global search (tasks, documents, contacts, notes)
- [ ] Search filters
- [ ] Recent searches
- [ ] Keyboard shortcut (⌘K)

**Filtering & Views**
- [ ] Saved views (custom filters)
- [ ] Quick filters (mine, urgent, overdue, etc.)
- [ ] Smart filters (e.g., "delayed tasks impacting milestones")

**Bulk Actions**
- [ ] Select multiple tasks
- [ ] Batch update (change phase, reassign, reschedule)
- [ ] Batch delete
- [ ] Batch export

**Undo/Redo**
- [ ] Action history
- [ ] Undo last action
- [ ] Redo

**Keyboard Shortcuts**
- [ ] Global shortcuts (new task, search, switch views)
- [ ] Navigation shortcuts
- [ ] Shortcuts help modal

**Estimated time:** 2 weeks

---

### 13. Planning & Brief Module - 🔴 Future feature

**Brief Builder** (Guided questions)
- [ ] Project vision and goals
- [ ] Room-by-room requirements
- [ ] Sustainability priorities
- [ ] Budget constraints
- [ ] Timeline constraints
- [ ] Priority tagging (must-have vs nice-to-have)

**Planning Constraints**
- [ ] Conservation area info
- [ ] Permitted development checks
- [ ] Local planning requirements

**Building Regulations Notes**
- [ ] Part L (energy efficiency)
- [ ] Part M (accessibility)
- [ ] Part B (fire safety)
- [ ] SAP calculations

**Estimated time:** 2-3 weeks

---

### 14. Production Build & Distribution - 🔴 Essential for release

**Electron Packaging**
- [ ] Windows .exe installer (electron-builder)
- [ ] macOS .app bundle (with .dmg)
- [ ] Linux AppImage
- [ ] Include Python runtime in bundle
- [ ] Code signing (macOS, Windows)
- [ ] Icon and splash screen

**Installation Experience**
- [ ] Installer wizard
- [ ] License agreement
- [ ] Install location selection
- [ ] Desktop shortcut creation
- [ ] Start menu/Applications folder

**Auto-Updater**
- [ ] Check for updates on launch
- [ ] Download and install updates
- [ ] Release notes display
- [ ] Update server setup

**File Locations**
- [ ] Windows: `C:\Users\[username]\AppData\Roaming\AvenStudio`
- [ ] macOS: `~/Library/Application Support/AvenStudio`
- [ ] Database, documents, settings stored here

**Estimated time:** 1-2 weeks

---

### 15. Testing & QA - 🔴 Essential

**Unit Tests**
- [ ] Backend API tests (pytest)
- [ ] Database layer tests
- [ ] Business logic tests

**Integration Tests**
- [ ] Frontend-backend integration
- [ ] Database operations
- [ ] File handling

**Manual QA Checklist**
- [ ] All features work on Windows
- [ ] All features work on macOS
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Offline functionality
- [ ] Data import/export
- [ ] Performance testing (large projects)

**User Testing**
- [ ] Beta tester recruitment
- [ ] Feedback collection
- [ ] Bug fixes based on feedback

**Estimated time:** 2-3 weeks

---

## 🤖 Phase 4: Intelligence (Future / 6-12 months out)

### 16. AI Workbook - 🔴 Long-term feature

**Planning Assistance**
- [ ] AI-powered question flow
- [ ] Suggest tasks based on project type
- [ ] Estimate timelines
- [ ] Flag potential issues

**Smart Suggestions**
- [ ] Suggest budget categories
- [ ] Recommend contractors (based on location)
- [ ] Identify missing tasks
- [ ] Detect timeline conflicts

**Risk Detection**
- [ ] Budget overruns
- [ ] Timeline delays
- [ ] Critical path risks
- [ ] Weather impacts

**Reference Database**
- [ ] UK building regulations lookup
- [ ] Standard build phases
- [ ] Typical costs database
- [ ] Common pitfalls

**Estimated time:** 3-4 months (requires AI integration)

---

### 17. Advanced Integrations - 🔴 Long-term

**Cloud Sync (Optional)**
- [ ] Encrypted backup to cloud
- [ ] Sync across devices
- [ ] Still works offline-first
- [ ] User controls when to sync

**Third-party Integrations**
- [ ] Calendar apps (Google Calendar, Outlook)
- [ ] Email integration
- [ ] Accounting software (Xero, QuickBooks)
- [ ] Project management tools (Trello, Asana)

**API for Extensions**
- [ ] Plugin system
- [ ] Developer documentation
- [ ] Community extensions

**Estimated time:** 2-3 months per integration

---

## 📊 Summary: Work Breakdown

| Phase | Features | Estimated Time | Status |
|-------|----------|----------------|--------|
| **Current** | Basic dashboard, task API | — | ✅ 5% Complete |
| **Phase 1 (MVP)** | Projects, full tasks, budget, timeline, settings | 2-3 months | 🔴 Not started |
| **Phase 2 (Structure)** | Documents, contacts, materials, enhanced dashboard | 2-3 months | 🔴 Not started |
| **Phase 3 (Polish)** | Reports, search, bulk actions, production build | 1-2 months | 🔴 Not started |
| **Phase 4 (Intelligence)** | AI assistance, integrations, advanced features | 6-12 months | 🔴 Future |

**Total estimated development time: 12-20 months for full vision**

---

## 🎯 Recommended Immediate Priorities

### Week 1-2: Foundation
1. ✅ **Projects table and UI** - Blocking everything else
2. ✅ **Project onboarding flow** - First user experience
3. ✅ **Project switcher** - Multiple projects support

### Week 3-4: Core CRUD
4. ✅ **New task modal** - Create tasks from UI
5. ✅ **Task detail drawer** - Edit/delete tasks
6. ✅ **Enhanced task model** - Add missing fields (phase, assignee, start_date, blocked_by)

### Week 5-6: Essential Views
7. ✅ **Task list view** - Full sorting/filtering
8. ✅ **Kanban board** - Visual task management
9. ✅ **Simple budget view** - Track spending

### Week 7-8: Timeline
10. ✅ **UK build phases setup** - 18 standard phases
11. ✅ **Timeline/Gantt view** - Visual scheduling
12. ✅ **Milestones** - Key dates tracking

---

## 🚨 Critical Missing Components

### Database Schema (High Priority)
- ❌ **projects** table - Users can't create projects!
- ❌ **budget_items** table - Budget tracking impossible
- ❌ **documents** table - Can't store files
- ❌ **contacts** table - Can't track professionals
- ❌ **milestones** table - Can't mark key dates
- ❌ **materials** table - Can't manage procurement

### Backend APIs (High Priority)
- ❌ Projects CRUD
- ❌ Budget CRUD
- ❌ Documents CRUD (with file upload)
- ❌ Contacts CRUD
- ❌ Milestones CRUD
- ❌ Materials CRUD
- ❌ File handling (upload, download, versioning)

### Frontend UI (High Priority)
- ❌ 8 of 9 main views (only dashboard exists)
- ❌ Task CRUD modals (can't create/edit from UI)
- ❌ All Phase 2/3 features

### Infrastructure (Medium Priority)
- ❌ Production build (can't distribute to users)
- ❌ Auto-updater (can't push updates)
- ❌ Testing suite (no automated tests)

---

## 💡 Complexity Assessment

**Current Stack Complexity:** Low ✅
**Full Project Complexity:** High 🔴

**Why high complexity:**
- 7 core database tables (projects, tasks, budget, documents, contacts, milestones, materials)
- 9 major UI views (dashboard, tasks×4, budget, timeline, documents, contacts, settings)
- File management system (upload, version, storage)
- UK-specific domain knowledge (planning, building regs, phases)
- Offline-first architecture (sync complexity)
- Cross-platform distribution (Windows, macOS, Linux)

**This is a 12-18 month project for full v1.0**

---

## 🎯 MVP Definition (What's actually needed for beta launch)

**Minimum viable AvenStudio:**
1. ✅ Create a project
2. ✅ Create and manage tasks (all CRUD)
3. ✅ Organize tasks by UK build phases
4. ✅ Track budget (basic categories, estimated vs actual)
5. ✅ View timeline/Gantt chart
6. ✅ Upload and organize documents
7. ✅ Manage contacts (architects, builders, suppliers)
8. ✅ Generate basic reports (budget, task list)
9. ✅ Package as desktop app (.exe/.app)

**Estimated time to MVP beta: 3-4 months full-time**

---

## 📋 Next Steps Recommendation

### Option A: Full MVP (3-4 months)
Build everything listed in Phase 1 properly. This gets you a beta-testable product that real users can try.

### Option B: Iterative Releases (faster feedback)
1. **v0.2** (2 weeks): Projects + enhanced tasks
2. **v0.3** (2 weeks): Budget tracking
3. **v0.4** (2 weeks): Timeline & phases
4. **v0.5** (3 weeks): Documents & contacts
5. **v1.0** (2 weeks): Polish + production build

**Total: 11 weeks to v1.0 MVP**

### Option C: Focus on Unique Value (fastest)
Skip generic project management features. Focus on **UK self-build specific** value:
- ✅ UK build phases (18 phases)
- ✅ Building regulations checklist
- ✅ Planning permission tracking
- ✅ SAP calculations helper
- ✅ UK supplier database
- ✅ Weather integration (UK forecast)

Make AvenStudio **uniquely valuable for UK self-builders**, not just another project manager.

---

**Conclusion:**

The design brief describes an **enterprise-level application** with massive scope. The current prototype validates the architecture works, but you're at 5% completion.

**Realistic path forward:**
- 3-4 months to MVP beta (core features only)
- 6-9 months to v1.0 (polished, distributable)
- 12-18 months to full design brief vision

This is a **significant long-term project**, but the foundation you've built (clean architecture, simple stack, beautiful design) is solid.

**Recommendation:** Prioritize the uniquely valuable UK self-build features over generic project management. That's your competitive advantage.

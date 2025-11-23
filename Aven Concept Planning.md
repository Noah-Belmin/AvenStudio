Aven Studio - Self Build Navigator should support users in tracking all the major pillars of a self-build project:  

• budgets and costs  
• timelines, phases, and critical path  
• tasks and to-dos  
• materials and suppliers  
• documents, drawings, and specifications  
• key contacts such as builders, architects, engineers, consultants  
• procurement steps and contractor management  
• brief creation and revisions  
• a central dashboard that surfaces priorities, issues, and overall progress  
• reports that can be exported or shared when needed

# **1. User Stories (Clear, Practical, UK-Focused)**

These are written from the user’s point of view and reflect real behaviors you’d expect from someone designing and building their own home.

### **Planning & Early Concept**

- _As a self-builder, I want to capture my early ideas and requirements so I can shape a clear brief before speaking to professionals._
- _As a user, I want a simple way to record planning constraints (local authority, conservation area, permitted development limits) so I understand what’s realistically achievable._
- _As a user, I want guidance on building regulations to ensure I make decisions that won’t cause delays later._

### **Budget & Costs**

- _As a self-builder, I want to set an overall budget so I can see how decisions affect affordability._
- _As a user, I want to record quotes from contractors and suppliers so I can compare and choose wisely._
- _As a user, I want alerts when costs exceed estimates so I can take action quickly._
    

### **Timeline & Phasing**

- _As a user, I want a visual timeline that breaks the build into phases (foundations, structure, first fix, etc.) so I know what’s coming next._
- _As a user, I want to track dependencies (e.g., roof must be completed before windows) so I can manage expectations and sequencing._

### **Tasks & To-Dos**

- _As a self-builder, I want to see all my tasks in one place so nothing critical slips through the cracks._
- _As a user, I want tasks grouped by phase so I can focus on what matters right now._    

### **Materials, Suppliers & Procurement**

- _As a user, I want to maintain a list of materials and suppliers so I can order at the right time and avoid delays._    
- _As a user, I want to track lead times so I know when to place orders._


### **Documents & Specifications**

- _As a user, I want to store drawings, approvals, certificates, and specifications so everything is organised and accessible._    
- _As a user, I want version history so I can refer back to earlier decisions._


### **Contacts & Contractors**

- _As a self-builder, I want a directory of contractors, designers, and professionals so I have all key people in one place._
- _As a user, I want to log meetings, site visits, and decisions so I don’t lose track of what’s been agreed._


### **Reporting**

- _As a user, I want simple reports showing budget status, progress, and outstanding tasks so I can update family, lenders, or inspectors._
    

### **Dashboard**

- _As a user, I want a dashboard that gives me a snapshot of budget, timeline, tasks, and risks so I always know the project’s health._
    

---

# **2. Project Management Workflows Relevant to Construction / Self-Build**

These are the core workflows normally used in UK self-build or small-scale construction. Your app can support them directly through navigation, screens, and data structures.

---

## **A. RIBA-Inspired Design Stages (UK Standard)**

Even if your users aren’t architects, this sequence is intuitive:

1. **Strategic Definition** – goals, early ideas, constraints
2. **Preparation & Brief** – requirements, budget, planning considerations
3. **Concept Design**
4. **Spatial Coordination / Technical Design**
5. **Manufacturing & Construction**
6. **Handover**
7. **Use / Maintenance**

You don’t need to use the official terminology, but the flow is gold for structuring a project.

---

## **B. Construction Workflow Phases (plain-language, user-friendly)**

### **1. Pre-Planning**

- Define goals
- Research planning requirements
- Produce sketches / rough design
- Set initial budget
- Design Brief Builder (Add room by room sections )

### **2. Planning Permission & Approvals**

- Submit planning application
- Track documents, decisions, revisions
- Handle neighbour consultations
- Track building regs packages and approvals

### **3. Detailed Design**

- Final drawings
- Specification writing
- Structural calculations
- SAP/EPC considerations

### **4. Procurement**

- Tendering (quotes from builders)
- Selecting contractors
- Ordering materials
- Scheduling deliveries, handling lead times

### **5. Construction**

Broken into familiar site phases:

- Groundworks
- Foundations
- Frame/structure
- Roof
- Windows/doors
- First fix (electrical, plumbing, HVAC)
- Insulation
- Plastering
- Second fix
- Finishes
- Snagging

### **6. Handover / Completion**

- Certificates (building regs, electrical, gas safe, etc.)
- Final inspections
- Sign-off
- Move-in prep

### **7. Post-Completion**

- Warranty management (NHBC or similar)
- Maintenance schedule
- Future improvements

---

# **C. Supporting Workflows (cross-cutting across all phases)**

### **Budget Management Workflow**

1. Create initial budget
2. Add real quotes
3. Track committed spend
4. Update forecasts
5. Flag overruns

### **Task Workflow**

1. Create task
2. Assign to phase/contact
3. Add due dates
4. Mark blockers
5. Complete + log notes


### **Risk Management Workflow**

- Identify risks
- Track likelihood/impact
- Add mitigation steps
- Review regularly (dashboard could surface these)

### **Document Workflow**

- Upload
- Tag by category
- Store revisions
- Link to tasks or phases

---

# **1. Expanded User Stories (Deeper, Broader, More Useful for Design)**

### **Early Vision & Brief Formation**

- _As a self-builder, I want a place to explore my ideas without judgement, so I can gradually shape them into a clear brief that I feel confident sharing with professionals._
    
- _As a user, I want prompts and checklists that remind me of things I might forget (e.g., access, orientation, storage, energy strategy) so my brief is holistic rather than reactive._
    
- _As someone new to the process, I want gentle explanations of building regs and planning constraints so I don’t accidentally design something unbuildable._
    

### **Budgeting & Financial Control**

- _As a self-builder, I want to break my budget into categories so I can see where the money goes (e.g. groundwork, materials, professional fees)._
    
- _As a user, I want automatic calculations (estimates vs actuals vs forecast) so I don’t miscalculate due to stress or lack of experience._
    
- _As a user managing multiple quotes, I want to compare them easily so I can make an informed, confident choice._
    

### **Timeline & Phase Management**

- _As a user, I want to understand the general order of a self-build so I don’t schedule things in an impossible sequence._
    
- _As a self-builder juggling life and deadlines, I want reminders for key dates (planning responses, delivery lead times, contractor reviews) so nothing drifts._
    
- _As a user, I want to visualise how delays impact the rest of the project, so I can adjust expectations early._
    

### **Tasks, To-Dos & Daily Management**

- _As a user, I want tasks grouped by phase so I can focus on what matters now rather than the overwhelming big picture._
    
- _As a person managing trades, I want tasks I can assign to contractors or professionals so responsibilities are crystal clear._
    
- _As someone whose energy fluctuates, I want tasks to be simple, actionable and not buried in clutter._
    

### **Materials, Suppliers & Procurement**

- _As a user, I want to list materials with quantities and costs so I don’t reorder or under-order accidentally._
    
- _As a user, I want to track delivery lead times so materials arrive when needed and don’t hold up the build._
    
- _As a user, I want space to store supplier contacts, quotes, warranties and notes so everything stays tidy._
    

### **Documents, Drawings & Specifications**

- _As a user, I want all drawings, approvals and certificates stored in one place so I’m not searching email threads._
    
- _As a self-builder, I want version control so I know which drawing is current, avoiding costly mistakes._
    
- _As a user, I want to link documents directly to phases or tasks so they’re easy to find in context._
    

### **Contractors, Contacts & Communication**

- _As a user, I want a contact book for builders, architects, engineers, planners and suppliers so all my key people are centralised._
    
- _As a user, I want to store notes from meetings or site visits so I don’t forget agreements or action points._
    
- _As a user hiring trades, I want to track performance and reliability so I can make informed choices in future._
    

### **Dashboard & Insights**

- _As a user, I want a dashboard that shows the health of my project at a glance so I don’t lose my sense of direction._
    
- _As a user, I want indicators for risk, delays or overruns so I can fix issues before they escalate._
    
- _As a user, I want the dashboard to be calm, not overwhelming — a place to reset my head._
    

### **Reporting & Exporting**

- _As a user, I want simple, shareable reports (budget, tasks, timelines) so I can update family, lenders or contractors easily._
    
- _As a user, I want PDF exports for inspections, meetings, or planning updates._
    

---

# **2. Expanded Feature Definitions (What the App _Actually Does_)**

Below is a deeper breakdown of each feature so we have a strong foundation for design.

---

## **A. Project Brief Builder**

**Purpose:** Help users build a coherent brief that evolves organically.  
**Features:**

- Guided questions (rooms, lifestyle, sustainability, aesthetics)
- Planning constraints (site context, access, conservation area flags)
- Building Regs notes (Part L, Part M accessibility, drainage, U-values)
- Priorities tagging (must-have, nice-to-have)


---

## **B. Budget Manager**

**Purpose:** Give users clarity and confidence about money.  
**Features:**

- Category-based budgeting (land, design, materials, labour, fees)
- Quote comparison tool
- Running actuals + forecast
- Overrun alerts
- Cashflow breakdown by phase
- VAT/Zero-rated calculations for self-builds
    

---

## **C. Timeline & Phase Planner**

**Purpose:** Make sequencing understandable.  
**Features:**

- Pre-set UK construction phases
- Custom phases
- Gantt-style timeline
- Lead-time logic for materials
- Delay impact calculations
- Milestones (planning submission, foundation pour, first fix, etc.)
    

---

## **D. Task Management**

**Purpose:** Keep people from being overwhelmed.  
**Features:**

- Tasks grouped by phase
- Priority levels
- Contractor assignment
- Checklists for each build stage
- Reminder system
    

---

## **E. Materials & Suppliers**

**Purpose:** Help users buy the right things at the right time.  
**Features:**

- Materials list with quantities
- Supplier directory
- Price tracking
- Delivery scheduling & notifications
- Warranty tracking
    

---

## **F. Documents & Specs Hub**

**Purpose:** A single source of truth.  
**Features:**

- Upload, tag, and categorise documents
- Link files to tasks, suppliers, phases
- Version history
- Quick access for site visits or inspections
    

---

## **G. Contacts & Contractors Manager**

**Purpose:** Reduce communication chaos.  
**Features:**

- Contact profiles (builders, architects, engineers)
- Notes log (meetings, agreements, disputes)
- Contract dates, insurance, certificates
- Performance/feedback notes
    

---

## **H. Dashboard**

**Purpose:** A calm, clear snapshot  of the project with no noise.  

**Always visible (minimal info first users can add or remove)**

**Features:**

- Project progress bar (overall build stage)
- Quick links to documents or reports
- Key upcoming milestone
- Number of urgent decisions/tasks
- Budget snapshot (simplified: spent vs budget)
- Key upcoming milestone
- High Priority Tasks
- Total Tasks
- In Progress (tasks) - no. of
- completed (tasks) - no. of
- Blocked (tasks) - no. of
- Upcoming Due Dates
-  High Priority Tasks
- Risks flagged

**Expandable sections (progressive disclosure):**

- Tasks & deadlines (full list or filtered)
- Budget details / alerts
- Milestones history & future
- Document queue (contracts, planning docs, permits)


---

## **I. Reporting & Exporting**

**Purpose:** Support inspections, lenders, and communication with trades.  
**Features:**

- Budget reports
- Task lists
- Timeline summaries
- Document bundles
- PDF exports with clean formatting

---

## **j. Settings***

- Storage location
- Interface complexity defaults
- Notifications / reminders
- Export / import project data
- Theme Switcher

## **j. User Profile***

    
---

### **1. Onboarding / First-Time User Flow**

**Goal:** Tailor the experience to the user’s self-build stage and comfort level.

- **Step 1: Welcome & Context**
    
    - Prompt: “Where are you in your self-build journey?”
        
        - Options: Dreaming / Just bought land / Planning permission / Mid-build
            
    - Optional short guide for beginners: “Self-build 101 in the UK”
        
- **Step 2: Experience Level**
    
    - “How detailed do you want your dashboard?”
        
        - Simple / Intermediate / Advanced
            
        - Sets progressive disclosure defaults
            
- **Step 3: Setup Basics**
    
    - Project name, location, start date, optional budget
        
    - Default storage: **SQLite local file**
        
- **Step 4: Quick Tutorial**
    
    - Highlight dashboard sections, explain expandable modules
        
    - Option to skip


---

# **3. Experience Principles (to anchor the UX)**

These help keep the app coherent:

1. **Clarity over complexity**  
    Give users only what they need at each step; hide complexity until needed.
    
2. **Calm interface, low cognitive load**  
    Especially important for people under stress or managing large projects for the first time.
    
3. **Progressive disclosure**  
    Don’t overwhelm people early — unfold details at the right time.
    
4. **UK-native language and structure**  
    Planning, regs, building stages — all should feel culturally and legally aligned.
    
5. **Inclusive design**
    
    - Clear labels
    - Consistent layout
    - High contrast modes
    - Dyslexia-aware typography options
    - Reduced motion
    - Keyboard/screen reader support
        
6. **Single source of truth**  
    Everything should live in one reliable, tidy place.
    
7. **Incremental Development Approach**

	1. Start with **Onboarding + Minimal Dashboard + Tasks**
	2. Add **Milestones + Budget**
	3. Add **Documents + AI Workbook**
	4. Implement **progressive disclosure + advanced features**

8. **Data Architecture (Offline-first)**

	- **SQLite file**, local, self-contained
	- Abstract database access (Repository pattern) to allow swapping DBs later
	- Suggested schema modules:
	    
	    - Projects
	    - Tasks
	    - Milestones
	    - Budget items
	    - Documents
	    - Notes / AI outputs


    ### **B. The Messy Middle – Managing Change**

Self-builds are **iteration marathons**. You need stronger change-management tools:

---

**Data Schema**

Spatial Structure (Rooms & Spaces)
Design Choices & Specifications
Materials & Procurement
Budget & Costs
Programme & Schedule
Quality & Inspections
Decisions & Risk Management
Documents & Media
Variations & Change Orders
Professional Team & Contractors
Communication & Meetings
Site Operations & Monitoring
User Learning & Knowledge Tracking
System Configuration & Metadata
Analytics & Reporting Views
LLM Reference Database - (Building regs etc)



**1. Enhanced Task Creation Modal**

- **Estimated Hours** - Track time estimates (decimal input: 8.5 hours)
- **Completion Percentage** - Visual progress (0-100% with validation)
- **Blocked By** - Track task dependencies (array field)
- Improved modal size with scrolling
- Enhanced validation with error messages

**2. Calendar View** 📅

- Monthly calendar grid showing tasks on due dates
- Navigate months (Previous/Next/Today buttons)
- Color-coded by priority (Urgent → Low)
- Shows 3 tasks per day + counter
- Today highlighted, overdue indicators
- Hover tooltips with full details
- Professional visual legend

**3. Timeline/Gantt View** 📊

- Visual timeline with horizontal duration bars
- Color-coded by status (To Do, In Progress, Blocked, Done)
- Completion progress overlay on bars
- Auto-scaling timeline
- Smart date markers (adapts to timeline length)
- Shows assignee and percentage on bars
- Sorted by start date

**4. Drag & Drop for Kanban** 🎯

- Drag tasks between columns to change status
- Visual feedback (semi-transparent, highlighted zones)
- Grip handle icon (⋮⋮) for drag indication
- "Drop here" messages
- Smooth animations
- Progress bars on cards
- Auto-saves changes

# Design principles (high level, non-negotiable)

- **Clarity first** — every screen answers: “what can I do here?” and “why does this matter?” at a glance.
- **Consistency** — single source of truth for spacing, typography, colour, controls and interaction states (hover/focus/disabled). Use tokens.
- **Progressive disclosure** — show only what’s needed; surface advanced/rare options in contextual panels.
- **Accessibility by default** — keyboard focus order, ARIA where needed, 4.5:1 contrast for body text, semantic markup.
- **Predictable patterns** — reuse a small set of interaction patterns (list, card, modal, drawer, toast). Users learn once.
- **Performance & responsiveness** — mobile-first styling; avoid heavy initial payloads; lazy load attachments and large lists.
    

---

# Core UI patterns & components (re-usable library)

Create a component library (design tokens + React/Vue/Svelte components). Keep each component small, documented, and testable.

Essential components:

- **Top bar / App shell** — app title, global search, user menu, global notifications.
- **Sidebar** — collapsible, shows projects/groups; supports quick create and filters, structured and elements aligned.
- **Board / View switcher** — segmented control to toggle Kanban / Gantt / List / Calendar / Timeline / Roadmap.
- **Task card (compact & expanded)** — title, status chip, due date, assignees, priority, quick actions. Clicking expands to task detail.
- **Task detail drawer** — full task metadata, comments, checklist, attachments, audit trail, history.
- **Sprint / Epic card** — shows progress bar, linked tasks, start/end dates.
- **Gantt row** — task bar, drag to resize, keyboard accessible adjustments.
- **Settings modal / Panel** — preferences, integrations, import/export CSV, user roles.
- **Create / Bulk-import** — CSV import UI with mapping step, row validation, preview, errors per-row.
- **Breadcrumb / context header** — shows where user is (Project → Sprint → Epic).
- **Notifications & toasts** — non-blocking success/error messages.
- **Confirmation & destructive actions** — modal with reason & undo where needed.
- **Empty states / onboarding** — teach the user what to do next with CTAs.
    

For each component include:

- Visuals (tokens), interaction states, a11y notes, responsive rules, and usage examples.
    

---

# Interaction & UX specifics (best practice)

- **View parity**: switching between Kanban / Gantt / List should not duplicate data — it’s the same dataset with different presentations. Edits sync live.
- **Drag & drop**: support pointer + keyboard (use aria-grabbed + up/down keys). Provide clear drop targets and snap/preview.
- **Inline editing**: allow quick changes on cards (status, assignee, dates) without opening drawer. Save optimistically, roll back on failure.
- **Bulk actions**: select multiple items for assign, move sprint, change status, delete, export. Show clear selection count.
- **Filtering & saved views**: multi-dimensional filtering (project, assignee, tag, due range). Allow saving custom views.
- **Task linking**: show parent/child relationships, blocked-by links, and epic membership. Visualise dependency arrows in Gantt and Roadmap.
- **Audit trail & comments**: show who changed what and when; support inline mentions and attachments.
- **Onboarding flow**: first-run checklist to create project, import sample tasks or CSV, and create a sprint.
    
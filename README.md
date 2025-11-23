# AvenStudio - Project Documentation Index

Welcome! This index helps you navigate all the documentation for AvenStudio.

---

## 📋 Quick Reference

**Project Name:** AvenStudio  
**Purpose:** Self-build project management platform for UK home builders  
**Technology:** Electron + Python + SQLite  
**Status:** Planning & Design Phase  

---

## 📚 Documentation Overview

### 1. **Aven-Studio-Design-Brief.md** ⭐ START HERE
**What it is:** Complete, consolidated design brief

**Contains:**
- Project overview and problem statement
- Brand identity and values
- Visual design system (colors, typography)
- User experience principles
- Target audience definition
- Full feature set with user stories
- Information architecture
- Technical approach (updated with final stack decision)
- Accessibility requirements
- Development phases
- UI specifications
- Content guidelines
- Success metrics

**When to use:** This is your single source of truth. Reference it for any design or development decision.

---

### 2. **Technical-Stack-Decision.md**
**What it is:** Deep dive into the technology stack choice

**Contains:**
- Why Electron + Python + SQLite was chosen
- Detailed explanation of each technology's role
- How they work together
- Alternatives considered and why they weren't chosen
- File structure and architecture
- Database schema overview
- Packaging and distribution details
- Development roadmap
- Common concerns addressed
- Learning resources

**When to use:** When you need to understand why technical decisions were made, or when explaining the architecture to others.

---

### 3. **Getting-Started-Guide.md**
**What it is:** Step-by-step development setup guide

**Contains:**
- Prerequisites (Node.js, Python, Git, VS Code)
- Complete project setup instructions
- Code examples for:
  - Electron setup
  - Basic UI structure
  - Python FastAPI backend
  - SQLite database configuration
- Testing instructions
- First feature implementation example
- Troubleshooting tips
- Resource links

**When to use:** When you're ready to start coding. Follow this guide to go from zero to working app.

---

## 🎯 How to Use This Documentation

### If you're just starting:
1. Read **Aven-Studio-Design-Brief.md** (sections 1-7) to understand the vision
2. Read **Technical-Stack-Decision.md** to understand the technical approach
3. Follow **Getting-Started-Guide.md** when ready to code

### If you're designing:
- Use **Aven-Studio-Design-Brief.md** sections 3 (Visual Design), 4 (UX Principles), and 10 (UI Specifications)
- Reference the color palette, typography, and component specifications

### If you're developing:
- Use **Getting-Started-Guide.md** for initial setup
- Reference **Technical-Stack-Decision.md** for architecture decisions
- Use **Aven-Studio-Design-Brief.md** section 8 for database schema

### If you're planning features:
- Use **Aven-Studio-Design-Brief.md** section 6 (Feature Set & User Stories)
- Reference section 7 (Information Architecture)

---

## ✅ Key Decisions Made

These decisions are FINAL and documented:

**Brand:**
- ✅ Name: **AvenStudio**
- ✅ Typography: **DM Sans** throughout (no serif)
- ✅ Dyslexia-friendly toggle available
- ✅ Color palette: Navy, Bronze, Mint, Sand (+ semantic colors)

**Technology:**
- ✅ **Electron** for desktop shell
- ✅ **Python + FastAPI** for backend
- ✅ **SQLite** for data storage
- ✅ **Offline-first** architecture
- ✅ Packaged as **.exe** (Windows) and **.app** (macOS)

**User Experience:**
- ✅ Progressive disclosure (simple by default, advanced when needed)
- ✅ Accessibility by default (WCAG AA compliance)
- ✅ Calm, warm, professional aesthetic
- ✅ UK-specific language and workflows

---

## ⏳ Open Questions

These still need decisions:

**Features:**
- Which features are MVP vs Phase 2?
- How much AI assistance in early versions?
- Budget categories: pre-defined or fully custom?

**User Experience:**
- Onboarding flow: quick start vs comprehensive setup?
- Default dashboard layout: simple vs detailed?

**Business:**
- Pricing model?
- Beta testing approach?
- Target launch date?

---

## 📁 Original Source Documents

These were used to create the consolidated documentation:

1. **Aven Studio - Brand.md** - Original brand thinking
2. **Aven Studio - Project Outline.md** - Feature epics and UX flows
3. **Aven Concept Planning.md** - User stories and workflows
4. **selfbuild-dashboard.html** - Visual mockup (used Ground+Flow branding)
5. **selfbuild-timeline.html** - Visual mockup (used Ground+Flow branding)

**Note:** The HTML mockups explored "Ground+Flow" as a name, but the actual product is **AvenStudio**.

---

## 🚀 Getting Started Checklist

Ready to build? Here's your checklist:

**Planning:**
- [ ] Read complete design brief
- [ ] Understand target users
- [ ] Review feature priorities

**Setup:**
- [ ] Install Node.js
- [ ] Install Python 3.11+
- [ ] Install Git
- [ ] Install VS Code
- [ ] Install DM Sans font locally

**Development:**
- [ ] Follow Getting Started Guide
- [ ] Set up project structure
- [ ] Initialize Electron
- [ ] Set up Python backend
- [ ] Create SQLite database
- [ ] Test everything works

**First Feature:**
- [ ] Build task creation (full stack)
- [ ] Test end-to-end
- [ ] Celebrate! 🎉

---

## 📞 Need Help?

**Documentation unclear?**
- Review the relevant section again
- Check the Getting Started Guide troubleshooting section
- Search the official docs (linked in each guide)

**Technical questions?**
- Stack Overflow (electron, fastapi, python tags)
- Official Discord servers (Electron, FastAPI)

**Design questions?**
- Reference the design brief
- Review the HTML mockups for visual examples
- Check WCAG guidelines for accessibility

---

## 🔄 Document Versions

**Version 1.0** - November 2025
- Initial consolidated design brief
- Technical stack decision documented
- Getting started guide created
- All Ground+Flow references removed
- Typography updated to DM Sans only
- Technology stack finalized

---

## 📝 Maintaining These Docs

**When to update:**
- New features are planned
- Technology decisions change
- Design system evolves
- User feedback requires changes

**How to update:**
- Edit the relevant .md file
- Update version number
- Document what changed and why
- Keep this index in sync

---

**Everything you need to build AvenStudio is in these documents. Take your time, work through them systematically, and you'll have a great foundation for development.**

Good luck! 🏗️

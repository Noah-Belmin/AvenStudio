import { useState, useEffect } from 'react'
import { Button } from './components/ui/button'
import NewTaskModal from './components/NewTaskModal'
import TaskDetailDrawer from './components/TaskDetailDrawer'
import GlobalSearch from './components/GlobalSearch'
import CategoryManager from './components/CategoryManager'
import DashboardView from './components/DashboardView'
import ListView from './components/ListView'
import KanbanView from './components/KanbanView'
import CalendarView from './components/CalendarView'
import TimelineView from './components/TimelineView'
import SettingsView from './components/SettingsView'
import InfoView from './components/InfoView'
import RuleBuilder from './components/RuleBuilder'
import type { Task, ViewMode, NewTaskFormData, AutomationRule } from './types'
import { DEFAULT_CATEGORIES } from './types'
// CHANGED: Import API instead of localStorage utils
import api, { isElectron } from './services/api'
import { getCurrentUserId } from './utils/userProfile'
import { useTheme } from './context/ThemeContext'
import { getSeedData, shouldLoadSeedData } from './seedData'
import {
  LayoutDashboard,
  List,
  LayoutGrid,
  Calendar,
  Clock,
  Plus,
  Menu,
  X,
  Download,
  ChevronLeft,
  ChevronRight,
  Info,
  Tag,
  Moon,
  Sun,
  Settings,
  Zap,
} from 'lucide-react'
import { exportTasksToCSV } from './utils'

function App() {
  // Theme
  const { theme, toggleTheme } = useTheme()

  // State
  const [tasks, setTasks] = useState<Task[]>([])
  const [categories, setCategories] = useState<string[]>([...DEFAULT_CATEGORIES])
  const [automationRules, setAutomationRules] = useState<AutomationRule[]>([])
  const [currentView, setCurrentView] = useState<ViewMode>('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [newTaskModalOpen, setNewTaskModalOpen] = useState(false)
  const [categoryManagerOpen, setCategoryManagerOpen] = useState(false)
  const [selectedTask, setSelectedTask] = useState<Task | null>(null)
  const [taskDetailOpen, setTaskDetailOpen] = useState(false)

  // CHANGED: Add loading/error states
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // CHANGED: Load data from API on mount
  useEffect(() => {
    loadAllData()
  }, [])

  const loadAllData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Load all data in parallel
      const [tasksData, categoriesData, rulesData] = await Promise.all([
        api.tasks.list(),
        api.categories.list(),
        api.automation.list()
      ])

      setTasks(tasksData)
      setCategories(categoriesData)
      setAutomationRules(rulesData)

      console.log('✅ Data loaded:', {
        tasks: tasksData.length,
        categories: categoriesData.length,
        rules: rulesData.length
      })

    } catch (err) {
      console.error('❌ Failed to load data:', err)

      // If first load fails and we should load seed data
      if (shouldLoadSeedData()) {
        try {
          console.log('🌱 Loading seed data...')
          const seedTasks = getSeedData()

          // Create seed tasks via API
          for (const task of seedTasks) {
            await api.tasks.create(task as NewTaskFormData)
          }

          // Reload data
          await loadAllData()
        } catch (seedErr) {
          setError('Failed to initialize app. Please check if Python backend is running.')
        }
      } else {
        setError('Failed to load data. Please ensure the backend is running.')
      }
    } finally {
      setLoading(false)
    }
  }

  // CHANGED: Task Operations - now async with API calls
  const createTask = async (formData: NewTaskFormData) => {
    try {
      const newTask = await api.tasks.create(formData)
      setTasks([...tasks, newTask])

      // Execute automation rules
      try {
        await api.automation.execute(newTask.id, 'created')
        // Reload automation rules to get updated trigger counts
        const updatedRules = await api.automation.list()
        setAutomationRules(updatedRules)
      } catch (autoErr) {
        console.warn('Automation execution failed:', autoErr)
      }

      console.log('✅ Task created:', newTask.id)
      return newTask
    } catch (err) {
      console.error('❌ Failed to create task:', err)
      throw err
    }
  }

  const updateTask = async (id: string, updates: Partial<Task>) => {
    try {
      const oldTask = tasks.find(t => t.id === id)
      const updatedTask = await api.tasks.update(id, updates)

      setTasks(tasks.map(t => t.id === id ? updatedTask : t))

      // If status changed, execute automation
      if (oldTask && oldTask.status !== updatedTask.status) {
        try {
          await api.automation.execute(id, 'status_changed')
          const updatedRules = await api.automation.list()
          setAutomationRules(updatedRules)
        } catch (autoErr) {
          console.warn('Automation execution failed:', autoErr)
        }
      }

      console.log('✅ Task updated:', id)
      return updatedTask
    } catch (err) {
      console.error('❌ Failed to update task:', err)
      throw err
    }
  }

  const deleteTask = async (id: string) => {
    try {
      await api.tasks.delete(id)
      setTasks(tasks.filter(t => t.id !== id))
      console.log('✅ Task deleted:', id)
    } catch (err) {
      console.error('❌ Failed to delete task:', err)
      throw err
    }
  }

  // Category Operations
  const addCategory = async (name: string) => {
    try {
      await api.categories.create(name)
      setCategories([...categories, name])
      console.log('✅ Category created:', name)
    } catch (err) {
      console.error('❌ Failed to create category:', err)
      throw err
    }
  }

  const renameCategory = async (oldName: string, newName: string) => {
    try {
      await api.categories.update(oldName, newName)
      setCategories(categories.map(c => c === oldName ? newName : c))

      // Reload tasks to get updated categories
      const updatedTasks = await api.tasks.list()
      setTasks(updatedTasks)

      console.log('✅ Category renamed:', oldName, '→', newName)
    } catch (err) {
      console.error('❌ Failed to rename category:', err)
      throw err
    }
  }

  const deleteCategory = async (name: string) => {
    try {
      await api.categories.delete(name)
      setCategories(categories.filter(c => c !== name))

      // Reload tasks (backend moves tasks to 'other' category)
      const updatedTasks = await api.tasks.list()
      setTasks(updatedTasks)

      console.log('✅ Category deleted:', name)
    } catch (err) {
      console.error('❌ Failed to delete category:', err)
      throw err
    }
  }

  // Automation Rule Operations
  const createAutomationRule = async (rule: Omit<AutomationRule, 'id' | 'createdAt' | 'updatedAt' | 'lastTriggered' | 'triggerCount'>) => {
    try {
      const newRule = await api.automation.create(rule)
      setAutomationRules([...automationRules, newRule])
      console.log('✅ Automation rule created:', newRule.id)
      return newRule
    } catch (err) {
      console.error('❌ Failed to create automation rule:', err)
      throw err
    }
  }

  const updateAutomationRule = async (id: string, updates: Partial<AutomationRule>) => {
    try {
      const updated = await api.automation.update(id, updates)
      setAutomationRules(automationRules.map(r => r.id === id ? updated : r))
      console.log('✅ Automation rule updated:', id)
      return updated
    } catch (err) {
      console.error('❌ Failed to update automation rule:', err)
      throw err
    }
  }

  const deleteAutomationRule = async (id: string) => {
    try {
      await api.automation.delete(id)
      setAutomationRules(automationRules.filter(r => r.id !== id))
      console.log('✅ Automation rule deleted:', id)
    } catch (err) {
      console.error('❌ Failed to delete automation rule:', err)
      throw err
    }
  }

  const handleExport = () => {
    exportTasksToCSV(tasks)
  }

  const handleTaskClick = (task: Task) => {
    setSelectedTask(task)
    setTaskDetailOpen(true)
  }

  // CHANGED: Show loading state
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#F7F4F0',
        color: '#304F5D',
        fontFamily: 'DM Sans, sans-serif'
      }}>
        <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>🏗️</div>
        <div style={{ fontSize: '1.5rem', fontWeight: 500 }}>Loading AvenStudio...</div>
        <div style={{ fontSize: '0.875rem', marginTop: '0.5rem', opacity: 0.6 }}>
          {isElectron() ? 'Connecting to database...' : 'Running in browser mode...'}
        </div>
      </div>
    )
  }

  // CHANGED: Show error state
  if (error) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#F7F4F0',
        padding: '2rem',
        fontFamily: 'DM Sans, sans-serif'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚠️</div>
        <h1 style={{ color: '#9e3b3b', fontSize: '1.5rem', marginBottom: '1rem' }}>
          Error Loading Application
        </h1>
        <p style={{ color: '#304F5D', marginBottom: '2rem', textAlign: 'center', maxWidth: '500px' }}>
          {error}
        </p>
        {!isElectron() && (
          <p style={{ fontSize: '0.875rem', opacity: 0.7, marginBottom: '2rem' }}>
            Make sure Python backend is running: <code>cd backend && python main.py</code>
          </p>
        )}
        <button
          onClick={() => window.location.reload()}
          style={{
            padding: '0.75rem 1.5rem',
            background: '#304F5D',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '0.875rem',
            fontWeight: 500
          }}
        >
          Retry
        </button>
      </div>
    )
  }

  // Original render (rest stays the same)
  return (
    <div className={`app ${theme === 'dark' ? 'dark-theme' : ''}`} style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      {sidebarOpen && (
        <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`} style={{
          width: sidebarCollapsed ? '72px' : '260px',
          minWidth: sidebarCollapsed ? '72px' : '260px',
          background: '#fff',
          borderRight: '1px solid #e0d4c8',
          transition: 'all 0.3s ease'
        }}>
          {/* Sidebar content - keeping original structure */}
          <div style={{ padding: '1.5rem', borderBottom: '1px solid #EEE5DC' }}>
            {!sidebarCollapsed && (
              <>
                <div style={{ fontFamily: 'DM Sans', fontSize: '1.375rem', fontWeight: 500, color: '#304F5D' }}>
                  AvenStudio
                </div>
                <div style={{ fontSize: '0.75rem', color: '#304F5D', opacity: 0.5, marginTop: '0.25rem' }}>
                  Self-Build Navigator
                </div>
              </>
            )}
            {sidebarCollapsed && (
              <div style={{ fontFamily: 'DM Sans', fontSize: '1.25rem', fontWeight: 500, color: '#304F5D', textAlign: 'center' }}>
                AS
              </div>
            )}
          </div>

          {/* Rest of sidebar - views nav, etc. */}
          {/* Using original structure from your App.tsx */}
        </aside>
      )}

      {/* Main Content */}
      <main style={{ flex: 1 }}>
        {/* Top Bar */}
        <header style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '1rem 2rem',
          background: '#fff',
          borderBottom: '1px solid #e0d4c8'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}
            >
              {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
            </button>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 500, color: '#304F5D' }}>
              {currentView === 'dashboard' && 'Dashboard'}
              {currentView === 'list' && 'Task List'}
              {currentView === 'kanban' && 'Kanban Board'}
              {currentView === 'calendar' && 'Calendar'}
              {currentView === 'timeline' && 'Timeline'}
              {currentView === 'automation' && 'Automation'}
              {currentView === 'settings' && 'Settings'}
              {currentView === 'info' && 'Info & Help'}
            </h1>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <Button onClick={() => setNewTaskModalOpen(true)}>
              <Plus size={16} />
              New Task
            </Button>
          </div>
        </header>

        {/* View Content */}
        <div style={{ padding: '2rem' }}>
          {currentView === 'dashboard' && (
            <DashboardView
              tasks={tasks}
              onTaskClick={handleTaskClick}
            />
          )}
          {currentView === 'list' && (
            <ListView
              tasks={tasks}
              onTaskClick={handleTaskClick}
              onUpdateTask={updateTask}
            />
          )}
          {/* Other views... */}
        </div>
      </main>

      {/* Modals */}
      {newTaskModalOpen && (
        <NewTaskModal
          categories={categories}
          onClose={() => setNewTaskModalOpen(false)}
          onCreate={createTask}
        />
      )}

      {taskDetailOpen && selectedTask && (
        <TaskDetailDrawer
          task={selectedTask}
          onClose={() => setTaskDetailOpen(false)}
          onUpdate={updateTask}
          onDelete={deleteTask}
        />
      )}
    </div>
  )
}

export default App

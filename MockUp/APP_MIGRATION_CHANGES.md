# App.tsx Migration Changes

This document shows the key changes needed to adapt App.tsx from localStorage to API-based storage.

## Changes Required

### 1. Import API instead of utils

**REMOVE:**
```typescript
import { saveToLocalStorage, loadFromLocalStorage } from './utils'
```

**ADD:**
```typescript
import api from './services/api'
```

### 2. Update useEffect for loading data

**REPLACE:**
```typescript
// Load data from localStorage on mount
useEffect(() => {
  const savedData = loadFromLocalStorage()
  if (savedData) {
    if (savedData.tasks) {
      setTasks(savedData.tasks)
    }
    if (savedData.categories) {
      setCategories(savedData.categories)
    }
    if (savedData.automationRules) {
      setAutomationRules(savedData.automationRules)
    }
  } else if (shouldLoadSeedData()) {
    const seedTasks = getSeedData()
    setTasks(seedTasks)
    saveToLocalStorage({ tasks: seedTasks, categories: DEFAULT_CATEGORIES, automationRules: [] })
  }
  setIsInitialLoad(false)
}, [])
```

**WITH:**
```typescript
// Load data from API on mount
useEffect(() => {
  loadAllData()
}, [])

const loadAllData = async () => {
  try {
    const [tasksData, categoriesData, rulesData] = await Promise.all([
      api.tasks.list(),
      api.categories.list(),
      api.automation.list()
    ])

    setTasks(tasksData)
    setCategories(categoriesData)
    setAutomationRules(rulesData)
  } catch (error) {
    console.error('Failed to load data:', error)
    // Fallback to seed data on first run
    if (shouldLoadSeedData()) {
      const seedTasks = getSeedData()
      // Create tasks via API
      for (const task of seedTasks) {
        await api.tasks.create(task)
      }
      await loadAllData() // Reload from API
    }
  } finally {
    setIsInitialLoad(false)
  }
}
```

### 3. REMOVE localStorage save effect

**DELETE THIS:**
```typescript
// Save to localStorage whenever tasks or categories change
useEffect(() => {
  if (!isInitialLoad) {
    saveToLocalStorage({ tasks, categories, automationRules })
  }
}, [tasks, categories, automationRules, isInitialLoad])
```

### 4. Update createTask to use API

**REPLACE:**
```typescript
const createTask = (formData: NewTaskFormData) => {
  const newTask: Task = {
    id: crypto.randomUUID(),
    title: formData.title,
    description: formData.description,
    status: 'todo',
    priority: formData.priority,
    category: formData.category,
    tags: formData.tags,
    dueDate: formData.dueDate,
    startDate: formData.startDate,
    assignedTo: formData.assignedTo,
    estimatedHours: formData.estimatedHours,
    completionPercentage: formData.completionPercentage || 0,
    blockedBy: formData.blockedBy || [],
    createdAt: new Date(),
    updatedAt: new Date(),
    createdBy: getCurrentUserId(),
    comments: [],
    attachments: [],
    checklist: [],
    subtasks: [],
    customFields: {}
  }

  setTasks([...tasks, newTask])

  // Execute automation rules
  const triggeredRules = executeAutomationRules(newTask, automationRules, 'created')
  // ... automation logic
}
```

**WITH:**
```typescript
const createTask = async (formData: NewTaskFormData) => {
  try {
    const newTask = await api.tasks.create(formData)
    setTasks([...tasks, newTask])

    // Execute automation rules
    try {
      await api.automation.execute(newTask.id, 'created')
    } catch (error) {
      console.warn('Automation execution failed:', error)
      // Non-critical, continue
    }

    return newTask
  } catch (error) {
    console.error('Failed to create task:', error)
    throw error
  }
}
```

### 5. Update updateTask to use API

**REPLACE:**
```typescript
const updateTask = (id: string, updates: Partial<Task>) => {
  const taskIndex = tasks.findIndex(t => t.id === id)
  if (taskIndex === -1) return

  const existingTask = tasks[taskIndex]
  const updatedTask = {
    ...existingTask,
    ...updates,
    updatedAt: new Date()
  }

  const newTasks = [...tasks]
  newTasks[taskIndex] = updatedTask
  setTasks(newTasks)

  // Automation rules...
}
```

**WITH:**
```typescript
const updateTask = async (id: string, updates: Partial<Task>) => {
  try {
    const updatedTask = await api.tasks.update(id, updates)

    setTasks(tasks.map(t => t.id === id ? updatedTask : t))

    // Check if status changed for automation
    const oldTask = tasks.find(t => t.id === id)
    if (oldTask && oldTask.status !== updatedTask.status) {
      try {
        await api.automation.execute(id, 'status_changed')
      } catch (error) {
        console.warn('Automation execution failed:', error)
      }
    }

    return updatedTask
  } catch (error) {
    console.error('Failed to update task:', error)
    throw error
  }
}
```

### 6. Update deleteTask to use API

**REPLACE:**
```typescript
const deleteTask = (id: string) => {
  setTasks(tasks.filter(t => t.id !== id))
}
```

**WITH:**
```typescript
const deleteTask = async (id: string) => {
  try {
    await api.tasks.delete(id)
    setTasks(tasks.filter(t => t.id !== id))
  } catch (error) {
    console.error('Failed to delete task:', error)
    throw error
  }
}
```

### 7. Update category operations

**REPLACE:**
```typescript
const addCategory = (name: string) => {
  if (!categories.includes(name)) {
    setCategories([...categories, name])
  }
}

const deleteCategory = (name: string) => {
  setCategories(categories.filter(c => c !== name))
  // Update tasks...
}
```

**WITH:**
```typescript
const addCategory = async (name: string) => {
  try {
    await api.categories.create(name)
    setCategories([...categories, name])
  } catch (error) {
    console.error('Failed to create category:', error)
    throw error
  }
}

const deleteCategory = async (name: string) => {
  try {
    await api.categories.delete(name)
    setCategories(categories.filter(c => c !== name))

    // Update tasks with this category
    const affectedTasks = tasks.filter(t => t.category === name)
    for (const task of affectedTasks) {
      await api.tasks.update(task.id, { category: 'other' })
    }

    // Reload tasks
    const updatedTasks = await api.tasks.list()
    setTasks(updatedTasks)
  } catch (error) {
    console.error('Failed to delete category:', error)
    throw error
  }
}
```

### 8. Update automation rule operations

**REPLACE:**
```typescript
const createAutomationRule = (rule: Omit<AutomationRule, 'id' | 'createdAt' | 'updatedAt' | 'lastTriggered' | 'triggerCount'>) => {
  const newRule: AutomationRule = {
    ...rule,
    id: crypto.randomUUID(),
    createdAt: new Date(),
    updatedAt: new Date(),
    triggerCount: 0
  }
  setAutomationRules([...automationRules, newRule])
}
```

**WITH:**
```typescript
const createAutomationRule = async (rule: Omit<AutomationRule, 'id' | 'createdAt' | 'updatedAt' | 'lastTriggered' | 'triggerCount'>) => {
  try {
    const newRule = await api.automation.create(rule)
    setAutomationRules([...automationRules, newRule])
    return newRule
  } catch (error) {
    console.error('Failed to create automation rule:', error)
    throw error
  }
}
```

### 9. Add loading states

**ADD:**
```typescript
const [loading, setLoading] = useState(true)
const [error, setError] = useState<string | null>(null)
```

**UPDATE render:**
```typescript
if (loading) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      fontSize: '1.5rem',
      color: '#304F5D'
    }}>
      Loading AvenStudio...
    </div>
  )
}

if (error) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      padding: '2rem'
    }}>
      <h1 style={{ color: '#9e3b3b' }}>Error Loading Application</h1>
      <p style={{ color: '#304F5D', marginTop: '1rem' }}>{error}</p>
      <button
        onClick={() => window.location.reload()}
        style={{
          marginTop: '2rem',
          padding: '0.75rem 1.5rem',
          background: '#304F5D',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer'
        }}
      >
        Retry
      </button>
    </div>
  )
}
```

### 10. Update component callbacks

All components that use task operations need to handle async:

**In NewTaskModal:**
```typescript
const handleSubmit = async (formData: NewTaskFormData) => {
  try {
    await createTask(formData)
    setNewTaskModalOpen(false)
  } catch (error) {
    // Show error toast/notification
    console.error('Failed to create task:', error)
  }
}
```

**In TaskDetailDrawer:**
```typescript
const handleUpdateTask = async (updates: Partial<Task>) => {
  try {
    await updateTask(selectedTask.id, updates)
  } catch (error) {
    console.error('Failed to update task:', error)
  }
}

const handleDeleteTask = async () => {
  try {
    await deleteTask(selectedTask.id)
    setTaskDetailOpen(false)
  } catch (error) {
    console.error('Failed to delete task:', error)
  }
}
```

## Summary

Key changes:
1. ✅ Import `api` instead of `utils`
2. ✅ Load data from API on mount (async)
3. ✅ Remove localStorage save effect
4. ✅ Make all CRUD operations `async`
5. ✅ Add `try/catch` error handling
6. ✅ Add loading states
7. ✅ Update all callbacks to handle async

All UI components stay the same - only the data layer changes!

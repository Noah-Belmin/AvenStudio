/**
 * API Client for AvenStudio
 * Communicates with Python FastAPI backend via Electron preload bridge
 * Replaces localStorage with real database persistence
 */

import type { Task, NewTaskFormData, AutomationRule } from '../types'

/**
 * Electron API interface (injected by preload.js)
 */
interface ElectronAPI {
  tasks: {
    list: (filters?: {
      status?: string
      priority?: string
      category?: string
    }) => Promise<Task[]>
    get: (id: string) => Promise<Task>
    create: (data: NewTaskFormData) => Promise<Task>
    update: (id: string, data: Partial<Task>) => Promise<Task>
    delete: (id: string) => Promise<void>
  }
  stats: {
    get: () => Promise<{
      total_tasks: number
      in_progress: number
      completed: number
      blocked: number
      completion_rate: number
      by_priority: Record<string, number>
      by_category: Record<string, number>
      overdue: number
      due_soon: number
    }>
  }
  categories: {
    list: () => Promise<string[]>
    create: (name: string) => Promise<{ name: string }>
    update: (oldName: string, newName: string) => Promise<{ name: string }>
    delete: (name: string) => Promise<void>
  }
  automation: {
    list: () => Promise<AutomationRule[]>
    get: (id: string) => Promise<AutomationRule>
    create: (rule: Omit<AutomationRule, 'id' | 'createdAt' | 'updatedAt'>) => Promise<AutomationRule>
    update: (id: string, rule: Partial<AutomationRule>) => Promise<AutomationRule>
    delete: (id: string) => Promise<void>
    execute: (taskId: string, trigger: string) => Promise<void>
  }
  system: {
    health: () => Promise<{ status: string; version: string }>
    ping: () => Promise<boolean>
  }
}

interface ElectronEnv {
  isElectron: boolean
  platform: string
  apiBaseUrl: string
}

/**
 * Extend Window interface to include Electron API
 */
declare global {
  interface Window {
    api: ElectronAPI
    env: ElectronEnv
  }
}

/**
 * Check if running in Electron environment
 */
export function isElectron(): boolean {
  return typeof window !== 'undefined' &&
         typeof window.api !== 'undefined' &&
         typeof window.env !== 'undefined' &&
         window.env.isElectron === true
}

/**
 * Development fallback API (uses localStorage when not in Electron)
 * This allows development in browser without Electron
 */
const devAPI: ElectronAPI = {
  tasks: {
    list: async (filters) => {
      const saved = localStorage.getItem('tasks')
      let tasks: Task[] = saved ? JSON.parse(saved) : []

      // Apply filters
      if (filters?.status) {
        tasks = tasks.filter(t => t.status === filters.status)
      }
      if (filters?.priority) {
        tasks = tasks.filter(t => t.priority === filters.priority)
      }
      if (filters?.category) {
        tasks = tasks.filter(t => t.category === filters.category)
      }

      return tasks
    },

    get: async (id) => {
      const saved = localStorage.getItem('tasks')
      const tasks: Task[] = saved ? JSON.parse(saved) : []
      const task = tasks.find(t => t.id === id)
      if (!task) throw new Error('Task not found')
      return task
    },

    create: async (data) => {
      const saved = localStorage.getItem('tasks')
      const tasks: Task[] = saved ? JSON.parse(saved) : []

      const newTask: Task = {
        id: crypto.randomUUID(),
        ...data,
        status: 'todo',
        tags: data.tags || [],
        comments: [],
        attachments: [],
        checklist: [],
        subtasks: [],
        customFields: {},
        createdAt: new Date(),
        updatedAt: new Date()
      }

      tasks.push(newTask)
      localStorage.setItem('tasks', JSON.stringify(tasks))
      return newTask
    },

    update: async (id, data) => {
      const saved = localStorage.getItem('tasks')
      const tasks: Task[] = saved ? JSON.parse(saved) : []
      const index = tasks.findIndex(t => t.id === id)

      if (index === -1) throw new Error('Task not found')

      const updated = {
        ...tasks[index],
        ...data,
        updatedAt: new Date()
      }

      tasks[index] = updated
      localStorage.setItem('tasks', JSON.stringify(tasks))
      return updated
    },

    delete: async (id) => {
      const saved = localStorage.getItem('tasks')
      const tasks: Task[] = saved ? JSON.parse(saved) : []
      const filtered = tasks.filter(t => t.id !== id)
      localStorage.setItem('tasks', JSON.stringify(filtered))
    }
  },

  stats: {
    get: async () => {
      const saved = localStorage.getItem('tasks')
      const tasks: Task[] = saved ? JSON.parse(saved) : []

      const stats = {
        total_tasks: tasks.length,
        in_progress: tasks.filter(t => t.status === 'in-progress').length,
        completed: tasks.filter(t => t.status === 'done').length,
        blocked: tasks.filter(t => t.status === 'blocked').length,
        completion_rate: tasks.length > 0
          ? Math.round((tasks.filter(t => t.status === 'done').length / tasks.length) * 100)
          : 0,
        by_priority: tasks.reduce((acc, t) => {
          acc[t.priority] = (acc[t.priority] || 0) + 1
          return acc
        }, {} as Record<string, number>),
        by_category: tasks.reduce((acc, t) => {
          acc[t.category] = (acc[t.category] || 0) + 1
          return acc
        }, {} as Record<string, number>),
        overdue: tasks.filter(t => t.dueDate && new Date(t.dueDate) < new Date() && t.status !== 'done').length,
        due_soon: tasks.filter(t => {
          if (!t.dueDate || t.status === 'done') return false
          const due = new Date(t.dueDate)
          const soon = new Date()
          soon.setDate(soon.getDate() + 7)
          return due <= soon && due >= new Date()
        }).length
      }

      return stats
    }
  },

  categories: {
    list: async () => {
      const saved = localStorage.getItem('categories')
      return saved ? JSON.parse(saved) : ['work', 'personal', 'health', 'learning', 'construction', 'other']
    },

    create: async (name) => {
      const saved = localStorage.getItem('categories')
      const categories: string[] = saved ? JSON.parse(saved) : []
      if (!categories.includes(name)) {
        categories.push(name)
        localStorage.setItem('categories', JSON.stringify(categories))
      }
      return { name }
    },

    update: async (oldName, newName) => {
      const saved = localStorage.getItem('categories')
      const categories: string[] = saved ? JSON.parse(saved) : []
      const index = categories.indexOf(oldName)
      if (index !== -1) {
        categories[index] = newName
        localStorage.setItem('categories', JSON.stringify(categories))
      }
      return { name: newName }
    },

    delete: async (name) => {
      const saved = localStorage.getItem('categories')
      const categories: string[] = saved ? JSON.parse(saved) : []
      const filtered = categories.filter(c => c !== name)
      localStorage.setItem('categories', JSON.stringify(filtered))
    }
  },

  automation: {
    list: async () => {
      const saved = localStorage.getItem('automationRules')
      return saved ? JSON.parse(saved) : []
    },

    get: async (id) => {
      const saved = localStorage.getItem('automationRules')
      const rules: AutomationRule[] = saved ? JSON.parse(saved) : []
      const rule = rules.find(r => r.id === id)
      if (!rule) throw new Error('Rule not found')
      return rule
    },

    create: async (data) => {
      const saved = localStorage.getItem('automationRules')
      const rules: AutomationRule[] = saved ? JSON.parse(saved) : []

      const newRule: AutomationRule = {
        ...data,
        id: crypto.randomUUID(),
        createdAt: new Date(),
        updatedAt: new Date(),
        triggerCount: 0
      } as AutomationRule

      rules.push(newRule)
      localStorage.setItem('automationRules', JSON.stringify(rules))
      return newRule
    },

    update: async (id, data) => {
      const saved = localStorage.getItem('automationRules')
      const rules: AutomationRule[] = saved ? JSON.parse(saved) : []
      const index = rules.findIndex(r => r.id === id)

      if (index === -1) throw new Error('Rule not found')

      rules[index] = {
        ...rules[index],
        ...data,
        updatedAt: new Date()
      }

      localStorage.setItem('automationRules', JSON.stringify(rules))
      return rules[index]
    },

    delete: async (id) => {
      const saved = localStorage.getItem('automationRules')
      const rules: AutomationRule[] = saved ? JSON.parse(saved) : []
      const filtered = rules.filter(r => r.id !== id)
      localStorage.setItem('automationRules', JSON.stringify(filtered))
    },

    execute: async (taskId, trigger) => {
      console.log('Automation executed:', taskId, trigger)
      // In dev mode, this is a no-op
    }
  },

  system: {
    health: async () => ({
      status: 'ok (dev mode)',
      version: '0.1.0-dev'
    }),

    ping: async () => true
  }
}

/**
 * Export API client
 * Uses Electron API if available, falls back to dev API (localStorage)
 */
const api = isElectron() ? window.api : devAPI

export default api

/**
 * Export individual APIs for convenience
 */
export const { tasks, stats, categories, automation, system } = api

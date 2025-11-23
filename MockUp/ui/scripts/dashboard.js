/**
 * AvenStudio Dashboard Logic
 * Vanilla JavaScript implementation - loads data from API and updates DOM
 */

// ==================== STATE ====================

let allTasks = [];
let stats = null;

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', async () => {
  console.log('🏗️ AvenStudio Dashboard initializing...');

  // Check if API is available
  if (typeof window.avenAPI === 'undefined') {
    console.error('❌ window.avenAPI is not defined! Check if api.js loaded correctly.');
    showError('API not loaded. Please refresh the page.');
    return;
  }

  // Check if we're in Electron
  const isElectron = typeof window.api !== 'undefined';
  console.log('📱 Running in:', isElectron ? 'Electron' : 'Browser');

  if (isElectron) {
    console.log('✅ window.api available from Electron preload');
  } else {
    console.log('⚠️ Using localStorage fallback (browser mode)');
  }

  // Load all data
  await loadDashboardData();

  // Set up event listeners
  setupEventListeners();

  console.log('✅ Dashboard ready!');
});

// ==================== DATA LOADING ====================

async function loadDashboardData() {
  try {
    console.log('📡 Fetching stats and tasks...');

    // Load stats and tasks in parallel
    const [statsData, tasksData] = await Promise.all([
      window.avenAPI.getStats(),
      window.avenAPI.getTasks()
    ]);

    stats = statsData;
    allTasks = tasksData;

    console.log('📊 Loaded successfully!');
    console.log('  - Stats:', stats);
    console.log('  - Tasks:', allTasks.length, 'tasks');

    // Update UI
    updateStatsCards();
    updateSidebarStats();
    updateProgressBar();
    updateHighPriorityTasks();
    updateUpcomingTasks();

  } catch (error) {
    console.error('❌ Failed to load dashboard data:', error);
    console.error('Error details:', error.message, error.stack);
    showError(`Failed to load data: ${error.message}`);
  }
}

// ==================== UI UPDATES ====================

function updateStatsCards() {
  // Total tasks
  document.getElementById('stat-total').textContent = stats.total_tasks;

  // In progress
  const inProgress = stats.by_status['in-progress'] || 0;
  document.getElementById('stat-inprogress').textContent = inProgress;

  // Completed
  const completed = stats.by_status['done'] || 0;
  document.getElementById('stat-completed').textContent = completed;

  // Completion rate
  const completionRate = stats.completion_rate || 0;
  document.getElementById('stat-completion-rate').textContent =
    `${completionRate}% completion rate`;

  // Blocked
  const blocked = stats.by_status['blocked'] || 0;
  document.getElementById('stat-blocked').textContent = blocked;
}

function updateSidebarStats() {
  document.getElementById('sidebar-total').textContent = stats.total_tasks;
  document.getElementById('sidebar-inprogress').textContent =
    stats.by_status['in-progress'] || 0;
  document.getElementById('sidebar-completed').textContent =
    stats.by_status['done'] || 0;
}

function updateProgressBar() {
  const completionRate = stats.completion_rate || 0;

  document.getElementById('progress-subtitle').textContent =
    `You've completed ${completionRate}% of all tasks`;

  const progressBar = document.getElementById('progressBar');

  // Animate progress bar
  setTimeout(() => {
    progressBar.style.width = `${completionRate}%`;
  }, 100);
}

function updateHighPriorityTasks() {
  // Filter high/urgent priority tasks that aren't done
  const highPriorityTasks = allTasks.filter(task =>
    (task.priority === 'high' || task.priority === 'urgent') &&
    task.status !== 'done'
  ).slice(0, 4); // Show top 4

  const container = document.getElementById('highPriorityTasks');
  const countLabel = document.getElementById('high-priority-count');

  countLabel.textContent = `${highPriorityTasks.length} tasks need attention`;

  if (highPriorityTasks.length === 0) {
    container.innerHTML = '<p style="opacity: 0.5; text-align: center; padding: 2rem;">No high priority tasks</p>';
    return;
  }

  container.innerHTML = highPriorityTasks.map(task => `
    <div class="task-item" onclick="openTask('${task.id}')">
      <div class="task-item-content">
        <div class="task-item-title">${escapeHtml(task.title)}</div>
        <div class="task-tags">
          ${createPriorityTag(task.priority)}
          ${createStatusTag(task.status)}
        </div>
      </div>
    </div>
  `).join('');
}

function updateUpcomingTasks() {
  // Filter tasks with due dates
  const tasksWithDueDates = allTasks
    .filter(task => task.dueDate && task.status !== 'done')
    .map(task => {
      const dueDate = new Date(task.dueDate);
      const now = new Date();
      const isOverdue = dueDate < now;
      const isDueSoon = !isOverdue && (dueDate - now) < (7 * 24 * 60 * 60 * 1000); // Within 7 days

      return {
        ...task,
        dueDate,
        isOverdue,
        isDueSoon,
        sortDate: dueDate.getTime()
      };
    })
    .sort((a, b) => a.sortDate - b.sortDate)
    .slice(0, 5); // Show top 5

  const container = document.getElementById('upcomingTasks');
  const countLabel = document.getElementById('upcoming-count');

  countLabel.textContent = `${tasksWithDueDates.length} tasks with deadlines`;

  if (tasksWithDueDates.length === 0) {
    container.innerHTML = '<p style="opacity: 0.5; text-align: center; padding: 2rem;">No upcoming deadlines</p>';
    return;
  }

  container.innerHTML = tasksWithDueDates.map(task => {
    const statusClass = task.isOverdue ? 'overdue' : (task.isDueSoon ? 'due-soon' : '');
    const statusText = task.isOverdue ? 'Overdue' : (task.isDueSoon ? 'Due soon' : 'Upcoming');
    const statusCssClass = task.isOverdue ? 'overdue' : (task.isDueSoon ? 'due-soon' : '');

    return `
      <div class="due-item ${statusClass}" onclick="openTask('${task.id}')">
        <div class="due-item-content">
          <div class="due-item-title">${escapeHtml(task.title)}</div>
          <div class="due-item-status ${statusCssClass}">${statusText}</div>
        </div>
        <div class="due-item-date">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <path d="M16 2v4M8 2v4M3 10h18"/>
          </svg>
          ${formatDate(task.dueDate)}
        </div>
      </div>
    `;
  }).join('');
}

// ==================== EVENT LISTENERS ====================

function setupEventListeners() {
  // New Task button
  document.getElementById('newTaskBtn').addEventListener('click', () => {
    alert('New Task modal would open here');
    // TODO: Implement new task modal
  });

  // Export button
  document.getElementById('exportBtn').addEventListener('click', async () => {
    try {
      const csv = exportTasksToCSV(allTasks);
      downloadCSV(csv, 'avenstudio-tasks.csv');
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export tasks');
    }
  });

  // Theme toggle
  document.getElementById('themeToggle').addEventListener('click', () => {
    alert('Dark theme toggle would work here');
    // TODO: Implement theme switching
  });

  // Categories button
  document.getElementById('categoriesBtn').addEventListener('click', () => {
    alert('Category manager would open here');
    // TODO: Implement category manager
  });

  // Search input
  document.getElementById('searchInput').addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    if (query.length > 2) {
      // TODO: Implement search functionality
      console.log('Searching for:', query);
    }
  });
}

// ==================== HELPER FUNCTIONS ====================

function openTask(taskId) {
  const task = allTasks.find(t => t.id === taskId);
  if (task) {
    console.log('Opening task:', task);
    alert(`Task: ${task.title}\n\nClick here would open task detail drawer`);
    // TODO: Implement task detail drawer
  }
}

function createPriorityTag(priority) {
  const tagClass = `tag-${priority}`;
  return `<span class="tag ${tagClass}">${priority}</span>`;
}

function createStatusTag(status) {
  const tagClass = `tag-${status}`;
  const displayText = status.replace('-', ' ');
  return `<span class="tag ${tagClass}">${displayText}</span>`;
}

function formatDate(date) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(date).toLocaleDateString('en-GB', options);
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showError(message) {
  // Show error banner at top of page
  const dashboard = document.querySelector('.dashboard');
  if (dashboard) {
    const errorBanner = document.createElement('div');
    errorBanner.style.cssText = `
      background: var(--danger-light);
      border: 2px solid var(--danger);
      border-radius: var(--radius-md);
      padding: var(--spacing-lg);
      margin-bottom: var(--spacing-xl);
      color: var(--danger);
    `;
    errorBanner.innerHTML = `
      <strong>❌ Error:</strong> ${escapeHtml(message)}<br>
      <small>Check the DevTools console (F12) for details.</small>
    `;
    dashboard.insertBefore(errorBanner, dashboard.firstChild);
  }

  // Also log to console
  console.error('Error displayed to user:', message);
}

// ==================== CSV EXPORT ====================

function exportTasksToCSV(tasks) {
  const headers = [
    'ID', 'Title', 'Description', 'Status', 'Priority',
    'Category', 'Tags', 'Due Date', 'Created', 'Updated'
  ];

  const rows = tasks.map(task => [
    task.id,
    task.title,
    task.description || '',
    task.status,
    task.priority,
    task.category,
    (task.tags || []).join(';'),
    task.dueDate || '',
    task.createdAt,
    task.updatedAt
  ]);

  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
  ].join('\n');

  return csvContent;
}

function downloadCSV(content, filename) {
  const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');

  if (navigator.msSaveBlob) {
    // IE 10+
    navigator.msSaveBlob(blob, filename);
  } else {
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  }
}

// ==================== AUTO-REFRESH ====================

// Refresh data every 30 seconds
setInterval(async () => {
  console.log('🔄 Auto-refreshing dashboard data...');
  await loadDashboardData();
}, 30000);

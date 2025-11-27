<template>
  <div class="todo-app">
    <h2>📝 Todo (CRUD Practice)</h2>

    <form @submit.prevent="addTask">
      <input v-model="newTitle" placeholder="What to do?" required />
      <button type="submit" class="btn-add">Add Task</button>
    </form>

    <div v-if="loading" class="loading">Loading tasks...</div>

    <div v-else-if="tasks.length === 0" class="no-tasks">
      <p>No tasks yet. Create one above!</p>
    </div>

    <div v-else class="tasks-list">
      <div v-for="task in tasks" :key="task.id" class="task-item" :class="{ completed: task.completed_at }">
        
        <div v-if="editingTask?.id !== task.id" class="task-display">
          <div class="task-content">
            <p class="task-title">{{ task.title }}</p>
            <small class="task-meta">by {{ task.created_by || 'anon' }} • {{ formatDate(task.created_at) }}</small>
            <div v-if="task.completed_at" class="task-completed">
              ✓ Completed: {{ formatDate(task.completed_at) }}
            </div>
          </div>
          <div class="task-actions">
            <button @click="toggleComplete(task)" class="btn-complete">
              {{ task.completed_at ? 'Uncomplete' : 'Complete' }}
            </button>
            <button @click="editTask(task)" class="btn-edit">Edit</button>
            <button @click="deleteTask(task)" class="btn-delete">Delete</button>
          </div>
        </div>

        <div v-else class="task-edit">
          <input v-model="editTitle" class="edit-input" />
          <div class="edit-actions">
            <button @click="saveTask" class="btn-save">Save</button>
            <button @click="cancelEdit" class="btn-cancel">Cancel</button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API_URL = 'http://localhost:8000/api/tasks/'

export default {
  name: 'TodoApp',
  data() {
    return {
      tasks: [],
      newTitle: '',
      loading: false,
      editingTask: null,
      editTitle: '',
    }
  },
  mounted() {
    this.fetchAllTasks()
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    },

    async fetchAllTasks() {
      this.loading = true
      try {
        const response = await axios.get(API_URL)
        this.tasks = response.data
      } catch (error) {
        console.error('Error fetching tasks:', error)
        alert('Failed to load tasks')
      } finally {
        this.loading = false
      }
    },

    async addTask() {
      if (!this.newTitle.trim()) return

      try {
        const newTask = { title: this.newTitle.trim() }
        const response = await axios.post(API_URL, newTask)
        this.tasks.unshift(response.data)
        this.newTitle = ''
      } catch (error) {
        console.error('Error adding task:', error)
        alert('Failed to add task')
      }
    },

    editTask(task) {
      this.editingTask = task
      this.editTitle = task.title
    },

    cancelEdit() {
      this.editingTask = null
      this.editTitle = ''
    },

    async saveTask() {
      if (!this.editTitle.trim()) return

      try {
        const updateData = { title: this.editTitle.trim() }
        const response = await axios.patch(
          API_URL + this.editingTask.id + '/',
          updateData
        )
        const taskIndex = this.tasks.findIndex(t => t.id === this.editingTask.id)
        
        // FIX: Directly update the array item for reliable Vue reactivity
        this.tasks[taskIndex] = response.data 

        this.editingTask = null
      } catch (error) {
        console.error('Error saving task:', error)
        alert('Failed to save task')
      }
    },

    async toggleComplete(task) {
      try {
        let updateData = {}
        if (task.completed_at) {
          // Uncomplete: Set completed_at to null
          updateData = { completed_at: null }
        } else {
          // Complete: Set completed_at to now (in ISO format)
          updateData = { completed_at: new Date().toISOString() }
        }
        
        const response = await axios.patch(API_URL + task.id + '/', updateData)
        const taskIndex = this.tasks.findIndex(t => t.id === task.id)
        
        // FIX: Directly update the array item for reliable Vue reactivity
        this.tasks[taskIndex] = response.data

      } catch (error) {
        console.error('Error toggling complete:', error)
        alert('Failed to update task')
      }
    },

    async deleteTask(task) {
      if (!confirm('Are you sure you want to delete this task?')) return

      try {
        await axios.delete(API_URL + task.id + '/')
        // Update local state by filtering the deleted task out
        this.tasks = this.tasks.filter(t => t.id !== task.id)
      } catch (error) {
        console.error('Error deleting task:', error)
        alert('Failed to delete task')
      }
    },
  },
}
</script>

<style scoped>
.todo-app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.todo-app h2 {
  text-align: center;
  color: #16d840;
  margin-bottom: 30px;
}

form {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

form input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.btn-add {
  padding: 12px 24px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-add:hover {
  background: #229954;
}

.loading,
.no-tasks {
  text-align: center;
  color: #999;
  padding: 40px;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-item {
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.task-item.completed {
  background: #f9f9f9;
  opacity: 0.7;
}

.task-display {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 15px;
}

.task-content {
  flex: 1;
}

.task-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.task-item.completed .task-title {
  text-decoration: line-through;
  color: #999;
}

.task-meta {
  color: #999;
  font-size: 13px;
}

.task-completed {
  margin-top: 8px;
  color: #27ae60;
  font-size: 13px;
  font-weight: bold;
}

.task-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.task-actions button {
  padding: 6px 12px;
  font-size: 13px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-complete {
  background: #3498db;
  color: white;
}

.btn-complete:hover {
  background: #2980b9;
}

.btn-edit {
  background: #f39c12;
  color: white;
}

.btn-edit:hover {
  background: #e67e22;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background: #c0392b;
}

.task-edit {
  display: flex;
  gap: 10px;
  align-items: center;
}

.edit-input {
  flex: 1;
  padding: 10px;
  border: 2px solid #f39c12;
  border-radius: 4px;
  font-size: 14px;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.btn-save {
  padding: 8px 16px;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn-save:hover {
  background: #229954;
}

.btn-cancel {
  padding: 8px 16px;
  background: #95a5a6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #7f8c8d;
}
</style>
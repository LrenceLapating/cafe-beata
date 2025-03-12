<template>
  <div class="item-editor">
    <div class="header">
      <h2>Menu Item Editor</h2>
      <div class="header-buttons">
        <button @click="showAddItemForm" class="add-item-button">
          <i class="fa-solid fa-plus"></i> Add New Item
        </button>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="notification.show" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>

    <!-- Category Filter -->
    <div class="category-filter">
      <label for="category-filter">Filter by Category:</label>
      <select id="category-filter" v-model="selectedCategory" @change="filterItemsByCategory">
        <option value="All">All Categories</option>
        <option v-for="category in categories" :key="category" :value="category">
          {{ category }}
        </option>
      </select>
    </div>

    <!-- Add/Edit Item Form -->
    <div v-if="showForm" class="item-form">
      <h3>{{ isEditing ? 'Edit Item' : 'Add New Item' }}</h3>
      <form @submit.prevent="saveItem" class="form-content">
        <div class="form-group">
          <label for="itemName">Item Name:</label>
          <input 
            type="text" 
            id="itemName" 
            v-model="currentItem.name" 
            required 
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="itemPrice">Price (₱):</label>
          <input 
            type="number" 
            id="itemPrice" 
            v-model="currentItem.price" 
            required 
            step="0.01" 
            min="0" 
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="itemCategory">Category:</label>
          <select 
            id="itemCategory" 
            v-model="currentItem.category" 
            class="form-input"
            required
          >
            <option value="">-- Select Category --</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
          <small class="form-help">Category is required and determines where the item will appear in the menu.</small>
        </div>

        <div class="form-group">
          <label for="itemImage">Image:</label>
          <input 
            type="file" 
            id="itemImage" 
            @change="handleImageUpload" 
            accept="image/*" 
            :required="!isEditing"
            class="form-input"
          />
          <img 
            v-if="imagePreview" 
            :src="imagePreview" 
            class="image-preview" 
            alt="Item preview"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="save-button" :disabled="isSaving">
            {{ isEditing ? (isSaving ? 'Updating...' : 'Update Item') : (isSaving ? 'Adding...' : 'Add Item') }}
          </button>
          <button type="button" @click="cancelEdit" class="cancel-button" :disabled="isSaving">
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Items List -->
    <div v-if="isLoading" class="loading">Loading items...</div>
    <div v-else class="items-list">
      <div v-for="item in items" :key="item.id" class="item-card">
        <img :src="getImageUrl(item.image)" :alt="item.name" class="item-image"/>
        <div class="item-info">
          <h4>{{ item.name }}</h4>
          <p class="item-price">₱{{ Number(item.price).toFixed(2) }}</p>
          <p v-if="item.category" class="item-category">{{ item.category }}</p>
        </div>
        <div class="item-actions">
          <button @click="editItem(item)" class="edit-button" :disabled="isSaving">
            <i class="fa-solid fa-edit"></i>
          </button>
          <button @click="deleteItem(item.id)" class="delete-button" :disabled="isSaving">
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { importMenuItems } from './ImportMenuItems';

export default {
  name: 'ItemEditor',
  emits: ['item-updated'],
  data() {
    return {
      items: [],
      showForm: false,
      isEditing: false,
      imagePreview: null,
      isLoading: false,
      isSaving: false,
      notification: {
        show: false,
        message: '',
        type: 'success'
      },
      currentItem: {
        id: null,
        name: '',
        price: '',
        category: '',
        image: null
      },
      categories: [
        'Ice Coffee',
        'Hot Coffee',
        'Juice Drinks',
        'Milkteas',
        'Chocolate Drinks',
        'Blended Frappes',
        'Pasta & Dishes'
      ],
      selectedCategory: 'All',
      allItems: [],
      hasImported: false
    }
  },
  methods: {
    showNotification(message, type = 'success') {
      this.notification = {
        show: true,
        message,
        type
      };
      setTimeout(() => {
        this.notification.show = false;
      }, 3000);
    },
    async fetchItems() {
      this.isLoading = true;
      try {
        const response = await fetch('http://localhost:8000/api/items');
        const data = await response.json();
        if (data.items) {
          this.allItems = data.items; // Store all items
          this.filterItemsByCategory(); // Apply current filter
          this.$emit('item-updated');
        }
      } catch (error) {
        console.error('Error fetching items:', error);
        this.showNotification('Failed to load items', 'error');
      } finally {
        this.isLoading = false;
      }
    },
    showAddItemForm() {
      this.currentItem = {
        name: '',
        price: '',
        category: this.categories[0], // Default to first category
        image: null
      };
      this.isEditing = false;
      this.showForm = true;
    },
    editItem(item) {
      this.isEditing = true;
      this.currentItem = { 
        id: item.id,
        name: item.name,
        price: item.price,
        category: item.category || '',
        image: null
      };
      this.imagePreview = this.getImageUrl(item.image);
      this.showForm = true;
    },
    async saveItem() {
      if (this.isSaving) return;
      
      // Validate category is selected
      if (!this.currentItem.category) {
        this.showNotification('Please select a category', 'error');
        return;
      }
      
      this.isSaving = true;

      try {
        const formData = new FormData();
        formData.append('name', this.currentItem.name);
        formData.append('price', this.currentItem.price);
        formData.append('category', this.currentItem.category);
        
        if (this.currentItem.image instanceof File) {
          formData.append('image', this.currentItem.image);
        }

        const url = this.isEditing 
          ? `http://localhost:8000/api/items/${this.currentItem.id}`
          : 'http://localhost:8000/api/items';
        
        const method = this.isEditing ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
          method,
          body: formData
        });

        if (response.ok) {
          const result = await response.json();
          this.showNotification(this.isEditing ? 'Item updated successfully' : 'Item added successfully');
          
          // Emit event to notify other components (like DashboardPage) that items have been updated
          this.$emit('item-updated', {
            action: this.isEditing ? 'updated' : 'added',
            item: {
              ...this.currentItem,
              id: this.isEditing ? this.currentItem.id : result.id
            }
          });
          
          // Refresh the items list
          await this.fetchItems();
          
          // Dispatch a custom event that can be listened to globally
          const event = new CustomEvent('items-updated', { 
            detail: { 
              action: this.isEditing ? 'updated' : 'added',
              category: this.currentItem.category
            } 
          });
          window.dispatchEvent(event);
          
          this.showForm = false;
          this.resetForm();
        } else {
          const error = await response.json();
          throw new Error(error.detail || 'Operation failed');
        }
      } catch (error) {
        console.error('Error saving item:', error);
        this.showNotification(error.message || 'Failed to save item', 'error');
      } finally {
        this.isSaving = false;
      }
    },
    async deleteItem(itemId) {
      if (!confirm('Are you sure you want to delete this item?')) return;
      
      this.isSaving = true;
      try {
        const response = await fetch(`http://localhost:8000/api/items/${itemId}`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          this.showNotification('Item deleted successfully');
          
          // Emit event to notify other components that an item has been deleted
          this.$emit('item-updated', {
            action: 'deleted',
            itemId
          });
          
          // Dispatch a custom event that can be listened to globally
          const event = new CustomEvent('items-updated', { 
            detail: { 
              action: 'deleted',
              itemId
            } 
          });
          window.dispatchEvent(event);
          
          await this.fetchItems();
        } else {
          const error = await response.json();
          throw new Error(error.detail || 'Failed to delete item');
        }
      } catch (error) {
        console.error('Error deleting item:', error);
        this.showNotification(error.message || 'Failed to delete item', 'error');
      } finally {
        this.isSaving = false;
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.currentItem.image = file;
        this.imagePreview = URL.createObjectURL(file);
      }
    },
    cancelEdit() {
      this.showForm = false;
      this.resetForm();
    },
    resetForm() {
      this.currentItem = {
        id: null,
        name: '',
        price: '',
        category: '',
        image: null
      };
      this.imagePreview = null;
      this.isEditing = false;
    },
    getImageUrl(imagePath) {
      if (!imagePath) {
        return require('@/assets/default.png');
      }
      
      // If it's already a full URL
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
      }
      
      // If it's a backend upload path
      if (imagePath.startsWith('/uploads/')) {
        return `http://localhost:8000${imagePath}`;
      }
      
      // If it's just a filename
      if (!imagePath.includes('/')) {
        return `http://localhost:8000/uploads/avatars/${imagePath}`;
      }
      
      // Fallback to default image
      return require('@/assets/default.png');
    },
    filterItemsByCategory() {
      if (!this.allItems) return;
      
      if (this.selectedCategory === 'All') {
        this.items = [...this.allItems];
      } else {
        this.items = this.allItems.filter(item => item.category === this.selectedCategory);
      }
    }
  },
  async mounted() {
    // First, check if we have any existing items
    await this.fetchItems();
    
    // If no items exist, import the static menu
    if (this.allItems.length === 0 && !this.hasImported) {
      this.showNotification('Importing menu items...', 'info');
      try {
        await importMenuItems();
        this.showNotification('Menu items imported successfully!', 'success');
        this.hasImported = true;
        await this.fetchItems(); // Refresh the items list
      } catch (error) {
        console.error('Error importing menu:', error);
        this.showNotification('Error importing menu items', 'error');
      }
    }
  }
}
</script>

<style scoped>
.item-editor {
  padding: 0;
  margin: 0;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-buttons {
  display: flex;
  gap: 10px;
}

.add-item-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-form {
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
}

.image-preview {
  max-width: 200px;
  max-height: 200px;
  margin-top: 10px;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.save-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.cancel-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.items-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.item-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
}

.item-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.item-info {
  padding: 15px;
}

.item-info h4 {
  margin: 0;
  font-size: 1.1em;
}

.item-price {
  margin: 5px 0 0;
  color: #d12f7a;
  font-weight: bold;
}

.item-category {
  margin: 5px 0 0;
  color: #666;
  font-size: 0.9em;
  font-style: italic;
}

.item-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
}

.edit-button, .delete-button {
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-button:hover {
  background-color: #4CAF50;
  color: white;
}

.delete-button:hover {
  background-color: #f44336;
  color: white;
}

.notification {
  padding: 10px 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
}

.notification.success {
  background-color: #4CAF50;
  color: white;
}

.notification.error {
  background-color: #f44336;
  color: white;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-help {
  color: #666;
  font-size: 0.8em;
  margin-top: 5px;
  display: block;
}

.category-filter {
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style> 
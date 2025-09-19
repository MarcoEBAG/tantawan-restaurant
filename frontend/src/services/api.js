import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    
    // Handle different error scenarios
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          throw new Error(data.error?.message || 'Ungültige Anfrage');
        case 404:
          throw new Error(data.error?.message || 'Nicht gefunden');
        case 500:
          throw new Error(data.error?.message || 'Serverfehler');
        default:
          throw new Error(data.error?.message || `Fehler ${status}`);
      }
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Keine Antwort vom Server. Bitte versuchen Sie es später erneut.');
    } else {
      // Something else happened
      throw new Error('Ein unerwarteter Fehler ist aufgetreten');
    }
  }
);

// Menu API
export const menuAPI = {
  // Get all menu items
  getAllItems: async () => {
    const response = await api.get('/menu/');
    return response.data;
  },

  // Get menu items by category
  getItemsByCategory: async (category) => {
    const response = await api.get(`/menu/${category}`);
    return response.data;
  },

  // Get specific menu item
  getItem: async (itemId) => {
    const response = await api.get(`/menu/item/${itemId}`);
    return response.data;
  }
};

// Orders API
export const ordersAPI = {
  // Create new order
  createOrder: async (orderData) => {
    const response = await api.post('/orders/', orderData);
    return response.data;
  },

  // Get order by ID
  getOrder: async (orderId) => {
    const response = await api.get(`/orders/${orderId}`);
    return response.data;
  },

  // Get order by order number
  getOrderByNumber: async (orderNumber) => {
    const response = await api.get(`/orders/number/${orderNumber}`);
    return response.data;
  },

  // Update order status (admin functionality)
  updateOrderStatus: async (orderId, status) => {
    const response = await api.put(`/orders/${orderId}/status`, { status });
    return response.data;
  },

  // Get customer orders
  getCustomerOrders: async (phone) => {
    const response = await api.get(`/orders/customer/${phone}`);
    return response.data;
  }
};

// Newsletter API
export const newsletterAPI = {
  // Subscribe to newsletter
  subscribe: async (email) => {
    const response = await api.post('/newsletter/subscribe', { email });
    return response.data;
  },

  // Unsubscribe from newsletter
  unsubscribe: async (email) => {
    const response = await api.delete(`/newsletter/subscribe/${email}`);
    return response.data;
  },

  // Get subscription count
  getSubscriptionCount: async () => {
    const response = await api.get('/newsletter/subscriptions/count');
    return response.data;
  }
};

// Health check API
export const healthAPI = {
  // Check API health
  checkHealth: async () => {
    const response = await api.get('/health');
    return response.data;
  }
};

// Export default api instance for custom requests
export default api;
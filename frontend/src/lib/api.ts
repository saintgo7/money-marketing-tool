import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// API functions
export const contentAPI = {
  generateSocial: (data: any) => api.post('/content/generate/social', data),
  generateImage: (data: any) => api.post('/content/generate/image', data),
  generateEmail: (data: any) => api.post('/content/generate/email', data),
  generateAdCopy: (data: any) => api.post('/content/generate/ad-copy', data),
  generateVideoScript: (data: any) => api.post('/content/generate/video-script', data),
  optimize: (data: any) => api.post('/content/optimize', data),
};

export const campaignAPI = {
  schedulePost: (data: any) => api.post('/campaigns/schedule/post', data),
  scheduleCampaign: (data: any) => api.post('/campaigns/schedule/campaign', data),
  reschedule: (data: any) => api.post('/campaigns/reschedule', data),
  cancel: (taskId: string) => api.delete(`/campaigns/cancel/${taskId}`),
  getRecommendations: (params: any) => api.get('/campaigns/recommendations', { params }),
  getOptimalTime: (params: any) => api.get('/campaigns/optimal-time', { params }),
};

export const analyticsAPI = {
  getOverview: (params: any) => api.get('/analytics/overview', { params }),
  getPlatformPerformance: (params: any) => api.get('/analytics/platform-performance', { params }),
  getTopPosts: (params: any) => api.get('/analytics/top-posts', { params }),
  getTrends: (params: any) => api.get('/analytics/trends', { params }),
  getInsights: (params: any) => api.get('/analytics/insights', { params }),
};

export const socialAccountsAPI = {
  connect: (data: any) => api.post('/social-accounts/connect', data),
  list: (userId: number) => api.get('/social-accounts/list', { params: { user_id: userId } }),
  get: (accountId: number) => api.get(`/social-accounts/${accountId}`),
  update: (accountId: number, data: any) => api.patch(`/social-accounts/${accountId}`, data),
  disconnect: (accountId: number) => api.delete(`/social-accounts/${accountId}`),
};

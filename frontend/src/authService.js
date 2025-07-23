// Authentication service for handling user authentication
class AuthService {
  constructor() {
    this.baseURL = process.env.REACT_APP_BACKEND_URL || '';
    this.tokenKey = 'ideahero_token';
    this.userKey = 'ideahero_user';
  }

  // Get stored token
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  // Get stored user
  getUser() {
    const userStr = localStorage.getItem(this.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  // Check if user is authenticated
  isAuthenticated() {
    const token = this.getToken();
    const user = this.getUser();
    return !!(token && user);
  }

  // Store authentication data
  setAuthData(token, user) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.userKey, JSON.stringify(user));
  }

  // Clear authentication data
  clearAuthData() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
  }

  // Make authenticated API request
  async authenticatedFetch(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.clearAuthData();
      window.location.href = '/login';
      throw new Error('Authentication required');
    }

    return response;
  }

  // Register new user
  async register(userData) {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Registration failed');
      }

      const data = await response.json();
      this.setAuthData(data.access_token, data.user);
      return data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  // Login user
  async login(credentials) {
    try {
      const response = await fetch(`${this.baseURL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();
      this.setAuthData(data.access_token, data.user);
      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Logout user
  logout() {
    this.clearAuthData();
    window.location.href = '/';
  }

  // Get current user profile
  async getCurrentUser() {
    try {
      const response = await this.authenticatedFetch('/api/auth/me');
      if (!response.ok) {
        throw new Error('Failed to get user profile');
      }
      return await response.json();
    } catch (error) {
      console.error('Get user error:', error);
      throw error;
    }
  }

  // Update user profile
  async updateProfile(profileData) {
    try {
      const response = await this.authenticatedFetch('/api/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Profile update failed');
      }

      const updatedUser = await response.json();
      this.setAuthData(this.getToken(), updatedUser);
      return updatedUser;
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  }

  // Vote on idea
  async voteOnIdea(ideaId, voteData) {
    try {
      const response = await this.authenticatedFetch(`/api/ideas/${ideaId}/vote`, {
        method: 'POST',
        body: JSON.stringify(voteData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Vote failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Vote error:', error);
      throw error;
    }
  }

  // Comment on idea
  async commentOnIdea(ideaId, content) {
    try {
      const response = await this.authenticatedFetch(`/api/ideas/${ideaId}/comment`, {
        method: 'POST',
        body: JSON.stringify({ idea_id: ideaId, content }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Comment failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Comment error:', error);
      throw error;
    }
  }

  // Get enhanced ideas with validation data
  async getEnhancedIdeas(params = {}) {
    try {
      const searchParams = new URLSearchParams(params);
      const response = await fetch(`${this.baseURL}/api/ideas?${searchParams}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch ideas');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Get ideas error:', error);
      throw error;
    }
  }

  // Get single idea details
  async getIdeaDetails(ideaId) {
    try {
      const response = await fetch(`${this.baseURL}/api/ideas/${ideaId}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch idea details');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Get idea details error:', error);
      throw error;
    }
  }

  // Get user dashboard data
  async getUserDashboard() {
    try {
      const response = await this.authenticatedFetch('/api/user/dashboard');
      
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Dashboard error:', error);
      throw error;
    }
  }

  // Get user analytics data
  async getUserAnalytics() {
    try {
      const response = await this.authenticatedFetch('/api/user/analytics');
      
      if (!response.ok) {
        throw new Error('Failed to fetch analytics data');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Analytics error:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const authService = new AuthService();
import { useState, useEffect, useCallback } from 'react';
import api from '@/lib/api';

export function useAuth() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token) {
        const response = await api.get('/auth/me');
        setUser(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch user:', error);
      localStorage.removeItem('auth_token');
    } finally {
      setLoading(false);
    }
  };

  const logout = useCallback(() => {
    localStorage.removeItem('auth_token');
    setUser(null);
    window.location.href = '/login';
  }, []);

  return { user, loading, logout, refetch: fetchUser };
}

export function useContent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateSocial = useCallback(async (data: any) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/content/generate/social', data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate content');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const generateImage = useCallback(async (data: any) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/content/generate/image', data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate image');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { generateSocial, generateImage, loading, error };
}

export function useAnalytics(userId: number) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOverview = useCallback(async (params?: any) => {
    setLoading(true);
    try {
      const response = await api.get('/analytics/overview', {
        params: { user_id: userId, ...params }
      });
      setData(response.data.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch analytics');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) {
      fetchOverview();
    }
  }, [userId, fetchOverview]);

  return { data, loading, error, refetch: fetchOverview };
}

export function useCampaigns(userId: number) {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchCampaigns = useCallback(async () => {
    setLoading(true);
    try {
      // TODO: Implement API endpoint
      // const response = await api.get('/campaigns', { params: { user_id: userId } });
      // setCampaigns(response.data.data);
      setCampaigns([]);
    } catch (error) {
      console.error('Failed to fetch campaigns:', error);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) {
      fetchCampaigns();
    }
  }, [userId, fetchCampaigns]);

  return { campaigns, loading, refetch: fetchCampaigns };
}

export function useSubscription() {
  const [subscription, setSubscription] = useState<any>(null);
  const [usage, setUsage] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchSubscription = useCallback(async () => {
    try {
      const [subResponse, usageResponse] = await Promise.all([
        api.get('/payments/subscription'),
        api.get('/payments/usage')
      ]);
      setSubscription(subResponse.data);
      setUsage(usageResponse.data);
    } catch (error) {
      console.error('Failed to fetch subscription:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSubscription();
  }, [fetchSubscription]);

  return { subscription, usage, loading, refetch: fetchSubscription };
}

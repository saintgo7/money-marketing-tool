'use client';

import { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { TrendingUp, TrendingDown, Users, Heart, MessageCircle, Share2 } from 'lucide-react';

export default function Dashboard() {
  const [timeRange, setTimeRange] = useState('30d');
  const [analyticsData, setAnalyticsData] = useState<any>(null);

  useEffect(() => {
    // Fetch analytics data
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    // Mock data for demonstration
    setAnalyticsData({
      summary: {
        engagement_rate: 4.2,
        reach: 125000,
        impressions: 350000,
        posts: 45,
      },
      trends: [
        { date: '2025-01-01', engagement: 3.2, reach: 10000, impressions: 25000 },
        { date: '2025-01-08', engagement: 3.8, reach: 12000, impressions: 28000 },
        { date: '2025-01-15', engagement: 4.1, reach: 15000, impressions: 32000 },
        { date: '2025-01-22', engagement: 4.2, reach: 18000, impressions: 35000 },
      ],
      platformPerformance: [
        { platform: 'Instagram', posts: 15, engagement: 5200, rate: 4.8 },
        { platform: 'LinkedIn', posts: 12, engagement: 3800, rate: 3.9 },
        { platform: 'Twitter', posts: 10, engagement: 2100, rate: 3.2 },
        { platform: 'Facebook', posts: 8, engagement: 1900, rate: 2.8 },
      ],
    });
  };

  if (!analyticsData) {
    return <div className="p-8">Loading...</div>;
  }

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444'];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
          <p className="text-gray-600">Track your marketing performance across all platforms</p>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6 flex space-x-2">
          {['7d', '30d', '90d', '1y'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg ${
                timeRange === range
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {range === '7d' && 'Last 7 Days'}
              {range === '30d' && 'Last 30 Days'}
              {range === '90d' && 'Last 90 Days'}
              {range === '1y' && 'Last Year'}
            </button>
          ))}
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Engagement Rate"
            value={`${analyticsData.summary.engagement_rate}%`}
            change="+0.8%"
            trend="up"
            icon={<Heart className="w-6 h-6" />}
          />
          <KPICard
            title="Total Reach"
            value={formatNumber(analyticsData.summary.reach)}
            change="+12%"
            trend="up"
            icon={<Users className="w-6 h-6" />}
          />
          <KPICard
            title="Impressions"
            value={formatNumber(analyticsData.summary.impressions)}
            change="+8%"
            trend="up"
            icon={<TrendingUp className="w-6 h-6" />}
          />
          <KPICard
            title="Posts Published"
            value={analyticsData.summary.posts.toString()}
            change="+5"
            trend="up"
            icon={<MessageCircle className="w-6 h-6" />}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Engagement Trend */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-lg font-semibold mb-4">Engagement Trend</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analyticsData.trends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="engagement"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  name="Engagement Rate"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Platform Performance */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-lg font-semibold mb-4">Platform Performance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={analyticsData.platformPerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="platform" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="engagement" fill="#3B82F6" name="Total Engagement" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Reach vs Impressions */}
        <div className="bg-white p-6 rounded-lg shadow-sm mb-8">
          <h3 className="text-lg font-semibold mb-4">Reach vs Impressions</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analyticsData.trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="reach"
                stroke="#10B981"
                strokeWidth={2}
                name="Reach"
              />
              <Line
                type="monotone"
                dataKey="impressions"
                stroke="#3B82F6"
                strokeWidth={2}
                name="Impressions"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Top Posts */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold mb-4">Top Performing Posts</h3>
          <div className="space-y-4">
            {[
              {
                id: 1,
                platform: 'Instagram',
                content: '5 Tips for Better Marketing ROI...',
                engagement: 1250,
                date: '2025-01-15',
              },
              {
                id: 2,
                platform: 'LinkedIn',
                content: 'How AI is Transforming Digital Marketing',
                engagement: 980,
                date: '2025-01-18',
              },
              {
                id: 3,
                platform: 'Twitter',
                content: 'Quick thread on content strategy...',
                engagement: 745,
                date: '2025-01-20',
              },
            ].map((post) => (
              <div
                key={post.id}
                className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-sm font-medium text-blue-600">{post.platform}</span>
                    <span className="text-sm text-gray-500">{post.date}</span>
                  </div>
                  <p className="text-gray-900">{post.content}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <Heart className="w-4 h-4 text-gray-400" />
                  <span className="font-semibold">{post.engagement}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({
  title,
  value,
  change,
  trend,
  icon,
}: {
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  icon: React.ReactNode;
}) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-600 text-sm">{title}</span>
        <div className="text-blue-600">{icon}</div>
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-2">{value}</div>
      <div className="flex items-center space-x-1">
        {trend === 'up' ? (
          <TrendingUp className="w-4 h-4 text-green-500" />
        ) : (
          <TrendingDown className="w-4 h-4 text-red-500" />
        )}
        <span className={`text-sm ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
          {change}
        </span>
        <span className="text-sm text-gray-500">vs last period</span>
      </div>
    </div>
  );
}

function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}

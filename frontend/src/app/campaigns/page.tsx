'use client';

import { useState, useEffect } from 'react';
import { Plus, TrendingUp, Users, BarChart3, Edit, Trash2 } from 'lucide-react';

interface Campaign {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'completed';
  platforms: string[];
  postsScheduled: number;
  postsPublished: number;
  totalReach: number;
  engagement: number;
  startDate: string;
  endDate: string;
}

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    setLoading(true);
    // Mock data
    setTimeout(() => {
      setCampaigns([
        {
          id: '1',
          name: '신제품 런칭 캠페인',
          description: '새로운 제품 라인 홍보를 위한 통합 마케팅 캠페인',
          status: 'active',
          platforms: ['instagram', 'facebook', 'twitter'],
          postsScheduled: 15,
          postsPublished: 8,
          totalReach: 125000,
          engagement: 4800,
          startDate: '2025-01-15',
          endDate: '2025-02-15',
        },
        {
          id: '2',
          name: '브랜드 인지도 향상',
          description: '브랜드 스토리텔링 중심의 콘텐츠 캠페인',
          status: 'active',
          platforms: ['linkedin', 'instagram'],
          postsScheduled: 20,
          postsPublished: 12,
          totalReach: 98000,
          engagement: 3200,
          startDate: '2025-01-10',
          endDate: '2025-03-10',
        },
        {
          id: '3',
          name: '연말 프로모션',
          description: '2024년 연말 특별 할인 프로모션',
          status: 'completed',
          platforms: ['instagram', 'facebook', 'twitter', 'linkedin'],
          postsScheduled: 25,
          postsPublished: 25,
          totalReach: 250000,
          engagement: 12500,
          startDate: '2024-12-01',
          endDate: '2024-12-31',
        },
      ]);
      setLoading(false);
    }, 1000);
  };

  const statusColors = {
    active: 'bg-green-100 text-green-800',
    paused: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-gray-100 text-gray-800',
  };

  const platformIcons: { [key: string]: string } = {
    instagram: '📸',
    facebook: '📘',
    twitter: '🐦',
    linkedin: '💼',
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">캠페인 관리</h1>
            <p className="text-gray-600">마케팅 캠페인을 생성하고 성과를 추적하세요</p>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            <Plus className="w-5 h-5" />
            <span>새 캠페인</span>
          </button>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={<BarChart3 className="w-6 h-6" />}
            title="활성 캠페인"
            value="2"
            change="+1"
            trend="up"
          />
          <StatCard
            icon={<TrendingUp className="w-6 h-6" />}
            title="총 도달 수"
            value="223K"
            change="+12%"
            trend="up"
          />
          <StatCard
            icon={<Users className="w-6 h-6" />}
            title="총 참여"
            value="8.0K"
            change="+8%"
            trend="up"
          />
          <StatCard
            icon={<BarChart3 className="w-6 h-6" />}
            title="평균 참여율"
            value="3.6%"
            change="+0.4%"
            trend="up"
          />
        </div>

        {/* Campaigns List */}
        {loading ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">로딩 중...</p>
          </div>
        ) : campaigns.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <BarChart3 className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 mb-4">생성된 캠페인이 없습니다</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              첫 캠페인 만들기
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {campaigns.map((campaign) => (
              <div key={campaign.id} className="bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">{campaign.name}</h3>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          statusColors[campaign.status]
                        }`}
                      >
                        {campaign.status === 'active' && '진행중'}
                        {campaign.status === 'paused' && '일시정지'}
                        {campaign.status === 'completed' && '완료'}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-4">{campaign.description}</p>

                    {/* Platforms */}
                    <div className="flex items-center space-x-2 mb-4">
                      {campaign.platforms.map((platform) => (
                        <span
                          key={platform}
                          className="px-3 py-1 bg-gray-100 rounded-full text-sm flex items-center space-x-1"
                        >
                          <span>{platformIcons[platform]}</span>
                          <span className="capitalize">{platform}</span>
                        </span>
                      ))}
                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <p className="text-sm text-gray-500">게시물</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {campaign.postsPublished}/{campaign.postsScheduled}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">도달 수</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {formatNumber(campaign.totalReach)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">참여</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {formatNumber(campaign.engagement)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">기간</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {new Date(campaign.startDate).toLocaleDateString('ko-KR', {
                            month: 'short',
                            day: 'numeric',
                          })}{' '}
                          -{' '}
                          {new Date(campaign.endDate).toLocaleDateString('ko-KR', {
                            month: 'short',
                            day: 'numeric',
                          })}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition">
                      <Edit className="w-5 h-5" />
                    </button>
                    <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mt-4">
                  <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                    <span>진행률</span>
                    <span>{Math.round((campaign.postsPublished / campaign.postsScheduled) * 100)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{
                        width: `${(campaign.postsPublished / campaign.postsScheduled) * 100}%`,
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({
  icon,
  title,
  value,
  change,
  trend,
}: {
  icon: React.ReactNode;
  title: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
}) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-gray-600 text-sm">{title}</span>
        <div className="text-blue-600">{icon}</div>
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-2">{value}</div>
      <div className="flex items-center space-x-1">
        <span className={`text-sm ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
          {change}
        </span>
        <span className="text-sm text-gray-500">vs 지난 기간</span>
      </div>
    </div>
  );
}

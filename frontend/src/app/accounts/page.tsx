'use client';

import { useState, useEffect } from 'react';
import { Instagram, Facebook, Twitter, Linkedin, Plus, Trash2, RefreshCw } from 'lucide-react';

interface SocialAccount {
  id: number;
  platform: string;
  accountName: string;
  accountId: string;
  isActive: boolean;
  connectedAt: string;
}

export default function AccountsPage() {
  const [accounts, setAccounts] = useState<SocialAccount[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    setLoading(true);
    // Mock data
    setTimeout(() => {
      setAccounts([
        {
          id: 1,
          platform: 'instagram',
          accountName: '@mycompany',
          accountId: 'instagram_123',
          isActive: true,
          connectedAt: '2025-01-15T10:00:00',
        },
        {
          id: 2,
          platform: 'linkedin',
          accountName: 'My Company',
          accountId: 'linkedin_456',
          isActive: true,
          connectedAt: '2025-01-16T14:00:00',
        },
      ]);
      setLoading(false);
    }, 1000);
  };

  const platformConfig = {
    instagram: {
      name: 'Instagram',
      icon: Instagram,
      color: 'text-pink-600',
      bgColor: 'bg-pink-50',
    },
    facebook: {
      name: 'Facebook',
      icon: Facebook,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    twitter: {
      name: 'Twitter',
      icon: Twitter,
      color: 'text-sky-500',
      bgColor: 'bg-sky-50',
    },
    linkedin: {
      name: 'LinkedIn',
      icon: Linkedin,
      color: 'text-blue-700',
      bgColor: 'bg-blue-50',
    },
  };

  const availablePlatforms = ['instagram', 'facebook', 'twitter', 'linkedin'];
  const connectedPlatforms = accounts.map((acc) => acc.platform);
  const unconnectedPlatforms = availablePlatforms.filter(
    (p) => !connectedPlatforms.includes(p)
  );

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">소셜 미디어 계정</h1>
          <p className="text-gray-600">
            소셜 미디어 계정을 연결하고 관리하세요
          </p>
        </div>

        {/* Connected Accounts */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">연결된 계정</h2>

          {loading ? (
            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">로딩 중...</p>
            </div>
          ) : accounts.length === 0 ? (
            <div className="bg-white rounded-lg shadow-sm p-12 text-center">
              <p className="text-gray-600 mb-4">연결된 계정이 없습니다</p>
              <p className="text-sm text-gray-500">
                아래에서 소셜 미디어 계정을 연결하세요
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {accounts.map((account) => {
                const config = platformConfig[account.platform as keyof typeof platformConfig];
                const Icon = config.icon;

                return (
                  <div
                    key={account.id}
                    className="bg-white rounded-lg shadow-sm p-6 flex items-center justify-between"
                  >
                    <div className="flex items-center space-x-4">
                      <div className={`p-3 ${config.bgColor} rounded-lg`}>
                        <Icon className={`w-6 h-6 ${config.color}`} />
                      </div>

                      <div>
                        <h3 className="font-semibold text-gray-900">{config.name}</h3>
                        <p className="text-gray-600">{account.accountName}</p>
                        <p className="text-sm text-gray-500">
                          연결됨:{' '}
                          {new Date(account.connectedAt).toLocaleDateString('ko-KR')}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <span
                        className={`px-3 py-1 rounded-full text-sm ${
                          account.isActive
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {account.isActive ? '활성' : '비활성'}
                      </span>

                      <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition">
                        <RefreshCw className="w-5 h-5" />
                      </button>

                      <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Available Platforms */}
        {unconnectedPlatforms.length > 0 && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">계정 연결</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {unconnectedPlatforms.map((platform) => {
                const config = platformConfig[platform as keyof typeof platformConfig];
                const Icon = config.icon;

                return (
                  <button
                    key={platform}
                    className="bg-white rounded-lg shadow-sm p-6 flex items-center justify-between hover:shadow-md transition group"
                  >
                    <div className="flex items-center space-x-4">
                      <div className={`p-3 ${config.bgColor} rounded-lg`}>
                        <Icon className={`w-6 h-6 ${config.color}`} />
                      </div>

                      <div className="text-left">
                        <h3 className="font-semibold text-gray-900">{config.name}</h3>
                        <p className="text-sm text-gray-600">계정 연결하기</p>
                      </div>
                    </div>

                    <div className="p-2 bg-blue-600 text-white rounded-lg group-hover:bg-blue-700 transition">
                      <Plus className="w-5 h-5" />
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-2">계정 연결 방법</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm text-blue-800">
            <li>연결하려는 플랫폼을 선택하세요</li>
            <li>해당 플랫폼의 OAuth 인증 페이지로 이동합니다</li>
            <li>권한을 승인하면 자동으로 계정이 연결됩니다</li>
            <li>연결된 계정으로 콘텐츠를 발행할 수 있습니다</li>
          </ol>
        </div>
      </div>
    </div>
  );
}

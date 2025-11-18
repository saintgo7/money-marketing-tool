'use client';

import { useState } from 'react';
import { User, Bell, CreditCard, Shield, Globe, Trash2 } from 'lucide-react';

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');

  const tabs = [
    { id: 'profile', name: '프로필', icon: User },
    { id: 'notifications', name: '알림', icon: Bell },
    { id: 'billing', name: '결제', icon: CreditCard },
    { id: 'security', name: '보안', icon: Shield },
    { id: 'preferences', name: '환경설정', icon: Globe },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">설정</h1>
          <p className="text-gray-600">계정 및 애플리케이션 설정을 관리하세요</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="bg-white rounded-lg shadow-sm p-4">
            <nav className="space-y-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
                      activeTab === tab.id
                        ? 'bg-blue-50 text-blue-600'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{tab.name}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* Content */}
          <div className="md:col-span-3">
            {activeTab === 'profile' && <ProfileSettings />}
            {activeTab === 'notifications' && <NotificationSettings />}
            {activeTab === 'billing' && <BillingSettings />}
            {activeTab === 'security' && <SecuritySettings />}
            {activeTab === 'preferences' && <PreferencesSettings />}
          </div>
        </div>
      </div>
    </div>
  );
}

function ProfileSettings() {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">프로필 정보</h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">이름</label>
          <input
            type="text"
            defaultValue="홍길동"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">이메일</label>
          <input
            type="email"
            defaultValue="hong@example.com"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">회사명</label>
          <input
            type="text"
            defaultValue="마케팅 컴퍼니"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">전화번호</label>
          <input
            type="tel"
            placeholder="010-1234-5678"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
          />
        </div>

        <div className="pt-4">
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
            변경사항 저장
          </button>
        </div>
      </div>
    </div>
  );
}

function NotificationSettings() {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">알림 설정</h2>

      <div className="space-y-6">
        <div className="flex items-center justify-between py-3 border-b border-gray-200">
          <div>
            <h3 className="font-medium text-gray-900">이메일 알림</h3>
            <p className="text-sm text-gray-600">중요한 업데이트를 이메일로 받습니다</p>
          </div>
          <input type="checkbox" defaultChecked className="toggle" />
        </div>

        <div className="flex items-center justify-between py-3 border-b border-gray-200">
          <div>
            <h3 className="font-medium text-gray-900">게시물 발행 알림</h3>
            <p className="text-sm text-gray-600">게시물이 발행될 때 알림을 받습니다</p>
          </div>
          <input type="checkbox" defaultChecked className="toggle" />
        </div>

        <div className="flex items-center justify-between py-3 border-b border-gray-200">
          <div>
            <h3 className="font-medium text-gray-900">주간 리포트</h3>
            <p className="text-sm text-gray-600">주간 성과 리포트를 이메일로 받습니다</p>
          </div>
          <input type="checkbox" defaultChecked className="toggle" />
        </div>

        <div className="flex items-center justify-between py-3 border-b border-gray-200">
          <div>
            <h3 className="font-medium text-gray-900">마케팅 이메일</h3>
            <p className="text-sm text-gray-600">신규 기능 및 프로모션 정보를 받습니다</p>
          </div>
          <input type="checkbox" className="toggle" />
        </div>
      </div>
    </div>
  );
}

function BillingSettings() {
  return (
    <div className="space-y-6">
      {/* Current Plan */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">현재 요금제</h2>

        <div className="border-2 border-blue-600 rounded-lg p-6 bg-blue-50">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-2xl font-bold text-gray-900">Pro</h3>
              <p className="text-gray-600">월 $79</p>
            </div>
            <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition">
              요금제 변경
            </button>
          </div>

          <div className="space-y-2 text-sm text-gray-700">
            <p>✓ 25개 소셜 계정</p>
            <p>✓ 무제한 AI 콘텐츠 생성</p>
            <p>✓ 월 200회 이미지 생성</p>
            <p>✓ 팀 협업 (5명)</p>
            <p>✓ API 액세스</p>
          </div>
        </div>
      </div>

      {/* Usage */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">이번 달 사용량</h2>

        <div className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-700">AI 콘텐츠 생성</span>
              <span className="font-semibold">무제한</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: '0%' }}></div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-700">이미지 생성</span>
              <span className="font-semibold">45 / 200</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: '22.5%' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Payment Method */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">결제 수단</h2>

        <div className="border border-gray-200 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-8 bg-gray-800 rounded flex items-center justify-center">
              <span className="text-white font-bold text-xs">VISA</span>
            </div>
            <div>
              <p className="font-medium">•••• •••• •••• 4242</p>
              <p className="text-sm text-gray-600">만료: 12/25</p>
            </div>
          </div>
          <button className="text-blue-600 hover:text-blue-700 font-medium">변경</button>
        </div>
      </div>
    </div>
  );
}

function SecuritySettings() {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">보안 설정</h2>

      <div className="space-y-6">
        <div>
          <h3 className="font-medium text-gray-900 mb-4">비밀번호 변경</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                현재 비밀번호
              </label>
              <input
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                새 비밀번호
              </label>
              <input
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                비밀번호 확인
              </label>
              <input
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
              />
            </div>
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
              비밀번호 변경
            </button>
          </div>
        </div>

        <div className="border-t border-gray-200 pt-6">
          <h3 className="font-medium text-gray-900 mb-4">2단계 인증</h3>
          <p className="text-gray-600 mb-4">
            추가 보안 계층으로 계정을 보호하세요
          </p>
          <button className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition">
            2단계 인증 활성화
          </button>
        </div>

        <div className="border-t border-gray-200 pt-6">
          <h3 className="font-medium text-red-600 mb-4">계정 삭제</h3>
          <p className="text-gray-600 mb-4">
            계정을 삭제하면 모든 데이터가 영구적으로 삭제됩니다
          </p>
          <button className="flex items-center space-x-2 bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition">
            <Trash2 className="w-4 h-4" />
            <span>계정 삭제</span>
          </button>
        </div>
      </div>
    </div>
  );
}

function PreferencesSettings() {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">환경설정</h2>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">언어</label>
          <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent">
            <option value="ko">한국어</option>
            <option value="en">English</option>
            <option value="ja">日本語</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">시간대</label>
          <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent">
            <option value="Asia/Seoul">서울 (GMT+9)</option>
            <option value="America/New_York">뉴욕 (GMT-5)</option>
            <option value="Europe/London">런던 (GMT+0)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">날짜 형식</label>
          <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent">
            <option value="yyyy-MM-dd">2025-01-20</option>
            <option value="MM/dd/yyyy">01/20/2025</option>
            <option value="dd/MM/yyyy">20/01/2025</option>
          </select>
        </div>

        <div className="pt-4">
          <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
            변경사항 저장
          </button>
        </div>
      </div>
    </div>
  );
}

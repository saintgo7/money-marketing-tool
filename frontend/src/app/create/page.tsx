'use client';

import { useState } from 'react';
import { Sparkles, Image as ImageIcon, Mail, Megaphone, Video } from 'lucide-react';

export default function CreatePage() {
  const [activeTab, setActiveTab] = useState('social');
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState<any>(null);

  const [formData, setFormData] = useState({
    topic: '',
    platforms: [] as string[],
    tone: 'professional',
    brandVoice: 'friendly and engaging',
    keywords: '',
    targetAudience: '',
  });

  const platformOptions = [
    { id: 'instagram', name: 'Instagram', icon: '📸' },
    { id: 'facebook', name: 'Facebook', icon: '📘' },
    { id: 'twitter', name: 'Twitter', icon: '🐦' },
    { id: 'linkedin', name: 'LinkedIn', icon: '💼' },
    { id: 'tiktok', name: 'TikTok', icon: '🎵' },
  ];

  const toneOptions = ['professional', 'casual', 'humorous', 'inspirational', 'educational'];

  const handlePlatformToggle = (platformId: string) => {
    if (formData.platforms.includes(platformId)) {
      setFormData({
        ...formData,
        platforms: formData.platforms.filter((p) => p !== platformId),
      });
    } else {
      setFormData({
        ...formData,
        platforms: [...formData.platforms, platformId],
      });
    }
  };

  const handleGenerate = async () => {
    if (!formData.topic || formData.platforms.length === 0) {
      alert('주제와 최소 1개 이상의 플랫폼을 선택해주세요.');
      return;
    }

    setLoading(true);
    setGenerated(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/content/generate/social`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
          },
          body: JSON.stringify({
            topic: formData.topic,
            platforms: formData.platforms,
            tone: formData.tone,
            brand_voice: formData.brandVoice,
            keywords: formData.keywords.split(',').map((k) => k.trim()).filter(Boolean),
            target_audience: formData.targetAudience || null,
          }),
        }
      );

      if (!response.ok) {
        throw new Error('콘텐츠 생성에 실패했습니다.');
      }

      const result = await response.json();
      setGenerated(result.data);
    } catch (error) {
      alert('콘텐츠 생성 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI 콘텐츠 생성</h1>
          <p className="text-gray-600">AI로 몇 초 만에 매력적인 마케팅 콘텐츠를 생성하세요</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <div className="flex border-b">
            {[
              { id: 'social', name: '소셜 미디어', icon: Sparkles },
              { id: 'image', name: '이미지', icon: ImageIcon },
              { id: 'email', name: '이메일', icon: Mail },
              { id: 'ad', name: '광고', icon: Megaphone },
              { id: 'video', name: '비디오', icon: Video },
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-6 py-4 font-semibold transition ${
                    activeTab === tab.id
                      ? 'border-b-2 border-blue-600 text-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-4">콘텐츠 설정</h2>

            <div className="space-y-4">
              {/* Topic */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  주제 / 내용 *
                </label>
                <textarea
                  value={formData.topic}
                  onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  placeholder="예: 생산성 향상을 위한 5가지 팁"
                />
              </div>

              {/* Platforms */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  플랫폼 선택 *
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {platformOptions.map((platform) => (
                    <button
                      key={platform.id}
                      onClick={() => handlePlatformToggle(platform.id)}
                      className={`flex items-center space-x-2 px-4 py-3 border rounded-lg transition ${
                        formData.platforms.includes(platform.id)
                          ? 'border-blue-600 bg-blue-50 text-blue-600'
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                    >
                      <span className="text-xl">{platform.icon}</span>
                      <span className="font-medium">{platform.name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Tone */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">톤 앤 매너</label>
                <select
                  value={formData.tone}
                  onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                >
                  {toneOptions.map((tone) => (
                    <option key={tone} value={tone}>
                      {tone.charAt(0).toUpperCase() + tone.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              {/* Brand Voice */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">브랜드 보이스</label>
                <input
                  type="text"
                  value={formData.brandVoice}
                  onChange={(e) => setFormData({ ...formData, brandVoice: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  placeholder="친근하고 전문적인"
                />
              </div>

              {/* Keywords */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  키워드 (쉼표로 구분)
                </label>
                <input
                  type="text"
                  value={formData.keywords}
                  onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  placeholder="생산성, 시간관리, 효율성"
                />
              </div>

              {/* Target Audience */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  타겟 오디언스
                </label>
                <input
                  type="text"
                  value={formData.targetAudience}
                  onChange={(e) => setFormData({ ...formData, targetAudience: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  placeholder="직장인, 20-30대"
                />
              </div>

              {/* Generate Button */}
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
              >
                <Sparkles className="w-5 h-5" />
                <span>{loading ? 'AI 생성 중...' : 'AI로 콘텐츠 생성'}</span>
              </button>
            </div>
          </div>

          {/* Preview */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold mb-4">생성된 콘텐츠</h2>

            {!generated && !loading && (
              <div className="text-center py-12 text-gray-500">
                <Sparkles className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p>왼쪽 폼을 작성하고 생성 버튼을 클릭하세요</p>
              </div>
            )}

            {loading && (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">AI가 콘텐츠를 생성하고 있습니다...</p>
              </div>
            )}

            {generated && (
              <div className="space-y-6">
                {Object.entries(generated).map(([platform, content]: [string, any]) => (
                  <div key={platform} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-lg capitalize">{platform}</h3>
                      <button className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                        복사
                      </button>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <p className="text-sm font-medium text-gray-700 mb-1">콘텐츠:</p>
                        <p className="text-gray-900 whitespace-pre-wrap">{content.content}</p>
                      </div>

                      {content.hashtags && content.hashtags.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-1">해시태그:</p>
                          <p className="text-blue-600">{content.hashtags.join(' ')}</p>
                        </div>
                      )}

                      {content.best_time_to_post && (
                        <div>
                          <p className="text-sm font-medium text-gray-700 mb-1">최적 게시 시간:</p>
                          <p className="text-gray-600 text-sm">{content.best_time_to_post}</p>
                        </div>
                      )}
                    </div>

                    <div className="mt-4 flex space-x-2">
                      <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition text-sm font-medium">
                        스케줄 등록
                      </button>
                      <button className="flex-1 border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 transition text-sm font-medium">
                        수정하기
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

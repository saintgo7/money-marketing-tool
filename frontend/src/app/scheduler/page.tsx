'use client';

import { useState, useEffect } from 'react';
import { Calendar, Clock, Plus, Edit, Trash2, Play } from 'lucide-react';

interface ScheduledPost {
  id: string;
  platform: string;
  content: string;
  scheduledTime: string;
  status: 'scheduled' | 'publishing' | 'published' | 'failed';
}

export default function SchedulerPage() {
  const [posts, setPosts] = useState<ScheduledPost[]>([]);
  const [view, setView] = useState<'list' | 'calendar'>('list');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScheduledPosts();
  }, []);

  const fetchScheduledPosts = async () => {
    setLoading(true);
    // Mock data
    setTimeout(() => {
      setPosts([
        {
          id: '1',
          platform: 'instagram',
          content: '5 Tips for Better Productivity...',
          scheduledTime: '2025-01-20T14:00:00',
          status: 'scheduled',
        },
        {
          id: '2',
          platform: 'linkedin',
          content: 'How AI is Transforming Marketing...',
          scheduledTime: '2025-01-21T10:00:00',
          status: 'scheduled',
        },
        {
          id: '3',
          platform: 'twitter',
          content: 'Quick marketing tip thread...',
          scheduledTime: '2025-01-19T18:00:00',
          status: 'published',
        },
      ]);
      setLoading(false);
    }, 1000);
  };

  const platformIcons: { [key: string]: string } = {
    instagram: '📸',
    facebook: '📘',
    twitter: '🐦',
    linkedin: '💼',
    tiktok: '🎵',
  };

  const statusColors = {
    scheduled: 'bg-blue-100 text-blue-800',
    publishing: 'bg-yellow-100 text-yellow-800',
    published: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">콘텐츠 스케줄러</h1>
            <p className="text-gray-600">예약된 게시물을 관리하고 최적 시간에 발행하세요</p>
          </div>

          <button className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
            <Plus className="w-5 h-5" />
            <span>새 예약</span>
          </button>
        </div>

        {/* View Toggle */}
        <div className="bg-white rounded-lg shadow-sm mb-6 p-4 flex items-center justify-between">
          <div className="flex space-x-2">
            <button
              onClick={() => setView('list')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                view === 'list'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              목록 보기
            </button>
            <button
              onClick={() => setView('calendar')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                view === 'calendar'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              캘린더 보기
            </button>
          </div>

          <div className="flex items-center space-x-4">
            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600">
              <option value="all">모든 플랫폼</option>
              <option value="instagram">Instagram</option>
              <option value="facebook">Facebook</option>
              <option value="twitter">Twitter</option>
              <option value="linkedin">LinkedIn</option>
            </select>

            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600">
              <option value="all">모든 상태</option>
              <option value="scheduled">예약됨</option>
              <option value="published">발행됨</option>
              <option value="failed">실패</option>
            </select>
          </div>
        </div>

        {/* Posts List */}
        {view === 'list' && (
          <div className="bg-white rounded-lg shadow-sm">
            {loading ? (
              <div className="p-12 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">로딩 중...</p>
              </div>
            ) : posts.length === 0 ? (
              <div className="p-12 text-center">
                <Calendar className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-600 mb-4">예약된 게시물이 없습니다</p>
                <button className="text-blue-600 hover:text-blue-700 font-medium">
                  첫 게시물 예약하기
                </button>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {posts.map((post) => (
                  <div key={post.id} className="p-6 hover:bg-gray-50 transition">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4 flex-1">
                        <div className="text-3xl">{platformIcons[post.platform]}</div>

                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="font-semibold text-lg capitalize">{post.platform}</h3>
                            <span
                              className={`px-3 py-1 rounded-full text-xs font-medium ${
                                statusColors[post.status]
                              }`}
                            >
                              {post.status === 'scheduled' && '예약됨'}
                              {post.status === 'publishing' && '발행 중'}
                              {post.status === 'published' && '발행됨'}
                              {post.status === 'failed' && '실패'}
                            </span>
                          </div>

                          <p className="text-gray-700 mb-3">{post.content}</p>

                          <div className="flex items-center space-x-4 text-sm text-gray-500">
                            <div className="flex items-center space-x-1">
                              <Calendar className="w-4 h-4" />
                              <span>
                                {new Date(post.scheduledTime).toLocaleDateString('ko-KR')}
                              </span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Clock className="w-4 h-4" />
                              <span>
                                {new Date(post.scheduledTime).toLocaleTimeString('ko-KR', {
                                  hour: '2-digit',
                                  minute: '2-digit',
                                })}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-2">
                        {post.status === 'scheduled' && (
                          <>
                            <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition">
                              <Edit className="w-5 h-5" />
                            </button>
                            <button className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition">
                              <Play className="w-5 h-5" />
                            </button>
                            <button className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition">
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Calendar View */}
        {view === 'calendar' && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="text-center py-12">
              <Calendar className="w-16 h-16 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">캘린더 뷰는 곧 추가됩니다</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

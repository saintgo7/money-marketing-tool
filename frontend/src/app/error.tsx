'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-red-50 to-white flex items-center justify-center p-4">
      <div className="text-center max-w-md">
        <div className="text-6xl mb-6">⚠️</div>
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          문제가 발생했습니다
        </h2>
        <p className="text-gray-600 mb-8">
          죄송합니다. 예상치 못한 오류가 발생했습니다.
          다시 시도해 주세요.
        </p>
        <div className="space-x-4">
          <button
            onClick={reset}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            다시 시도
          </button>
          <a
            href="/dashboard"
            className="inline-block bg-gray-200 text-gray-900 px-6 py-3 rounded-lg hover:bg-gray-300 transition"
          >
            대시보드로 가기
          </a>
        </div>
        {error.digest && (
          <p className="mt-4 text-sm text-gray-500">
            오류 ID: {error.digest}
          </p>
        )}
      </div>
    </div>
  );
}

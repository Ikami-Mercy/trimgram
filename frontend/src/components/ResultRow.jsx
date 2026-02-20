/**
 * ResultRow component - displays a single non-follower with unfollow button.
 */
import { useState } from 'react';

export default function ResultRow({ user, onUnfollow }) {
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleUnfollowClick = () => {
    setShowConfirmation(true);
    setError('');
  };

  const handleConfirm = async () => {
    setLoading(true);
    setError('');

    try {
      await onUnfollow(user.user_id);
      // Success - row will be removed by parent component
    } catch (err) {
      setError(err.message || 'Failed to unfollow');
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setShowConfirmation(false);
    setError('');
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        {/* User Info */}
        <div className="flex items-center space-x-3 flex-1 min-w-0">
          {/* Profile Picture */}
          <img
            src={user.profile_pic_url || 'https://via.placeholder.com/50'}
            alt={user.username}
            className="w-12 h-12 rounded-full object-cover flex-shrink-0"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/50';
            }}
          />

          {/* Username and Score */}
          <div className="flex-1 min-w-0">
            <a
              href={`https://instagram.com/${user.username}`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-semibold text-gray-900 hover:text-purple-600 block truncate"
            >
              @{user.username}
            </a>
            {user.full_name && (
              <p className="text-sm text-gray-500 truncate">{user.full_name}</p>
            )}
            <div className="mt-1">
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                {user.total_score === 0
                  ? 'No interactions'
                  : `${user.likes_count} likes, ${user.comments_count} comments`}
              </span>
            </div>
          </div>
        </div>

        {/* Unfollow Button */}
        <div className="ml-4 flex-shrink-0">
          {!showConfirmation ? (
            <button
              onClick={handleUnfollowClick}
              className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors"
            >
              Unfollow
            </button>
          ) : (
            <div className="flex space-x-2">
              <button
                onClick={handleCancel}
                disabled={loading}
                className="px-3 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium rounded-lg transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleConfirm}
                disabled={loading}
                className="px-3 py-2 bg-red-500 hover:bg-red-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 flex items-center"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-4 w-4 mr-1" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Confirming...
                  </>
                ) : (
                  'Confirm'
                )}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-3 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Confirmation Dialog (shown when showConfirmation is true) */}
      {showConfirmation && (
        <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded">
          <p className="text-sm text-gray-700">
            Are you sure you want to unfollow <strong>@{user.username}</strong>?
          </p>
        </div>
      )}
    </div>
  );
}

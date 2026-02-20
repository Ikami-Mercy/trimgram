/**
 * ResultsList component - displays the ranked list of non-followers.
 */
import { useState } from 'react';
import ResultRow from './ResultRow';

export default function ResultsList({ analysisData, onUnfollow }) {
  const [unfollowedUsers, setUnfollowedUsers] = useState(new Set());

  const handleUnfollow = async (userId) => {
    await onUnfollow(userId);
    // Add to unfollowed set to remove from UI
    setUnfollowedUsers(prev => new Set([...prev, userId]));
  };

  // Filter out unfollowed users
  const displayedResults = analysisData.results.filter(
    user => !unfollowedUsers.has(user.user_id)
  );

  // Check if all have been unfollowed or if there were none to begin with
  const isEmpty = displayedResults.length === 0;

  return (
    <div className="min-h-screen bg-gray-50 p-4 py-8">
      <div className="max-w-3xl mx-auto">
        {/* Header Stats */}
        <div className="mb-8">
          <div className="text-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Results</h1>
            {analysisData.non_followers_shown < analysisData.total_non_followers && (
              <div className="inline-block px-4 py-2 bg-purple-100 text-purple-800 rounded-lg text-sm font-medium">
                Showing your {analysisData.non_followers_shown} least-interacted non-followers
              </div>
            )}
          </div>

          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg p-4 text-center shadow-sm">
              <p className="text-2xl font-bold text-gray-900">
                {analysisData.total_following.toLocaleString()}
              </p>
              <p className="text-sm text-gray-600">Following</p>
            </div>
            <div className="bg-white rounded-lg p-4 text-center shadow-sm">
              <p className="text-2xl font-bold text-gray-900">
                {analysisData.total_followers.toLocaleString()}
              </p>
              <p className="text-sm text-gray-600">Followers</p>
            </div>
            <div className="bg-white rounded-lg p-4 text-center shadow-sm instagram-gradient">
              <p className="text-2xl font-bold text-white">
                {analysisData.total_non_followers.toLocaleString()}
              </p>
              <p className="text-sm text-white">Don't Follow Back</p>
            </div>
          </div>

          {!isEmpty && (
            <div className="bg-white rounded-lg p-4 shadow-sm">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-gray-900">
                    {displayedResults.length} accounts to review
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Listed from least to most interaction — start from the top. Accounts you've never liked or commented on appear first.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Results List or Empty State */}
        {isEmpty ? (
          <div className="bg-white rounded-lg p-12 text-center shadow-sm">
            <svg className="w-16 h-16 mx-auto text-green-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              All Done!
            </h2>
            <p className="text-gray-600">
              Everyone you follow, follows you back!
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {displayedResults.map((user) => (
              <ResultRow
                key={user.user_id}
                user={user}
                onUnfollow={handleUnfollow}
              />
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            Unfollowed {unfollowedUsers.size} account{unfollowedUsers.size !== 1 ? 's' : ''} this session
          </p>
        </div>
      </div>
    </div>
  );
}

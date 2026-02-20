/**
 * API service module for Trimgram frontend.
 * All API calls go through this module - NO API calls inside components.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Login with Instagram credentials.
 *
 * @param {string} username - Instagram username
 * @param {string} password - Instagram password
 * @returns {Promise<{session_token: string, user_id: number, message: string}>}
 * @throws {Error} Authentication error or 2FA required
 */
export async function login(username, password) {
  const response = await fetch(`${API_BASE_URL}/api/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    // Check for 2FA required
    if (response.status === 449) {
      const error = new Error(data.detail.message || '2FA required');
      error.code = '2FA_REQUIRED';
      error.sessionToken = data.detail.session_token;
      throw error;
    }

    // Other errors
    throw new Error(data.detail?.message || 'Login failed');
  }

  return data;
}

/**
 * Resolve 2FA challenge.
 *
 * @param {string} sessionToken - Temporary session token from initial login
 * @param {string} code - 6-digit 2FA code
 * @returns {Promise<{session_token: string, user_id: number, message: string}>}
 * @throws {Error} If 2FA verification fails
 */
export async function resolve2FA(sessionToken, code) {
  const response = await fetch(`${API_BASE_URL}/api/2fa`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ session_token: sessionToken, code }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail?.message || '2FA verification failed');
  }

  return data;
}

/**
 * Analyze followers and get ranked list of non-followers.
 *
 * @param {string} sessionToken - Session token from login
 * @returns {Promise<{total_following: number, total_followers: number, total_non_followers: number, non_followers_shown: number, results: Array}>}
 * @throws {Error} If analysis fails
 */
export async function analyzeFollowers(sessionToken) {
  const response = await fetch(`${API_BASE_URL}/api/analysis`, {
    method: 'GET',
    headers: {
      'session_token': sessionToken,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail?.message || 'Analysis failed');
  }

  return data;
}

/**
 * Unfollow a specific user.
 *
 * @param {string} sessionToken - Session token from login
 * @param {number} targetUserId - Instagram user ID to unfollow
 * @returns {Promise<{success: boolean, message: string}>}
 * @throws {Error} If unfollow fails
 */
export async function unfollowUser(sessionToken, targetUserId) {
  const response = await fetch(`${API_BASE_URL}/api/unfollow`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_token: sessionToken,
      target_user_id: targetUserId,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail?.message || 'Unfollow failed');
  }

  return data;
}

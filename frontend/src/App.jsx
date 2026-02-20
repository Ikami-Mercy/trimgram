/**
 * Main App component - handles application state and routing.
 */
import { useState } from 'react';
import LoginForm from './components/LoginForm';
import LoadingScreen from './components/LoadingScreen';
import ResultsList from './components/ResultsList';
import PrivacyPolicy from './components/PrivacyPolicy';
import * as api from './services/api';

function App() {
  const [currentView, setCurrentView] = useState('login'); // 'login', 'loading', 'results', 'privacy'
  const [sessionToken, setSessionToken] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [error, setError] = useState(null);

  // Check if we're on privacy page
  if (window.location.pathname === '/privacy') {
    return <PrivacyPolicy />;
  }

  const handleLogin = async (username, password) => {
    try {
      setError(null);
      setCurrentView('loading');

      // Step 1: Login
      const loginResponse = await api.login(username, password);
      const token = loginResponse.session_token;
      setSessionToken(token);

      // Step 2: Analyze followers
      const analysisResponse = await api.analyzeFollowers(token);
      setAnalysisData(analysisResponse);

      // Step 3: Show results
      setCurrentView('results');

    } catch (err) {
      // Handle 2FA - in MVP we'll just show an error
      if (err.code === '2FA_REQUIRED') {
        setError('This account has 2FA enabled. 2FA support is coming in a future update. Please disable 2FA temporarily to use Trimgram.');
      } else {
        setError(err.message);
      }
      setCurrentView('login');
      throw err; // Re-throw so LoginForm can show the error
    }
  };

  const handleUnfollow = async (userId) => {
    try {
      await api.unfollowUser(sessionToken, userId);
      // Success - ResultsList will handle UI updates
    } catch (err) {
      // Error will be shown in ResultRow
      throw err;
    }
  };

  return (
    <>
      {currentView === 'login' && (
        <LoginForm onLoginSuccess={handleLogin} />
      )}

      {currentView === 'loading' && (
        <LoadingScreen />
      )}

      {currentView === 'results' && analysisData && (
        <ResultsList
          analysisData={analysisData}
          onUnfollow={handleUnfollow}
        />
      )}
    </>
  );
}

export default App;

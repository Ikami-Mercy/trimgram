/**
 * LoadingScreen component - shown while analyzing Instagram data.
 */
export default function LoadingScreen() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center">
        {/* Spinner */}
        <div className="mb-6">
          <div className="w-20 h-20 mx-auto instagram-gradient rounded-full flex items-center justify-center animate-pulse">
            <svg
              className="w-12 h-12 text-white animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
        </div>

        {/* Message */}
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Analyzing Your Account
        </h2>
        <p className="text-gray-600 mb-1">
          Fetching your Instagram data...
        </p>
        <p className="text-gray-500 text-sm">
          This may take a minute.
        </p>

        {/* Sub-message */}
        <div className="mt-6 p-4 bg-white rounded-lg shadow-sm">
          <p className="text-sm text-gray-700">
            We are checking followers, following, and interaction history.
          </p>
        </div>

        {/* Progress indication */}
        <div className="mt-8">
          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div className="h-full instagram-gradient animate-progress-bar"></div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes progress-bar {
          0% {
            width: 0%;
          }
          50% {
            width: 60%;
          }
          100% {
            width: 90%;
          }
        }

        .animate-progress-bar {
          animation: progress-bar 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}

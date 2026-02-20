/**
 * PrivacyPolicy component - explains data handling and privacy practices.
 */
export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-gray-50 p-4 py-8">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>

        <div className="space-y-6 text-gray-700">
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              We Never Store Your Instagram Password. Ever.
            </h2>
            <p className="leading-relaxed">
              Your Instagram password is used only to create a temporary session via the
              instagrapi library. The password is never written to any log file, database,
              file system, or external service. It is held in memory for the duration of
              your session (30 minutes maximum) and then discarded.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              How Sessions Work
            </h2>
            <p className="leading-relaxed">
              When you log in, we create a temporary session token stored in server memory
              (not in a database). This session expires after 30 minutes of inactivity. There
              is no "remember me" feature — every visit requires a fresh login. Session tokens
              are randomly generated UUIDs and are not derived from any user data.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              What Data We Access
            </h2>
            <p className="leading-relaxed mb-2">
              When you use Trimgram, we temporarily access the following Instagram data through
              the Instagram Private API:
            </p>
            <ul className="list-disc list-inside space-y-1 ml-4">
              <li>Your followers list</li>
              <li>Your following list</li>
              <li>Recent posts from accounts you follow (to calculate interaction scores)</li>
              <li>Likes and comments on those posts (to measure your engagement)</li>
            </ul>
            <p className="leading-relaxed mt-2">
              This data is processed in real-time and is never stored permanently.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              No Database, No Persistent Storage
            </h2>
            <p className="leading-relaxed">
              Trimgram does not use a database. All session data is stored in server memory only.
              When your session expires or when the server restarts, all data is completely erased.
              We do not retain any information about your Instagram account, followers, or usage
              patterns.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              No Analytics, No Tracking
            </h2>
            <p className="leading-relaxed">
              We do not use Google Analytics, Facebook Pixel, or any other tracking or analytics
              service. We do not collect data about your browsing behavior, device information, or
              location. We do not share any data with third parties because we don't collect or
              store any data to share.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Security
            </h2>
            <p className="leading-relaxed">
              All communication between your browser and our servers is encrypted via HTTPS.
              Passwords are never logged or written to disk. Our application is designed with
              security in mind, following clean architecture and best practices for credential
              handling.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Open Source
            </h2>
            <p className="leading-relaxed">
              The entire Trimgram codebase is open source and available on GitHub. You can read
              the code yourself to verify these claims. We encourage security researchers and
              developers to audit the code and report any concerns.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Unofficial API Disclaimer
            </h2>
            <p className="leading-relaxed">
              Trimgram uses Instagram's unofficial private API (via the instagrapi library).
              This is not affiliated with, endorsed by, or approved by Instagram or Meta.
              While we implement rate limiting and delays to minimize risk, using this tool
              may result in your Instagram account being temporarily rate-limited or flagged.
              Use at your own discretion.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Questions or Concerns?
            </h2>
            <p className="leading-relaxed">
              If you have questions about how Trimgram handles your data, please review the
              source code on{' '}
              <a
                href="https://github.com/yourusername/trimgram"
                target="_blank"
                rel="noopener noreferrer"
                className="text-purple-600 hover:underline font-medium"
              >
                GitHub
              </a>
              {' '}or open an issue in the repository.
            </p>
          </section>

          <div className="pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Last updated: February 2026
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <a
            href="/"
            className="inline-flex items-center px-6 py-3 instagram-gradient text-white font-medium rounded-lg hover:opacity-90 transition-opacity"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Login
          </a>
        </div>
      </div>
    </div>
  );
}

import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-800 bg-gray-950">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div>
            <h3 className="text-sm font-semibold text-white">Practice</h3>
            <ul className="mt-4 space-y-2">
              <li><Link href="/questions" className="text-sm text-gray-400 hover:text-white">All Questions</Link></li>
              <li><Link href="/companies" className="text-sm text-gray-400 hover:text-white">By Company</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Categories</h3>
            <ul className="mt-4 space-y-2">
              <li><Link href="/data-engineering" className="text-sm text-gray-400 hover:text-white">Data Engineering</Link></li>
              <li><Link href="/data-science" className="text-sm text-gray-400 hover:text-white">Data Science</Link></li>
              <li><Link href="/machine-learning" className="text-sm text-gray-400 hover:text-white">Machine Learning</Link></li>
              <li><Link href="/data-analytics" className="text-sm text-gray-400 hover:text-white">Data Analytics</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">Community</h3>
            <ul className="mt-4 space-y-2">
              <li><Link href="/discuss" className="text-sm text-gray-400 hover:text-white">Discussions</Link></li>
              <li><Link href="/discuss?category=interview_experience" className="text-sm text-gray-400 hover:text-white">Interview Experiences</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-sm font-semibold text-white">About</h3>
            <ul className="mt-4 space-y-2">
              <li><Link href="https://github.com" className="text-sm text-gray-400 hover:text-white">GitHub</Link></li>
              <li><Link href="#" className="text-sm text-gray-400 hover:text-white">Contributing</Link></li>
            </ul>
          </div>
        </div>
        <div className="mt-10 border-t border-gray-800 pt-8">
          <p className="text-center text-sm text-gray-500">
            Built with care for the Data Community. MIT License.
          </p>
        </div>
      </div>
    </footer>
  );
}

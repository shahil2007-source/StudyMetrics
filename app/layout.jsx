import './globals.css';
import Sidebar from '../components/Sidebar';

export const metadata = {
  title: 'StudyMetrics - Student Analytics Platform',
  description: 'Correlation Analysis Between Social Media Usage and Academic Performance',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 antialiased min-h-screen">
        <div className="flex min-h-screen">
          {/* Sidebar */}
          <Sidebar />

          {/* Main Content Area */}
          <main className="flex-1 lg:ml-64 p-4 md:p-8 overflow-x-hidden">
            <div className="max-w-7xl mx-auto">{children}</div>
          </main>
        </div>
      </body>
    </html>
  );
}

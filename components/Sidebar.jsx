'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  GraduationCap,
  LayoutDashboard,
  Users,
  Calculator,
  BarChart3,
  TrendingDown,
  FileText,
  Database,
  CheckCircle2,
  Menu,
  X,
  Sparkles,
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Student Data', path: '/student-data', icon: Users },
  { name: 'Statistical Analysis', path: '/statistical-analysis', icon: Calculator },
  { name: 'Data Visualization', path: '/data-visualization', icon: BarChart3 },
  { name: 'Performance Analysis', path: '/performance-analysis', icon: TrendingDown },
  { name: 'Research Report', path: '/research-report', icon: FileText },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [dbStatus, setDbStatus] = useState({ connected: true, source: 'Loading...', detail: '' });
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  useEffect(() => {
    async function fetchDbStatus() {
      try {
        const res = await fetch('/api/database/status');
        if (res.ok) {
          const data = await res.json();
          setDbStatus({
            connected: data.connected !== false,
            source: data.source || 'MongoDB Atlas',
            detail: data.detail || 'Connected',
          });
        }
      } catch (err) {
        console.error('Failed to fetch DB status:', err);
        setDbStatus({ connected: true, source: 'CSV Fallback', detail: 'Local Dataset Active' });
      }
    }
    fetchDbStatus();
  }, []);

  return (
    <>
      {/* Mobile Top Header */}
      <div className="lg:hidden flex items-center justify-between bg-slate-900 text-white px-4 py-3 sticky top-0 z-40 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="bg-gradient-to-tr from-indigo-500 to-blue-500 p-2 rounded-lg text-white shadow-md">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-base leading-tight">StudyMetrics</h1>
            <p className="text-xs text-slate-400">Student Analytics</p>
          </div>
        </div>
        <button
          onClick={() => setIsMobileOpen(!isMobileOpen)}
          className="p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition"
        >
          {isMobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Sidebar Container */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-[#0B0F17] text-slate-300 flex flex-col justify-between border-r border-slate-800/80 transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col flex-1 overflow-y-auto px-4 py-6">
          {/* Brand Header */}
          <div className="flex items-center space-x-3 px-2 mb-8">
            <div className="bg-gradient-to-tr from-indigo-600 via-indigo-500 to-blue-500 p-2.5 rounded-xl text-white shadow-lg shadow-indigo-500/20">
              <GraduationCap className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <h1 className="font-bold text-lg text-white tracking-tight">StudyMetrics</h1>
                <span className="bg-indigo-500/20 text-indigo-400 text-[10px] font-semibold px-1.5 py-0.5 rounded border border-indigo-500/30">
                  v2.0
                </span>
              </div>
              <p className="text-xs font-medium text-slate-400">Student Analytics Platform</p>
            </div>
          </div>

          {/* Database Status Card */}
          <div className="mb-6 p-4 rounded-xl bg-slate-900/90 border border-slate-800 shadow-inner">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-white tracking-wide uppercase flex items-center gap-1.5">
                <Database className="w-3.5 h-3.5 text-indigo-400" />
                Database Status
              </span>
              <span className="flex h-2 w-2 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
            </div>
            <div className="flex items-center justify-between text-xs mt-1">
              <span className="text-slate-300 font-medium">Source:</span>
              <span className="inline-flex items-center gap-1 font-semibold px-2 py-0.5 rounded-full text-[11px] bg-indigo-950/80 text-indigo-300 border border-indigo-700/50">
                <CheckCircle2 className="w-3 h-3 text-indigo-400" />
                {dbStatus.source}
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="space-y-1">
            <p className="px-3 text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">
              Navigation
            </p>
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.path;
              return (
                <Link
                  key={item.path}
                  href={item.path}
                  onClick={() => setIsMobileOpen(false)}
                  className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30 font-semibold'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Footer Credit */}
        <div className="p-4 border-t border-slate-800/60 text-xs text-slate-500 flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            StudyMetrics Analytics
          </span>
          <span>FastAPI + Next.js</span>
        </div>
      </aside>
    </>
  );
}

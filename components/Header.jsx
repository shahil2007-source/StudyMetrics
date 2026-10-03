'use client';

import React from 'react';
import { Calendar, Layers } from 'lucide-react';

export default function Header({ title, description, badge }) {
  const currentDate = new Date().toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <header className="bg-white border-b border-slate-200 px-6 py-5 rounded-2xl shadow-sm mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">{title}</h1>
          {badge && (
            <span className="bg-indigo-50 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full border border-indigo-200">
              {badge}
            </span>
          )}
        </div>
        <p className="text-sm text-slate-500 mt-1">{description}</p>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 bg-slate-50 text-slate-600 px-3.5 py-1.5 rounded-xl border border-slate-200 text-xs font-medium">
          <Calendar className="w-3.5 h-3.5 text-indigo-600" />
          <span>{currentDate}</span>
        </div>
        <div className="flex items-center gap-2 bg-indigo-50 text-indigo-700 px-3.5 py-1.5 rounded-xl border border-indigo-200 text-xs font-semibold">
          <Layers className="w-3.5 h-3.5" />
          <span>Sample Students Dataset</span>
        </div>
      </div>
    </header>
  );
}

'use client';

import React, { useState } from 'react';
import Header from '../../components/Header';
import { FileText, Download, CheckCircle2, Sparkles, Send, FileCheck } from 'lucide-react';

export default function ResearchReport() {
  const [formData, setFormData] = useState({
    title: 'StudyMetrics Analytical Research Report',
    author: 'Department of Student Analytics',
    institution: 'StudyMetrics Educational Research Institute',
    targetAudience: 'Academic Deans & Student Success Officers',
    executiveSummary:
      'This research report evaluates the empirical relationship between daily social media consumption and academic performance among undergraduate students. Quantitative analysis confirms a strong negative correlation.',
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);

  const handleDownloadPdf = async (e) => {
    e.preventDefault();
    setIsGenerating(true);
    setSuccessMsg(null);

    try {
      const res = await fetch('/api/report/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!res.ok) throw new Error('Failed to compile PDF report');

      // Get PDF blob
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      // Create download link
      const a = document.createElement('a');
      a.href = url;
      a.download = `StudyMetrics_Research_Report_${Date.now()}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setSuccessMsg('PDF Report compiled and downloaded successfully!');
    } catch (err) {
      console.error(err);
      alert('Error generating PDF report. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div>
      <Header
        title="Research Report Generator"
        description="Compile and export publication-ready PDF research reports with embedded statistics & charts."
        badge="ReportLab Engine"
      />

      {successMsg && (
        <div className="mb-6 p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <span className="text-sm font-semibold">{successMsg}</span>
          </div>
          <button onClick={() => setSuccessMsg(null)} className="text-slate-400 hover:text-slate-600">
            &times;
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Form Configuration */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-center space-x-2 mb-6">
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-900">Report Configuration Form</h3>
              <p className="text-xs text-slate-500">Specify report metadata, title, author, and custom executive summary.</p>
            </div>
          </div>

          <form onSubmit={handleDownloadPdf} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Report Title
              </label>
              <input
                type="text"
                required
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Author / Researcher
                </label>
                <input
                  type="text"
                  required
                  value={formData.author}
                  onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                  className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Institution
                </label>
                <input
                  type="text"
                  required
                  value={formData.institution}
                  onChange={(e) => setFormData({ ...formData, institution: e.target.value })}
                  className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Target Audience
              </label>
              <input
                type="text"
                required
                value={formData.targetAudience}
                onChange={(e) => setFormData({ ...formData, targetAudience: e.target.value })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                Executive Summary Note
              </label>
              <textarea
                rows={4}
                required
                value={formData.executiveSummary}
                onChange={(e) => setFormData({ ...formData, executiveSummary: e.target.value })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              ></textarea>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isGenerating}
                className="w-full py-3 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white font-bold rounded-xl shadow-md flex items-center justify-center space-x-2 transition disabled:opacity-50"
              >
                {isGenerating ? (
                  <>
                    <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24" fill="none">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    <span>Compiling ReportLab PDF...</span>
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    <span>Download PDF Research Report</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Right Column: Interactive Outline Preview */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-6">
              <div className="p-2 bg-purple-50 text-purple-600 rounded-xl">
                <FileCheck className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">PDF Report Document Structure</h3>
                <p className="text-xs text-slate-500">Preview sections automatically compiled into the final PDF.</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">Section 1</span>
                  <span className="text-xs text-slate-400">Page 1</span>
                </div>
                <h4 className="font-bold text-slate-900 mt-1">Title, Metadata & Executive Summary</h4>
                <p className="text-xs text-slate-500 mt-1">Includes author details, date, institution, and executive overview.</p>
              </div>

              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">Section 2</span>
                  <span className="text-xs text-slate-400">Page 1-2</span>
                </div>
                <h4 className="font-bold text-slate-900 mt-1">Quantitative Correlation Analysis</h4>
                <p className="text-xs text-slate-500 mt-1">
                  Pearson r, Spearman &rho;, p-values, and correlation matrix breakdown.
                </p>
              </div>

              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">Section 3</span>
                  <span className="text-xs text-slate-400">Page 2</span>
                </div>
                <h4 className="font-bold text-slate-900 mt-1">Descriptive Cohort Statistics</h4>
                <p className="text-xs text-slate-500 mt-1">
                  Full metrics breakdown table (Mean, Std, Min, Max, Quartiles).
                </p>
              </div>

              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">Section 4</span>
                  <span className="text-xs text-slate-400">Page 2</span>
                </div>
                <h4 className="font-bold text-slate-900 mt-1">Performance Risk Tiers & Recommendations</h4>
                <p className="text-xs text-slate-500 mt-1">
                  High-risk student cohort identification and academic intervention strategies.
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span className="flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-indigo-600" /> Powered by ReportLab & Python FastAPI
            </span>
            <span className="font-semibold text-slate-700">A4 PDF Output</span>
          </div>
        </div>
      </div>
    </div>
  );
}

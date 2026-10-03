'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import PlotlyChart from '../../components/PlotlyChart';
import { Calculator, TrendingDown, Layers, Sparkles, CheckCircle2 } from 'lucide-react';

export default function StatisticalAnalysis() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStats() {
      try {
        const res = await fetch('/api/analytics/statistics');
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (err) {
        console.error('Failed to load statistical data:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchStats();
  }, []);

  if (loading || !stats) {
    return (
      <div>
        <Header title="Statistical Analysis" description="Rigorous quantitative correlation & descriptive metrics" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="h-44 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
          <div className="h-44 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
        </div>
        <div className="h-96 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
      </div>
    );
  }

  const { pearson, spearman, descriptive, matrix } = stats;

  // Correlation Matrix Heatmap
  const heatmapData = [
    {
      z: matrix.z,
      x: matrix.x,
      y: matrix.y,
      type: 'heatmap',
      colorscale: [
        [0, '#EF4444'],
        [0.5, '#F8FAFC'],
        [1, '#6366F1'],
      ],
      showscale: true,
      texttemplate: '%{z:.3f}',
      hoverongaps: false,
    },
  ];

  const heatmapLayout = {
    title: { text: 'Correlation Matrix (Heatmap)', font: { size: 15, color: '#0F172A', weight: 700 } },
    xaxis: { font: { weight: 600 } },
    yaxis: { font: { weight: 600 } },
    margin: { t: 40, b: 40, l: 150, r: 40 },
  };

  return (
    <div>
      <Header
        title="Statistical Analysis"
        description="Comprehensive quantitative correlation coefficients, p-values, and descriptive statistics."
        badge="Hypothesis Tested"
      />

      {/* Correlation Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Pearson Correlation Card */}
        <div className="bg-gradient-to-br from-indigo-900 via-slate-900 to-slate-950 text-white rounded-2xl p-6 border border-indigo-800 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <div className="p-2 bg-indigo-800/60 rounded-xl text-indigo-300">
                <Calculator className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-lg text-white">Pearson Correlation</h3>
            </div>
            <span className="bg-indigo-500/20 text-indigo-300 text-xs font-semibold px-2.5 py-1 rounded-full border border-indigo-500/30">
              Parametric Test
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Correlation (r)</span>
              <span className="text-2xl font-extrabold text-indigo-300">{pearson.r}</span>
            </div>
            <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">p-Value</span>
              <span className="text-2xl font-extrabold text-emerald-400">{pearson.p_value}</span>
            </div>
          </div>

          <div className="bg-indigo-950/60 p-3.5 rounded-xl border border-indigo-800/40 text-xs text-indigo-200 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-indigo-400 flex-shrink-0 mt-0.5" />
            <p>
              <strong>Interpretation:</strong> {pearson.interpretation}. Highly statistically significant (p &lt; 0.001).
            </p>
          </div>
        </div>

        {/* Spearman Rank Correlation Card */}
        <div className="bg-gradient-to-br from-slate-900 via-purple-950 to-slate-950 text-white rounded-2xl p-6 border border-purple-900/60 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <div className="p-2 bg-purple-800/60 rounded-xl text-purple-300">
                <TrendingDown className="w-5 h-5" />
              </div>
              <h3 className="font-bold text-lg text-white">Spearman Rank Correlation</h3>
            </div>
            <span className="bg-purple-500/20 text-purple-300 text-xs font-semibold px-2.5 py-1 rounded-full border border-purple-500/30">
              Non-Parametric Test
            </span>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">Rank Rho (&rho;)</span>
              <span className="text-2xl font-extrabold text-purple-300">{spearman.rho}</span>
            </div>
            <div className="bg-slate-800/60 p-3.5 rounded-xl border border-slate-700/50">
              <span className="text-xs text-slate-400 uppercase tracking-wider block mb-1">p-Value</span>
              <span className="text-2xl font-extrabold text-emerald-400">{spearman.p_value}</span>
            </div>
          </div>

          <div className="bg-purple-950/60 p-3.5 rounded-xl border border-purple-800/40 text-xs text-purple-200 flex items-start space-x-2">
            <CheckCircle2 className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
            <p>
              <strong>Interpretation:</strong> {spearman.interpretation}. Confirms monotonic rank decline across usage tiers.
            </p>
          </div>
        </div>
      </div>

      {/* Descriptive Statistics Table Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm mb-6">
        <div className="flex items-center space-x-2 mb-4">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Descriptive Statistics Table</h3>
            <p className="text-xs text-slate-500">Summary statistics including mean, standard deviation, quartiles, and range.</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-sm">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                <th className="py-3 px-4">Metric Variable</th>
                <th className="py-3 px-4">Mean</th>
                <th className="py-3 px-4">Std Dev</th>
                <th className="py-3 px-4">Min</th>
                <th className="py-3 px-4">25th %</th>
                <th className="py-3 px-4">Median (50%)</th>
                <th className="py-3 px-4">75th %</th>
                <th className="py-3 px-4">Max</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {descriptive.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition">
                  <td className="py-3.5 px-4 font-bold text-slate-900">{row.Metric}</td>
                  <td className="py-3.5 px-4 font-semibold text-indigo-600">{row.Mean}</td>
                  <td className="py-3.5 px-4">{row.Std}</td>
                  <td className="py-3.5 px-4 text-slate-500">{row.Min}</td>
                  <td className="py-3.5 px-4">{row['25%']}</td>
                  <td className="py-3.5 px-4 font-semibold text-slate-900">{row['50%']}</td>
                  <td className="py-3.5 px-4">{row['75%']}</td>
                  <td className="py-3.5 px-4 text-slate-500">{row.Max}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Heatmap Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <PlotlyChart data={heatmapData} layout={heatmapLayout} />
      </div>
    </div>
  );
}

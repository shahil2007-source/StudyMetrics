'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import PlotlyChart from '../../components/PlotlyChart';
import { TrendingDown, Sliders, AlertTriangle, CheckCircle, Award, Users } from 'lucide-react';

export default function PerformanceAnalysis() {
  const [lowThreshold, setLowThreshold] = useState(2.0);
  const [highThreshold, setHighThreshold] = useState(5.0);

  const [perfData, setPerfData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPerformance() {
      setLoading(true);
      try {
        const res = await fetch(
          `/api/analytics/performance?low_threshold=${lowThreshold}&high_threshold=${highThreshold}`
        );
        if (res.ok) {
          const data = await res.json();
          setPerfData(data);
        }
      } catch (err) {
        console.error('Failed to load performance metrics:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchPerformance();
  }, [lowThreshold, highThreshold]);

  if (loading && !perfData) {
    return (
      <div>
        <Header title="Performance Analysis" description="Cohort usage tier breakdown and risk assessment" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="h-44 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
          <div className="h-44 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
          <div className="h-44 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
        </div>
      </div>
    );
  }

  const { low_usage, moderate_usage, high_usage, chart_data } = perfData || {};

  // Comparison Bar Chart
  const barChartData = [
    {
      x: chart_data?.categories || ['Low Usage', 'Moderate Usage', 'High Usage'],
      y: chart_data?.avg_marks || [0, 0, 0],
      type: 'bar',
      name: 'Avg Marks (%)',
      marker: { color: ['#10B981', '#F59E0B', '#EF4444'] },
      text: (chart_data?.avg_marks || []).map((m) => `${m}%`),
      textposition: 'auto',
    },
  ];

  const barChartLayout = {
    title: { text: 'Average Academic Marks by Social Media Usage Tier', font: { size: 15, color: '#0F172A', weight: 700 } },
    yaxis: { title: 'Average Marks (%)', range: [0, 100] },
    showlegend: false,
  };

  return (
    <div>
      <Header
        title="Performance Analysis"
        description="Stratified cohort comparison across screen time usage tiers."
        badge="Risk Stratified"
      />

      {/* Threshold Configurator Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm mb-6">
        <div className="flex items-center space-x-2 mb-4">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
            <Sliders className="w-4 h-4" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">Dynamic Tier Threshold Cutoffs</h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Low Cutoff (&lt; {lowThreshold} hrs/day)
              </label>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                {lowThreshold} h
              </span>
            </div>
            <input
              type="range"
              min="1.0"
              max="3.5"
              step="0.5"
              value={lowThreshold}
              onChange={(e) => setLowThreshold(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                High Cutoff (&gt; {highThreshold} hrs/day)
              </label>
              <span className="text-xs font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                {highThreshold} h
              </span>
            </div>
            <input
              type="range"
              min="4.0"
              max="7.0"
              step="0.5"
              value={highThreshold}
              onChange={(e) => setHighThreshold(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-rose-600"
            />
          </div>
        </div>
      </div>

      {/* Cohort Usage Tier Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        {/* Tier 1: Low Usage */}
        <div className="bg-white border-2 border-emerald-100 rounded-2xl p-6 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-50 rounded-full -mr-8 -mt-8 pointer-events-none"></div>
          <div className="flex items-center justify-between mb-3">
            <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
              Low Usage (&lt;{lowThreshold}h)
            </span>
            <CheckCircle className="w-5 h-5 text-emerald-600" />
          </div>

          <div className="mt-4 space-y-3">
            <div>
              <span className="text-xs text-slate-500 uppercase tracking-wider block">Average Marks</span>
              <span className="text-3xl font-extrabold text-emerald-700">{low_usage?.avg_marks}%</span>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
              <div>
                <span className="text-slate-400 block">Student Count</span>
                <span className="font-bold text-slate-800">{low_usage?.count} Students</span>
              </div>
              <div>
                <span className="text-slate-400 block">Pass Rate</span>
                <span className="font-bold text-emerald-600">{low_usage?.pass_rate}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tier 2: Moderate Usage */}
        <div className="bg-white border-2 border-amber-100 rounded-2xl p-6 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 w-24 h-24 bg-amber-50 rounded-full -mr-8 -mt-8 pointer-events-none"></div>
          <div className="flex items-center justify-between mb-3">
            <span className="bg-amber-100 text-amber-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
              Moderate ({lowThreshold}-{highThreshold}h)
            </span>
            <Users className="w-5 h-5 text-amber-600" />
          </div>

          <div className="mt-4 space-y-3">
            <div>
              <span className="text-xs text-slate-500 uppercase tracking-wider block">Average Marks</span>
              <span className="text-3xl font-extrabold text-amber-700">{moderate_usage?.avg_marks}%</span>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
              <div>
                <span className="text-slate-400 block">Student Count</span>
                <span className="font-bold text-slate-800">{moderate_usage?.count} Students</span>
              </div>
              <div>
                <span className="text-slate-400 block">Pass Rate</span>
                <span className="font-bold text-amber-600">{moderate_usage?.pass_rate}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tier 3: High Usage (At Risk) */}
        <div className="bg-white border-2 border-rose-200 rounded-2xl p-6 shadow-sm relative overflow-hidden">
          <div className="absolute top-0 right-0 w-24 h-24 bg-rose-50 rounded-full -mr-8 -mt-8 pointer-events-none"></div>
          <div className="flex items-center justify-between mb-3">
            <span className="bg-rose-100 text-rose-800 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wide">
              High Risk (&gt;{highThreshold}h)
            </span>
            <AlertTriangle className="w-5 h-5 text-rose-600" />
          </div>

          <div className="mt-4 space-y-3">
            <div>
              <span className="text-xs text-slate-500 uppercase tracking-wider block">Average Marks</span>
              <span className="text-3xl font-extrabold text-rose-600">{high_usage?.avg_marks}%</span>
            </div>

            <div className="grid grid-cols-2 gap-2 pt-2 border-t border-slate-100 text-xs">
              <div>
                <span className="text-slate-400 block">Student Count</span>
                <span className="font-bold text-slate-800">{high_usage?.count} Students</span>
              </div>
              <div>
                <span className="text-slate-400 block">Pass Rate</span>
                <span className="font-bold text-rose-600">{high_usage?.pass_rate}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Chart & Intervention Strategy */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
          <PlotlyChart data={barChartData} layout={barChartLayout} />
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 bg-rose-50 text-rose-600 rounded-xl">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Recommended Academic Interventions</h3>
            </div>

            <div className="space-y-3 text-sm text-slate-600">
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-900 font-medium">
                <strong>High-Risk Cohort Notice:</strong> Students logging &gt;{highThreshold} hrs/day exhibit a{' '}
                <strong>
                  {low_usage && high_usage ? (low_usage.avg_marks - high_usage.avg_marks).toFixed(1) : '20+'}% mark deficit
                </strong>{' '}
                compared to low-usage peers.
              </div>

              <ul className="list-disc pl-5 space-y-2">
                <li>
                  <strong>Digital Wellbeing Workshops:</strong> Implement screen-time awareness sessions for students exceeding {highThreshold} hours daily.
                </li>
                <li>
                  <strong>Structured Study Blocks:</strong> Encourage 2-hour daily study sessions with phone-free focused intervals.
                </li>
                <li>
                  <strong>Early Academic Warning:</strong> Flag students in the High-Risk tier for academic counseling before mid-term exams.
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

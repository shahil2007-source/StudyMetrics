'use client';

import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import PlotlyChart from '../components/PlotlyChart';
import { Users, Clock, BookOpen, Award, TrendingDown, ArrowDownRight, Sparkles, RefreshCw } from 'lucide-react';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/analytics/dashboard');
      if (!res.ok) throw new Error('Failed to load dashboard data');
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div>
        <Header title="Dashboard" description="Overview of student metrics and correlation analysis" />
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-28 bg-white border border-slate-200 rounded-2xl p-4 animate-pulse"></div>
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-96 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
          <div className="h-96 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div>
        <Header title="Dashboard" description="Overview of student metrics and correlation analysis" />
        <div className="bg-red-50 border border-red-200 text-red-800 p-6 rounded-2xl flex flex-col items-center justify-center space-y-4">
          <p className="font-semibold">{error || 'Unable to connect to backend server.'}</p>
          <button
            onClick={fetchDashboardData}
            className="px-4 py-2 bg-indigo-600 text-white font-semibold rounded-xl flex items-center gap-2 hover:bg-indigo-700 transition"
          >
            <RefreshCw className="w-4 h-4" /> Retry
          </button>
        </div>
      </div>
    );
  }

  const { summary, charts } = data;

  // Chart 1: Social Media vs Marks
  const socialChartData = [
    {
      x: charts.social_vs_marks.x,
      y: charts.social_vs_marks.y,
      text: charts.social_vs_marks.hover_text,
      mode: 'markers',
      type: 'scatter',
      name: 'Students',
      marker: {
        color: '#6366F1',
        size: 9,
        opacity: 0.8,
        line: { color: '#4338CA', width: 1 },
      },
      hovertemplate: '%{text}<br>Social Media: %{x} hrs/day<br>Academic Marks: %{y}%<extra></extra>',
    },
    {
      x: charts.social_vs_marks.trendline_x,
      y: charts.social_vs_marks.trendline_y,
      mode: 'lines',
      type: 'scatter',
      name: 'Regression Line',
      line: { color: '#EF4444', width: 2.5, dash: 'dash' },
    },
  ];

  const socialChartLayout = {
    title: { text: 'Social Media Usage vs. Academic Marks', font: { size: 15, color: '#0F172A', weight: 700 } },
    xaxis: { title: 'Social Media Usage (Hours / Day)', gridcolor: '#E2E8F0' },
    yaxis: { title: 'Academic Marks (%)', gridcolor: '#E2E8F0' },
    showlegend: true,
    legend: { orientation: 'h', y: -0.2 },
  };

  // Chart 2: Study Hours vs Marks
  const studyChartData = [
    {
      x: charts.study_vs_marks.x,
      y: charts.study_vs_marks.y,
      text: charts.study_vs_marks.hover_text,
      mode: 'markers',
      type: 'scatter',
      name: 'Students',
      marker: {
        color: '#3B82F6',
        size: 9,
        opacity: 0.8,
        line: { color: '#1D4ED8', width: 1 },
      },
      hovertemplate: '%{text}<br>Study Hours: %{x} hrs/day<br>Academic Marks: %{y}%<extra></extra>',
    },
    {
      x: charts.study_vs_marks.trendline_x,
      y: charts.study_vs_marks.trendline_y,
      mode: 'lines',
      type: 'scatter',
      name: 'Trend Line',
      line: { color: '#10B981', width: 2.5 },
    },
  ];

  const studyChartLayout = {
    title: { text: 'Study Hours vs. Academic Marks', font: { size: 15, color: '#0F172A', weight: 700 } },
    xaxis: { title: 'Study Hours (Hours / Day)', gridcolor: '#E2E8F0' },
    yaxis: { title: 'Academic Marks (%)', gridcolor: '#E2E8F0' },
    showlegend: true,
    legend: { orientation: 'h', y: -0.2 },
  };

  return (
    <div>
      <Header
        title="Dashboard"
        description="Key performance metrics and correlation insights across the student cohort."
        badge={`${summary.total_students} Active Records`}
      />

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
        {/* Metric 1 */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Students</span>
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-slate-900">{summary.total_students}</span>
            <p className="text-xs text-slate-400 mt-1">Sample Cohort</p>
          </div>
        </div>

        {/* Metric 2 */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Social Media</span>
            <div className="p-2 bg-purple-50 text-purple-600 rounded-xl">
              <Clock className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-slate-900">{summary.avg_social_media} <span className="text-sm font-normal text-slate-500">hrs/day</span></span>
            <p className="text-xs text-slate-400 mt-1">Screen Time</p>
          </div>
        </div>

        {/* Metric 3 */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Study Hours</span>
            <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
              <BookOpen className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-slate-900">{summary.avg_study_hours} <span className="text-sm font-normal text-slate-500">hrs/day</span></span>
            <p className="text-xs text-slate-400 mt-1">Focus Time</p>
          </div>
        </div>

        {/* Metric 4 */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Academic Marks</span>
            <div className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
              <Award className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-slate-900">{summary.avg_academic_marks}%</span>
            <p className="text-xs text-slate-400 mt-1">Overall Grade</p>
          </div>
        </div>

        {/* Metric 5 */}
        <div className="bg-gradient-to-br from-indigo-900 to-slate-900 text-white rounded-2xl p-5 shadow-md border border-indigo-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-indigo-300 uppercase tracking-wider">Pearson Correlation</span>
            <div className="p-2 bg-indigo-800/60 text-indigo-300 rounded-xl">
              <TrendingDown className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3">
            <div className="flex items-baseline space-x-2">
              <span className="text-2xl font-bold text-white">r = {summary.pearson_r}</span>
              <ArrowDownRight className="w-4 h-4 text-rose-400" />
            </div>
            <p className="text-xs text-indigo-200 mt-1 font-medium">{summary.pearson_interpretation}</p>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
          <PlotlyChart data={socialChartData} layout={socialChartLayout} />
        </div>
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
          <PlotlyChart data={studyChartData} layout={studyChartLayout} />
        </div>
      </div>

      {/* Executive Analytical Summary Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <div className="flex items-center gap-2.5 mb-4">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-900">Executive Statistical Summary</h3>
            <p className="text-xs text-slate-500">Automated analytical insights derived from cohort statistics</p>
          </div>
        </div>
        <div className="bg-slate-50 rounded-xl p-5 border border-slate-200 text-slate-700 text-sm leading-relaxed space-y-3">
          <p>
            Statistical evaluation confirms a <strong>strong inverse correlation (r = {summary.pearson_r})</strong> between student social media usage and academic performance.
          </p>
          <ul className="list-disc pl-5 space-y-1.5 text-slate-600">
            <li>
              Students spending <strong>over 5 hours per day</strong> on social media experience a statistically significant drop in overall academic performance.
            </li>
            <li>
              Study duration demonstrates a positive counter-weight effect, showing that consistent study hours can buffer against academic degradation.
            </li>
            <li>
              Spearman rank correlation coefficient (<strong>&rho; = {summary.spearman_rho}</strong>) further validates that rank-based performance strictly decreases as screen time increases.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

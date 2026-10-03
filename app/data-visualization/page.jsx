'use client';

import React, { useEffect, useState } from 'react';
import Header from '../../components/Header';
import PlotlyChart from '../../components/PlotlyChart';
import { BarChart3, Filter, Sliders, Layers } from 'lucide-react';

export default function DataVisualization() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [selectedTier, setSelectedTier] = useState('ALL');
  const [minMarks, setMinMarks] = useState(0);

  useEffect(() => {
    async function fetchStudents() {
      try {
        const res = await fetch('/api/students');
        if (res.ok) {
          const data = await res.json();
          const list = Array.isArray(data) ? data : (data?.data || []);
          setStudents(list);
        }
      } catch (err) {
        console.error('Failed to load students:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchStudents();
  }, []);

  if (loading) {
    return (
      <div>
        <Header title="Data Visualization" description="Interactive Plotly.js exploratory charts" />
        <div className="h-24 bg-white border border-slate-200 rounded-2xl animate-pulse mb-6"></div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="h-96 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
          <div className="h-96 bg-white border border-slate-200 rounded-2xl animate-pulse"></div>
        </div>
      </div>
    );
  }

  // Filter students based on state
  const studentList = Array.isArray(students) ? students : [];
  const filtered = studentList.filter((s) => {
    const marks = parseFloat(s.Academic_Marks ?? s.academic_marks ?? 0);
    const usage = parseFloat(s.Social_Media_Usage_Hours ?? s.social_media_hours ?? 0);

    if (marks < minMarks) return false;

    if (selectedTier === 'LOW') return usage < 2.0;
    if (selectedTier === 'MODERATE') return usage >= 2.0 && usage <= 5.0;
    if (selectedTier === 'HIGH') return usage > 5.0;

    return true;
  });

  // Chart 1: 2D Scatter - Social Media vs Academic Marks
  const scatter2DData = [
    {
      x: filtered.map((s) => parseFloat(s.Social_Media_Usage_Hours)),
      y: filtered.map((s) => parseFloat(s.Academic_Marks)),
      text: filtered.map((s) => s.Name || s.Student_ID),
      mode: 'markers',
      type: 'scatter',
      marker: {
        color: filtered.map((s) => parseFloat(s.Academic_Marks)),
        colorscale: 'Viridis',
        size: 10,
        showscale: true,
        colorbar: { title: 'Marks %', thickness: 15 },
      },
      hovertemplate: '<b>%{text}</b><br>Social Media: %{x} hrs/day<br>Marks: %{y}%<extra></extra>',
    },
  ];

  const scatter2DLayout = {
    title: { text: 'Social Media vs. Academic Marks (Filtered Cohort)', font: { size: 15, color: '#0F172A', weight: 700 } },
    xaxis: { title: 'Social Media Usage (Hours / Day)' },
    yaxis: { title: 'Academic Marks (%)' },
  };

  // Chart 2: 3D Scatter Plot (Social Media vs Study Hours vs Marks)
  const scatter3DData = [
    {
      x: filtered.map((s) => parseFloat(s.Social_Media_Usage_Hours)),
      y: filtered.map((s) => parseFloat(s.Study_Hours)),
      z: filtered.map((s) => parseFloat(s.Academic_Marks)),
      text: filtered.map((s) => s.Name || s.Student_ID),
      mode: 'markers',
      type: 'scatter3d',
      marker: {
        size: 6,
        color: filtered.map((s) => parseFloat(s.Academic_Marks)),
        colorscale: 'Plasma',
        opacity: 0.85,
      },
      hovertemplate:
        '<b>%{text}</b><br>Social Media: %{x} hrs<br>Study Hours: %{y} hrs<br>Academic Marks: %{z}%<extra></extra>',
    },
  ];

  const scatter3DLayout = {
    title: { text: '3D Interaction: Social Media x Study Hours x Academic Marks', font: { size: 14, color: '#0F172A', weight: 700 } },
    scene: {
      xaxis: { title: 'Social Media (h)' },
      yaxis: { title: 'Study Hours (h)' },
      zaxis: { title: 'Marks (%)' },
    },
    margin: { l: 0, r: 0, b: 0, t: 30 },
  };

  // Chart 3: Distribution Histogram of Marks
  const histData = [
    {
      x: filtered.map((s) => parseFloat(s.Academic_Marks)),
      type: 'histogram',
      marker: { color: '#6366F1', line: { color: '#4338CA', width: 1 } },
      opacity: 0.8,
      nbinsx: 15,
    },
  ];

  const histLayout = {
    title: { text: 'Grade Distribution Across Filtered Cohort', font: { size: 15, color: '#0F172A', weight: 700 } },
    xaxis: { title: 'Academic Marks (%)' },
    yaxis: { title: 'Student Count' },
  };

  return (
    <div>
      <Header
        title="Data Visualization"
        description="Interactive multidimensional exploration using Plotly.js visual analytics."
        badge={`${filtered.length} / ${students.length} Filtered`}
      />

      {/* Filter Toolbar Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm mb-6">
        <div className="flex items-center space-x-2 mb-4">
          <div className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
            <Filter className="w-4 h-4" />
          </div>
          <h3 className="font-bold text-slate-900 text-sm">Interactive Cohort Filters</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Filter 1: Usage Tier */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
              Social Media Usage Tier
            </label>
            <div className="grid grid-cols-4 gap-2">
              {['ALL', 'LOW', 'MODERATE', 'HIGH'].map((tier) => (
                <button
                  key={tier}
                  onClick={() => setSelectedTier(tier)}
                  className={`py-2 text-xs font-semibold rounded-xl border transition ${
                    selectedTier === tier
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                      : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  {tier}
                </button>
              ))}
            </div>
          </div>

          {/* Filter 2: Min Marks Slider */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                Minimum Academic Marks
              </label>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                {minMarks}%
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={minMarks}
              onChange={(e) => setMinMarks(parseInt(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
            />
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
          <PlotlyChart data={scatter2DData} layout={scatter2DLayout} />
        </div>
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
          <PlotlyChart data={histData} layout={histLayout} />
        </div>
      </div>

      {/* 3D Scatter Plot Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
        <PlotlyChart data={scatter3DData} layout={scatter3DLayout} style={{ minHeight: '450px' }} />
      </div>
    </div>
  );
}

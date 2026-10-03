'use client';

import React, { useEffect, useState } from 'react';

export default function PlotlyChart({ data, layout, style, config }) {
  const [PlotComponent, setPlotComponent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    import('react-plotly.js')
      .then((module) => {
        setPlotComponent(() => module.default);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load react-plotly.js:', err);
        setIsLoading(false);
      });
  }, []);

  if (isLoading || !PlotComponent) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-slate-50 border border-slate-200 rounded-xl animate-pulse">
        <div className="flex items-center space-x-2 text-slate-400">
          <svg className="animate-spin h-5 w-5 text-indigo-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span className="text-sm font-medium text-slate-500">Loading interactive chart...</span>
        </div>
      </div>
    );
  }

  const defaultLayout = {
    autosize: true,
    margin: { t: 40, r: 30, l: 50, b: 50 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: '#F8FAFC',
    font: { family: 'Inter, sans-serif', color: '#334155' },
    hoverlabel: { bgcolor: '#0F172A', font: { color: '#FFFFFF' } },
    ...layout,
  };

  const defaultConfig = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    ...config,
  };

  return (
    <div className="w-full overflow-hidden">
      <PlotComponent
        data={data}
        layout={defaultLayout}
        config={defaultConfig}
        style={{ width: '100%', height: '100%', minHeight: '350px', ...style }}
        useResizeHandler={true}
      />
    </div>
  );
}

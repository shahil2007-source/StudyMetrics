'use client';

import React, { useState, useEffect } from 'react';
import Header from '../../components/Header';
import {
  Users,
  Search,
  Plus,
  Download,
  Upload,
  Trash2,
  Edit2,
  X,
  CheckCircle,
  AlertCircle,
  RefreshCw,
  FileSpreadsheet,
} from 'lucide-react';

export default function StudentData() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTier, setSelectedTier] = useState('ALL');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    Student_ID: '',
    Name: '',
    Social_Media_Usage_Hours: '',
    Study_Hours: '',
    Academic_Marks: '',
  });

  // Message / Alert State
  const [message, setMessage] = useState(null);

  const fetchStudents = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/students');
      if (res.ok) {
        const data = await res.json();
        const list = Array.isArray(data) ? data : (data?.data || []);
        setStudents(list);
      }
    } catch (err) {
      console.error('Failed to fetch students:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleOpenAddModal = () => {
    setIsEditing(false);
    setFormData({
      Student_ID: `STD${Math.floor(100 + Math.random() * 900)}`,
      Name: '',
      Social_Media_Usage_Hours: '3.0',
      Study_Hours: '4.0',
      Academic_Marks: '75',
    });
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (student) => {
    setIsEditing(true);
    setFormData({
      Student_ID: student.Student_ID,
      Name: student.Name || '',
      Social_Media_Usage_Hours: student.Social_Media_Usage_Hours,
      Study_Hours: student.Study_Hours,
      Academic_Marks: student.Academic_Marks,
    });
    setIsModalOpen(true);
  };

  const handleSubmitModal = async (e) => {
    e.preventDefault();
    const payload = {
      Student_ID: formData.Student_ID,
      Name: formData.Name || `Student ${formData.Student_ID}`,
      Social_Media_Usage_Hours: parseFloat(formData.Social_Media_Usage_Hours),
      Study_Hours: parseFloat(formData.Study_Hours),
      Academic_Marks: parseFloat(formData.Academic_Marks),
    };

    try {
      const method = isEditing ? 'PUT' : 'POST';
      const endpoint = isEditing ? `/api/students/${payload.Student_ID}` : '/api/students';
      const res = await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        setMessage({ type: 'success', text: `Student record ${isEditing ? 'updated' : 'added'} successfully!` });
        setIsModalOpen(false);
        fetchStudents();
      } else {
        const err = await res.json();
        setMessage({ type: 'error', text: err.detail || 'Failed to save student record.' });
      }
    } catch (err) {
      console.error(err);
      setMessage({ type: 'error', text: 'Error connecting to API server.' });
    }
  };

  const handleDelete = async (studentId) => {
    if (!confirm(`Are you sure you want to delete student ${studentId}?`)) return;

    try {
      const res = await fetch(`/api/students/${studentId}`, { method: 'DELETE' });
      if (res.ok) {
        setMessage({ type: 'success', text: `Student ${studentId} deleted.` });
        fetchStudents();
      } else {
        setMessage({ type: 'error', text: 'Failed to delete student.' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Error connecting to server.' });
    }
  };

  const handleUploadCsv = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const body = new FormData();
    body.append('file', file);

    try {
      const res = await fetch('/api/students/upload', {
        method: 'POST',
        body,
      });

      if (res.ok) {
        const data = await res.json();
        setMessage({ type: 'success', text: data.message || 'CSV file imported successfully!' });
        fetchStudents();
      } else {
        setMessage({ type: 'error', text: 'Failed to upload CSV file.' });
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Error uploading file.' });
    }
  };

  const handleExportCsv = () => {
    window.open('/api/students/export', '_blank');
  };

  // Filter students based on search and usage tier
  const studentList = Array.isArray(students) ? students : [];
  const filteredStudents = studentList.filter((s) => {
    const matchesSearch =
      (s.Name && s.Name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (s.Student_ID && s.Student_ID.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (s.student_id && s.student_id.toLowerCase().includes(searchTerm.toLowerCase()));

    const usage = parseFloat(s.Social_Media_Usage_Hours ?? s.social_media_hours ?? 0);
    let matchesTier = true;
    if (selectedTier === 'LOW') matchesTier = usage < 2.0;
    if (selectedTier === 'MODERATE') matchesTier = usage >= 2.0 && usage <= 5.0;
    if (selectedTier === 'HIGH') matchesTier = usage > 5.0;

    return matchesSearch && matchesTier;
  });

  return (
    <div>
      <Header
        title="Student Data Management"
        description="View, add, edit, search, and manage student dataset records."
        badge={`${students.length} Total Records`}
      />

      {/* Alert banner */}
      {message && (
        <div
          className={`mb-6 p-4 rounded-xl flex items-center justify-between border ${
            message.type === 'success'
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-red-50 text-red-800 border-red-200'
          }`}
        >
          <div className="flex items-center gap-2">
            {message.type === 'success' ? (
              <CheckCircle className="w-5 h-5 text-emerald-600" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-600" />
            )}
            <span className="text-sm font-medium">{message.text}</span>
          </div>
          <button onClick={() => setMessage(null)} className="text-slate-400 hover:text-slate-600">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Toolbar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        {/* Search & Tier Filters */}
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search by ID or Name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <select
            value={selectedTier}
            onChange={(e) => setSelectedTier(e.target.value)}
            className="w-full sm:w-48 px-3 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
          >
            <option value="ALL">All Usage Tiers</option>
            <option value="LOW">Low Usage (&lt; 2h)</option>
            <option value="MODERATE">Moderate Usage (2-5h)</option>
            <option value="HIGH">High Usage (&gt; 5h)</option>
          </select>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={handleOpenAddModal}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold flex items-center gap-2 shadow-sm transition"
          >
            <Plus className="w-4 h-4" /> Add Student
          </button>

          <label className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-xl text-sm font-semibold flex items-center gap-2 cursor-pointer shadow-sm transition">
            <Upload className="w-4 h-4 text-indigo-600" /> Upload CSV
            <input type="file" accept=".csv" onChange={handleUploadCsv} className="hidden" />
          </label>

          <button
            onClick={handleExportCsv}
            className="px-4 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 rounded-xl text-sm font-semibold flex items-center gap-2 shadow-sm transition"
          >
            <Download className="w-4 h-4 text-emerald-600" /> Export CSV
          </button>

          <button
            onClick={fetchStudents}
            className="p-2.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-xl transition"
            title="Refresh Data"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Table Card */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-500 flex flex-col items-center justify-center space-y-3">
            <RefreshCw className="w-6 h-6 animate-spin text-indigo-600" />
            <p className="text-sm font-medium">Loading student dataset...</p>
          </div>
        ) : filteredStudents.length === 0 ? (
          <div className="p-12 text-center text-slate-500 flex flex-col items-center justify-center space-y-2">
            <FileSpreadsheet className="w-10 h-10 text-slate-300" />
            <p className="font-semibold text-slate-700">No student records found</p>
            <p className="text-xs text-slate-400">Try adjusting your search criteria or filter options.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
                  <th className="py-3.5 px-4">Student ID</th>
                  <th className="py-3.5 px-4">Name</th>
                  <th className="py-3.5 px-4">Social Media (hrs/day)</th>
                  <th className="py-3.5 px-4">Study Hours (hrs/day)</th>
                  <th className="py-3.5 px-4">Academic Marks (%)</th>
                  <th className="py-3.5 px-4">Usage Tier</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredStudents.map((student) => {
                  const usage = parseFloat(student.Social_Media_Usage_Hours);
                  let tierBadge = (
                    <span className="bg-emerald-50 text-emerald-700 px-2.5 py-0.5 rounded-full text-xs font-semibold border border-emerald-200">
                      Low (&lt;2h)
                    </span>
                  );
                  if (usage >= 2.0 && usage <= 5.0) {
                    tierBadge = (
                      <span className="bg-amber-50 text-amber-700 px-2.5 py-0.5 rounded-full text-xs font-semibold border border-amber-200">
                        Moderate (2-5h)
                      </span>
                    );
                  } else if (usage > 5.0) {
                    tierBadge = (
                      <span className="bg-rose-50 text-rose-700 px-2.5 py-0.5 rounded-full text-xs font-semibold border border-rose-200">
                        High (&gt;5h)
                      </span>
                    );
                  }

                  return (
                    <tr key={student.Student_ID} className="hover:bg-slate-50/80 transition">
                      <td className="py-3 px-4 font-bold text-indigo-900">{student.Student_ID}</td>
                      <td className="py-3 px-4 font-medium">{student.Name || `Student ${student.Student_ID}`}</td>
                      <td className="py-3 px-4 font-semibold text-purple-700">{student.Social_Media_Usage_Hours}</td>
                      <td className="py-3 px-4 font-semibold text-blue-700">{student.Study_Hours}</td>
                      <td className="py-3 px-4 font-extrabold text-slate-900">{student.Academic_Marks}%</td>
                      <td className="py-3 px-4">{tierBadge}</td>
                      <td className="py-3 px-4 text-right space-x-2">
                        <button
                          onClick={() => handleOpenEditModal(student)}
                          className="p-1.5 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition"
                          title="Edit Student"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(student.Student_ID)}
                          className="p-1.5 text-slate-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                          title="Delete Student"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add / Edit Student Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md border border-slate-200 overflow-hidden">
            <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between">
              <h3 className="font-bold text-base flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-400" />
                {isEditing ? 'Edit Student Record' : 'Add New Student'}
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSubmitModal} className="p-6 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Student ID
                </label>
                <input
                  type="text"
                  required
                  disabled={isEditing}
                  value={formData.Student_ID}
                  onChange={(e) => setFormData({ ...formData, Student_ID: e.target.value })}
                  className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-slate-100 disabled:text-slate-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Alex Johnson"
                  value={formData.Name}
                  onChange={(e) => setFormData({ ...formData, Name: e.target.value })}
                  className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                    Social Media (hrs/day)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="24"
                    required
                    value={formData.Social_Media_Usage_Hours}
                    onChange={(e) => setFormData({ ...formData, Social_Media_Usage_Hours: e.target.value })}
                    className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                    Study Hours (hrs/day)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="24"
                    required
                    value={formData.Study_Hours}
                    onChange={(e) => setFormData({ ...formData, Study_Hours: e.target.value })}
                    className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1">
                  Academic Marks (%)
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="100"
                  required
                  value={formData.Academic_Marks}
                  onChange={(e) => setFormData({ ...formData, Academic_Marks: e.target.value })}
                  className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="pt-4 flex items-center justify-end space-x-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border border-slate-200 text-slate-600 rounded-xl text-sm font-semibold hover:bg-slate-50 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold shadow-sm transition"
                >
                  {isEditing ? 'Save Changes' : 'Create Student'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

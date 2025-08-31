import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWidget from './components/Chatwidget';
import './App.css';

interface FilterData {
  state_name?: string;
  district_name?: string;
  sector?: string;
  religion?: string;
  social_group?: string;
  household_size?: string;
  panel?: string;
  quarter?: string;
  visit?: string;
}

interface ApiResponse {
  success: boolean;
  count: number;
  filters_applied: FilterData;
  data: any[];
  error?: string;
}

function App() {
  const [filters, setFilters] = useState<FilterData>({});
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [count, setCount] = useState(0);

  // Sample data for dropdowns (you can replace these with actual API calls)
  const sectors = ['Rural', 'Urban'];
  const religions = ['Hindu', 'Muslim', 'Christian', 'Sikh', 'Buddhist', 'Jain', 'Other'];
  const socialGroups = ['SC', 'ST', 'OBC', 'General'];
  const householdSizes = ['1-2', '3-4', '5-6', '7+'];
  const panels = ['Panel 1', 'Panel 2', 'Panel 3'];
  const quarters = ['Q1', 'Q2', 'Q3', 'Q4'];
  const visits = ['Visit 1', 'Visit 2', 'Visit 3'];

  const handleFilterChange = (key: keyof FilterData, value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: value || undefined
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          params.append(key, value);
        }
      });

      const response = await axios.get<ApiResponse>(`http://localhost:8000/api/filter?${params.toString()}`);
      
      if (response.data.success) {
        setData(response.data.data);
        setCount(response.data.count);
      } else {
        setError(response.data.error || 'An error occurred');
        setData([]);
        setCount(0);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Failed to fetch data');
      setData([]);
      setCount(0);
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setFilters({});
    setData([]);
    setCount(0);
    setError('');
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Statathon Project - Data Filter</h1>
      </header>
      
      <main className="main-content">
        <div className="filters-section">
          <h2>Filters</h2>
          
          <div className="filters-grid">
            <div className="filter-group">
              <label htmlFor="state_name">State Name:</label>
              <input
                type="text"
                id="state_name"
                placeholder="e.g., Maharashtra, Andhra Pradesh"
                value={filters.state_name || ''}
                onChange={(e) => handleFilterChange('state_name', e.target.value)}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="district_name">District Name:</label>
              <input
                type="text"
                id="district_name"
                placeholder="e.g., Mumbai, Pune"
                value={filters.district_name || ''}
                onChange={(e) => handleFilterChange('district_name', e.target.value)}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="sector">Sector:</label>
              <select
                id="sector"
                value={filters.sector || ''}
                onChange={(e) => handleFilterChange('sector', e.target.value)}
              >
                <option value="">Select Sector</option>
                {sectors.map(sector => (
                  <option key={sector} value={sector}>{sector}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="religion">Religion:</label>
              <select
                id="religion"
                value={filters.religion || ''}
                onChange={(e) => handleFilterChange('religion', e.target.value)}
              >
                <option value="">Select Religion</option>
                {religions.map(religion => (
                  <option key={religion} value={religion}>{religion}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="social_group">Social Group:</label>
              <select
                id="social_group"
                value={filters.social_group || ''}
                onChange={(e) => handleFilterChange('social_group', e.target.value)}
              >
                <option value="">Select Social Group</option>
                {socialGroups.map(group => (
                  <option key={group} value={group}>{group}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="household_size">Household Size:</label>
              <select
                id="household_size"
                value={filters.household_size || ''}
                onChange={(e) => handleFilterChange('household_size', e.target.value)}
              >
                <option value="">Select Household Size</option>
                {householdSizes.map(size => (
                  <option key={size} value={size}>{size}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="panel">Panel:</label>
              <select
                id="panel"
                value={filters.panel || ''}
                onChange={(e) => handleFilterChange('panel', e.target.value)}
              >
                <option value="">Select Panel</option>
                {panels.map(panel => (
                  <option key={panel} value={panel}>{panel}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="quarter">Quarter:</label>
              <select
                id="quarter"
                value={filters.quarter || ''}
                onChange={(e) => handleFilterChange('quarter', e.target.value)}
              >
                <option value="">Select Quarter</option>
                {quarters.map(quarter => (
                  <option key={quarter} value={quarter}>{quarter}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="visit">Visit:</label>
              <select
                id="visit"
                value={filters.visit || ''}
                onChange={(e) => handleFilterChange('visit', e.target.value)}
              >
                <option value="">Select Visit</option>
                {visits.map(visit => (
                  <option key={visit} value={visit}>{visit}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="filter-actions">
            <button 
              className="btn btn-primary" 
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Loading...' : 'Apply Filters'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={clearFilters}
              disabled={loading}
            >
              Clear Filters
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}

        {count > 0 && (
          <div className="results-section">
            <h2>Results ({count} records)</h2>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    {data.length > 0 && Object.keys(data[0]).map(key => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, index) => (
                    <tr key={index}>
                      {Object.values(row).map((value: any, cellIndex) => (
                        <td key={cellIndex}>{String(value)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
         <ChatWidget />
      </main>
    </div>
  );
}

export default App;

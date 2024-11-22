// src/VolumeChart.jsx
import React from 'react';
import { Bar } from 'react-chartjs-2';

const VolumeChart = () => {
  const data = {
    labels: ['2024-10-10', '2024-10-11', '2024-10-12', '2024-10-13'],
    datasets: [
      {
        label: 'Volume',
        data: [500, 1000, 1500, 700],
        backgroundColor: 'orange',
      },
    ],
  };

  return (
    <div className="chart-container">
      <h2>Trading Volume</h2>
      <Bar data={data} />
    </div>
  );
};

export default VolumeChart;

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function ArticleChart({ sentimentScore }) {
  // Example data based on the article's sentiment score over time.
  // You may want to adjust this based on your actual data structure.
  const data = [
    { name: 'Sentiment Score', value: sentimentScore }
  ];

  return (
    <div style={{ width: '100%', height: 300, marginTop: '20px' }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#0073e6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default ArticleChart;

import React, { useState } from 'react';
import { 
  BsFillArchiveFill, 
  BsFillGrid3X3GapFill, 
  BsPeopleFill, 
  BsFillBellFill 
} from 'react-icons/bs';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell 
} from 'recharts';
import './Home.css';

function Home() {
  const [selectedCard, setSelectedCard] = useState(null);

  const data = [
    { name: 'Page A', uv: 4000, pv: 2400, amt: 2400 },
    { name: 'Page B', uv: 3000, pv: 1398, amt: 2210 },
    { name: 'Page C', uv: 2000, pv: 9800, amt: 2290 },
    { name: 'Page D', uv: 2780, pv: 3908, amt: 2000 },
    { name: 'Page E', uv: 1890, pv: 4800, amt: 2181 },
    { name: 'Page F', uv: 2390, pv: 3800, amt: 2500 },
    { name: 'Page G', uv: 3490, pv: 4300, amt: 2100 },
  ];

  const pieData = [
    { name: 'Group A', value: 400 },
    { name: 'Group B', value: 300 },
    { name: 'Group C', value: 300 },
    { name: 'Group D', value: 200 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  const newsData = [
    { title: 'Stock Market Hits Record Highs', date: '2024-10-29', description: 'The stock market reached new highs today as investors rallied around tech stocks.' },
    { title: 'Company X Announces New Product', date: '2024-10-28', description: 'Company X has unveiled its latest product, which promises to revolutionize the industry.' },
    { title: 'Economic Growth Exceeds Expectations', date: '2024-10-27', description: 'The latest GDP report shows growth exceeding analyst predictions by a large margin.' },
  ];

  const handleCardClick = (card) => {
    setSelectedCard(card === selectedCard ? null : card); // Toggle card selection
  };

  const renderChartData = () => {
    switch (selectedCard) {
      case 'STOCKS':
        return <p>Stock-related data would be shown here...</p>;
      case 'COMPANIES':
        return <p>Company-specific data and trends here...</p>;
      case 'CUSTOMERS':
        return <p>Customer analytics and trends here...</p>;
      case 'ALERTS':
        return <p>Alert trends and statistics shown here...</p>;
      default:
        return <p>Select an icon to view more data.</p>;
    }
  };

  return (
    <main className='main-container'>
      <div className='main-title'>
        <h3>DASHBOARD</h3>
      </div>

      <div className='icon-buttons'>
        <button className='icon-button stocks' onClick={() => handleCardClick('STOCKS')} title="STOCKS">
          <BsFillArchiveFill className='icon' />
          <span>STOCKS</span>
        </button>
        <button className='icon-button companies' onClick={() => handleCardClick('COMPANIES')} title="COMPANIES">
          <BsFillGrid3X3GapFill className='icon' />
          <span>COMPANIES</span>
        </button>
        <button className='icon-button customers' onClick={() => handleCardClick('CUSTOMERS')} title="CUSTOMERS">
          <BsPeopleFill className='icon' />
          <span>CUSTOMERS</span>
        </button>
        <button className='icon-button alerts' onClick={() => handleCardClick('ALERTS')} title="ALERTS">
          <BsFillBellFill className='icon' />
          <span>ALERTS</span>
        </button>
      </div>

      {/* Modal for showing expanded data */}
      {selectedCard && (
        <div className="modal-overlay" onClick={() => setSelectedCard(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h4>Data for {selectedCard}</h4>
            {renderChartData()}
            <div className='charts'>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="pv" fill="#8884d8" />
                  <Bar dataKey="uv" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>

              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="pv" stroke="#8884d8" activeDot={{ r: 8 }} />
                  <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {/* News Section */}
      <div className="news-section">
        <h3>Latest News</h3>
        <div className="news-container">
          {newsData.map((news, index) => (
            <div key={index} className="news-item">
              <h4>{news.title}</h4>
              <p><small>{news.date}</small></p>
              <p>{news.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Pie Chart Section */}
      <div className="pie-chart-section">
        <h3>Charts</h3>
        <div className="pie-chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} fill="#8884d8">
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </main>
  );
}

export default Home;

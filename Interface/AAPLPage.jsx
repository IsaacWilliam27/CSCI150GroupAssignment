import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import './AAPLPageStyles.css';

function AAPLPage() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedArticle, setExpandedArticle] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5001/api/aapl/articles');
        setArticles(response.data);
      } catch (error) {
        setError("Error fetching articles");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const toggleArticle = (index) => {
    setExpandedArticle(expandedArticle?.index === index ? null : { index, showChart: false });
  };

  const toggleChart = (index) => {
    setExpandedArticle((prev) =>
      prev?.index === index ? { ...prev, showChart: !prev.showChart } : prev
    );
  };

  if (loading) return <p>Loading articles...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="aapl-page">
      <h2>AAPL Articles</h2>
      <div className="articles">
        {articles.length > 0 ? (
          articles.map((article, index) => (
            <div
              key={index}
              className={`article ${expandedArticle?.index === index ? 'expanded' : ''}`}
              onClick={() => toggleArticle(index)}
            >
              <h3 className="article-title">{article.Title}</h3>
              {expandedArticle?.index === index && (
                <div className="article-content">
                  <p>{article.Content}</p>
                  <p><strong>Sentiment Score:</strong> {article.Sentiment_Score}</p>
                  <p><strong>Date:</strong> {new Date(article.Date).toLocaleDateString()}</p>
                  <button
                    className="show-graph-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleChart(index);
                    }}
                  >
                    {expandedArticle.showChart ? 'Hide Graph' : 'Show Graph'}
                  </button>
                  {expandedArticle.showChart && (
                    <div className="chart-container">
                      <h4 className="chart-title">Sentiment Score</h4>
                      <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={[{ title: article.Title, sentiment: article.Sentiment_Score }]}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#cccccc" />
                          <XAxis dataKey="title" hide />
                          <YAxis />
                          <Tooltip cursor={{ fill: 'rgba(200, 200, 200, 0.2)' }} />
                          <Bar dataKey="sentiment" fill="#0073e6" radius={[10, 10, 0, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        ) : (
          <p>No articles available</p>
        )}
      </div>
    </div>
  );
}

export default AAPLPage;

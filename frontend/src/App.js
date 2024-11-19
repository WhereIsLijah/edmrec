import React, { useState } from 'react';
import './App.css'; // Import the CSS file

const EDMRecFrontend = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [datasets, setDatasets] = useState([
    // Example datasets; replace with actual API data.
    ...Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      name: `Dataset ${i + 1}`,
      title: `Title for Dataset ${i + 1}`,
      url: `https://example.com/dataset${i + 1}`,
    })),
  ]);
  const [recentSearches, setRecentSearches] = useState([]);
  const popularSearches = ['Sales Data', 'Customer Reviews', 'Product Metadata'];
  const [currentPage, setCurrentPage] = useState(1);

  const resultsPerPage = 10;
  const totalPages = Math.ceil(datasets.length / resultsPerPage);

  const handleSearch = (query) => {
    if (query) {
      setSearchQuery(query);
      setRecentSearches((prevSearches) => [...new Set([query, ...prevSearches])]);
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const paginatedDatasets = datasets.slice(
    (currentPage - 1) * resultsPerPage,
    currentPage * resultsPerPage
  );

  return (
    <div className="container">
      <header className="header">
        <h1>E-commerce Dataset Mining Recommendation System</h1>
      </header>

      <main className="main">
        <div className="search-bar-container">
          <input
            type="text"
            placeholder="Searching for an e-commerce dataset?"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-bar"
          />
          <button
            onClick={() => handleSearch(searchQuery)}
            className="search-button"
          >
            Search
          </button>
        </div>

        <div className="content">
          <section className="list-container">
            {paginatedDatasets.map((dataset) => (
              <div
                key={dataset.id}
                className="card"
                onClick={() => window.open(dataset.url, '_blank')}
              >
                <h3>{dataset.name}</h3>
                <p>{dataset.title}</p>
              </div>
            ))}

            {totalPages > 1 && (
              <div className="pagination">
                {Array.from({ length: totalPages }, (_, i) => (
                  <button
                    key={i + 1}
                    onClick={() => handlePageChange(i + 1)}
                    className="page-button"
                    style={{
                      backgroundColor: currentPage === i + 1 ? '#009688' : '#f1f1f1',
                      color: currentPage === i + 1 ? '#fff' : '#000',
                    }}
                  >
                    {i + 1}
                  </button>
                ))}
              </div>
            )}
          </section>

          <aside className="aside">
            <h3>Recent Searches</h3>
            <ul className="recent-search-list">
              {recentSearches.map((search, index) => (
                <li
                  key={index}
                  className="recent-search-item"
                  onClick={() => handleSearch(search)}
                >
                  {search}
                </li>
              ))}
            </ul>

            <h3>Popular Searches</h3>
            <ul className="popular-search-list">
              {popularSearches.map((search, index) => (
                <li key={index} className="popular-search-item">
                  {search}
                </li>
              ))}
            </ul>
          </aside>
        </div>
      </main>

      <footer className="footer">
  <p>
    &copy; 2024 EDMRec 
    <a href="mailto:ayomideoduba@gmail.com" style={{ color: '#fff', textDecoration: 'none' }}>
      | ayomideoduba@gmail.com
    </a> & 
    <a href="mailto:cezeife@uwindsor.ca" style={{ color: '#fff', textDecoration: 'none' }}>
      cezeife@uwindsor.ca |
    </a>
  </p>
</footer>
    </div>
  );
};

export default EDMRecFrontend;

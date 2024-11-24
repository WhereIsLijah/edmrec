import React, { useState, useEffect } from 'react';
import './App.css';

const EDMRecFrontend = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const popularSearches = ['Sales Data', 'Customer Reviews', 'Product Metadata', 'Find datasets about e-commerce sales'];
  const [currentPage, setCurrentPage] = useState(1);
  const [sortOrder, setSortOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCTA, setShowCTA] = useState(false);

  const resultsPerPage = 10;

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/datasets/')
      .then(response => response.json())
      .then(data => setDatasets(data))
      .catch(error => console.error('Error fetching datasets:', error));
  }, []);

  const handleSearch = (query) => {
    if (query) {
      setSearchQuery(query);
      setLoading(true);
      fetch('http://127.0.0.1:8000/api/query/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })
        .then(response => response.json())
        .then(data => {
          setDatasets(data);
          setRecentSearches((prevSearches) => [...new Set([query, ...prevSearches])]);
          setLoading(false);
          setShowCTA(true);
        })
        .catch(error => {
          console.error('Error processing query:', error);
          setLoading(false);
        });
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleSortOrderChange = (field, order) => {
    if (sortOrder && sortOrder.field === field && sortOrder.order === order) {
      setSortOrder(null); // Reset to default
    } else {
      setSortOrder({ field, order });
    }
  };

  const convertSizeToMB = (size) => {
    if (size.toLowerCase().endsWith('kb')) {
      return parseFloat(size) / 1024;
    }
    return parseFloat(size);
  };

  const sortedDatasets = sortOrder ? datasets.sort((a, b) => {
    if (sortOrder.field === 'name') {
      if (sortOrder.order === 'asc') {
        return a.title.localeCompare(b.title);
      } else {
        return b.title.localeCompare(a.title);
      }
    } else if (sortOrder.field === 'size') {
      const sizeA = convertSizeToMB(a.size);
      const sizeB = convertSizeToMB(b.size);
      if (sortOrder.order === 'asc') {
        return sizeA - sizeB;
      } else {
        return sizeB - sizeA;
      }
    }
    return 0;
  }) : datasets;

  const paginatedDatasets = sortedDatasets.slice(
    (currentPage - 1) * resultsPerPage,
    currentPage * resultsPerPage
  );

  const totalPagesDynamic = Math.ceil(sortedDatasets.length / resultsPerPage);

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
          <aside className="aside">
            <h3>Sort By</h3>
            <div className="sort-options">
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'name' && sortOrder?.order === 'asc'}
                  onChange={() => handleSortOrderChange('name', 'asc')}
                />
                Name Ascending
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'name' && sortOrder?.order === 'desc'}
                  onChange={() => handleSortOrderChange('name', 'desc')}
                />
                Name Descending
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'size' && sortOrder?.order === 'asc'}
                  onChange={() => handleSortOrderChange('size', 'asc')}
                />
                Size Ascending
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'size' && sortOrder?.order === 'desc'}
                  onChange={() => handleSortOrderChange('size', 'desc')}
                />
                Size Descending
              </label>
            </div>

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
                <li
                  key={index}
                  className="popular-search-item"
                  onClick={() => handleSearch(search)}
                >
                  {search}
                </li>
              ))}
            </ul>
          </aside>

          <section className="list-container">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <>
                {showCTA && <div className="cta">Click on a card to view the dataset</div>}
                {paginatedDatasets.map((dataset) => (
                  <div
                    key={dataset.id}
                    className="card"
                    onClick={() => window.open(dataset.url, '_blank')}
                  >
                    <h3>{dataset.title}</h3>
                    <p>{dataset.description}</p>
                    <p>Size: {dataset.size}</p>
                    {/* <p>Similarity Score: {dataset.similarity_score?.toFixed(2)}</p> */}
                  </div>
                ))}
              </>
            )}

            {totalPagesDynamic > 1 && (
              <div className="pagination">
                {Array.from({ length: totalPagesDynamic }, (_, i) => (
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
        </div>
      </main>

      <footer className="footer">
        <p>
          &copy; 2024 EDMRec 
          <a href="mailto:ayomideoduba@gmail.com" style={{ color: '#fff', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer">
            | ayomideoduba@gmail.com
          </a> & 
          <a href="mailto:cezeife@uwindsor.ca" style={{ color: '#fff', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer">
            cezeife@uwindsor.ca |
          </a>
        </p>
      </footer>
    </div>
  );
};

export default EDMRecFrontend;
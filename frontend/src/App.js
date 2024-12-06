import React, { useState, useEffect } from 'react';
import './App.css';

const EDMRecFrontend = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [recentSearches, setRecentSearches] = useState([]);
  const popularSearches = ['Sales Data', 'The impact of seasonal sales on consumer review for electronics', 'Product Metadata', 'Find datasets about e-commerce sales'];
  const [currentPage, setCurrentPage] = useState(1);
  const [sortOrder, setSortOrder] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showCTA, setShowCTA] = useState(false);
  const [ratingFilter, setRatingFilter] = useState(null);

  const resultsPerPage = 10;
  const maxPagesToShow = 5;

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
          const top20Results = data.slice(0, 20);
          setDatasets(top20Results);
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
      setSortOrder(null);
    } else {
      setSortOrder({ field, order });
    }
  };

  const handleRatingFilterChange = (rating) => {
    setRatingFilter(rating);
  };

  const convertSizeToMB = (size) => {
    if (size.toLowerCase().endsWith('kb')) {
      return parseFloat(size) / 1024;
    }
    return parseFloat(size);
  };

  const getStarRating = (similarityScore) => {
    if (similarityScore >= 0.65) return <span className="stars five-stars">⭐⭐⭐⭐⭐</span>;
    if (similarityScore >= 0.5) return <span className="stars four-stars">⭐⭐⭐⭐</span>;
    if (similarityScore >= 0.35) return <span className="stars three-stars">⭐⭐⭐</span>;
    if (similarityScore >= 0.2) return <span className="stars two-stars">⭐⭐</span>;
    return <span className="stars one-star">⭐</span>;
  };

  const filteredDatasets = ratingFilter
    ? datasets.filter(dataset => {
        const rating = getStarRating(dataset.similarity_score);
        return rating.props.children === ratingFilter;
      })
    : datasets;

  const sortedDatasets = sortOrder
    ? filteredDatasets.sort((a, b) => {
        if (sortOrder.field === 'size') {
          const sizeA = convertSizeToMB(a.size);
          const sizeB = convertSizeToMB(b.size);
          if (sortOrder.order === 'asc') {
            return sizeA - sizeB;
          } else {
            return sizeB - sizeA;
          }
        }
        return 0;
      })
    : filteredDatasets;

  const paginatedDatasets = sortedDatasets.slice(
    (currentPage - 1) * resultsPerPage,
    currentPage * resultsPerPage
  );

  const totalPagesDynamic = Math.ceil(sortedDatasets.length / resultsPerPage);

  const getPaginationGroup = () => {
    let start = Math.floor((currentPage - 1) / maxPagesToShow) * maxPagesToShow;
    return new Array(Math.min(maxPagesToShow, totalPagesDynamic - start)).fill().map((_, idx) => start + idx + 1);
  };

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

        {loading && (
          <div className="loading-screen">
            <div className="loader"></div>
            <p className="loading-message">Please wait while we recommend datasets for you...</p>
          </div>
        )}

        <div className="content" style={{ display: loading ? 'none' : 'grid' }}>
          <aside className="aside">
            <h3>Sort By Size</h3>
            <div className="sort-options">
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'size' && sortOrder?.order === 'asc'}
                  onChange={() => handleSortOrderChange('size', 'asc')}
                />
                Ascending
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={sortOrder?.field === 'size' && sortOrder?.order === 'desc'}
                  onChange={() => handleSortOrderChange('size', 'desc')}
                />
                Descending
              </label>
            </div>

            <h3>Filter by Similarity Score</h3>
            <div className="rating-filter">
              <label>
                <input
                  type="radio"
                  name="rating"
                  value="⭐⭐⭐⭐⭐"
                  onChange={() => handleRatingFilterChange('⭐⭐⭐⭐⭐')}
                />
                ⭐⭐⭐⭐⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="rating"
                  value="⭐⭐⭐⭐"
                  onChange={() => handleRatingFilterChange('⭐⭐⭐⭐')}
                />
                ⭐⭐⭐⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="rating"
                  value="⭐⭐⭐"
                  onChange={() => handleRatingFilterChange('⭐⭐⭐')}
                />
                ⭐⭐⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="rating"
                  value="⭐⭐"
                  onChange={() => handleRatingFilterChange('⭐⭐')}
                />
                ⭐⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="rating"
                  value="⭐"
                  onChange={() => handleRatingFilterChange('⭐')}
                />
                ⭐
              </label>
              <label>
                <input
                  type="radio"
                  name="rating"
                  value=""
                  onChange={() => handleRatingFilterChange(null)}
                />
                All
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
                <p>Format: {dataset.format}</p>
                {searchQuery && (
                  <div className="rating">
                    {getStarRating(dataset.similarity_score)}
                  </div>
                )}
              </div>
            ))}

            {totalPagesDynamic > 1 && !loading && (
              <div className="pagination">
                <button
                  onClick={() => handlePageChange(currentPage - 1)}
                  className="page-button"
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                {getPaginationGroup().map((item, index) => (
                  <button
                    key={index}
                    onClick={() => handlePageChange(item)}
                    className={`page-button ${currentPage === item ? 'active' : ''}`}
                  >
                    {item}
                  </button>
                ))}
                <button
                  onClick={() => handlePageChange(currentPage + 1)}
                  className="page-button"
                  disabled={currentPage === totalPagesDynamic}
                >
                  Next
                </button>
              </div>
            )}
          </section>
        </div>
      </main>

      <footer className="footer">
        <p>
          &copy; 2024 EDMRec | 
          <a href="mailto:ayomideoduba@gmail.com" style={{ color: '#fff', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer">
            ayomideoduba@gmail.com
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

function ResultsGrid({ results }) {
  if (!results || results.length === 0) return null

  return (
    <section className="results" id="results-section">
      <div className="results__header">
        <h2 className="results__title">Similar Sarees Found</h2>
        <span className="results__count">{results.length} matches</span>
      </div>

      <div className="results__grid">
        {results.map((item, index) => (
          <div
            key={item.filename}
            className={`result-card ${index === 0 ? 'result-card--best' : ''}`}
            id={`result-card-${index}`}
          >
            <div className="result-card__image-wrapper">
              <img
                src={item.image_url}
                alt={item.filename}
                className="result-card__image"
                loading="lazy"
              />
            </div>

            <div className="result-card__info">
              <h3 className="result-card__name" title={item.filename}>
                {formatName(item.filename)}
              </h3>

              <div className="result-card__score-bar">
                <div
                  className="result-card__score-fill"
                  style={{ width: `${item.similarity_score}%` }}
                />
              </div>

              <div className="result-card__score-text">
                <span className="result-card__rank">#{index + 1}</span>
                <span className="result-card__score-value">
                  {item.similarity_score}% match
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

/** Format filename into a readable name */
function formatName(filename) {
  return filename
    .replace(/\.[^/.]+$/, '')     // remove extension
    .replace(/[_-]/g, ' ')        // replace _ and - with spaces
    .replace(/\b\w/g, c => c.toUpperCase()) // capitalize words
}

export default ResultsGrid

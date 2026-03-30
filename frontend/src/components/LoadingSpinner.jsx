function LoadingSpinner() {
  return (
    <div className="loading" id="loading-spinner">
      <div className="loading__spinner" />
      <p className="loading__text">Analyzing your saree...</p>
      <p className="loading__subtext">Comparing visual features with our collection</p>
    </div>
  )
}

export default LoadingSpinner

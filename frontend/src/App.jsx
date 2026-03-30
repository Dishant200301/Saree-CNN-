import { useState, useRef, useCallback } from 'react'
import axios from 'axios'
import ImageUpload from './components/ImageUpload'
import ResultsGrid from './components/ResultsGrid'
import LoadingSpinner from './components/LoadingSpinner'

const API_URL = '/search'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const resultsRef = useRef(null)

  const handleFileSelect = useCallback((file) => {
    setSelectedFile(file)
    setPreviewUrl(URL.createObjectURL(file))
    setResults(null)
    setError(null)
  }, [])

  const handleClear = useCallback(() => {
    setSelectedFile(null)
    if (previewUrl) URL.revokeObjectURL(previewUrl)
    setPreviewUrl(null)
    setResults(null)
    setError(null)
  }, [previewUrl])

  const handleSearch = useCallback(async () => {
    if (!selectedFile) return

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await axios.post(API_URL, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000,
      })

      setResults(response.data.results)

      // Scroll to results after a short delay
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 200)
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'Something went wrong. Please try again.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }, [selectedFile])

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <span className="header__icon">🥻</span>
        <h1 className="header__title">Saree Similarity Search</h1>
        <p className="header__subtitle">
          Upload a saree image and discover visually similar sarees using AI-powered analysis
        </p>
      </header>

      {/* Upload Section */}
      <section className="upload-section" id="upload">
        <ImageUpload
          onFileSelect={handleFileSelect}
          previewUrl={previewUrl}
          fileName={selectedFile?.name}
          onClear={handleClear}
        />

        {/* Actions */}
        {selectedFile && (
          <div className="preview__actions" style={{ marginTop: '24px', justifyContent: 'center', display: 'flex', gap: '12px' }}>
            <button
              className="btn btn--primary"
              onClick={handleSearch}
              disabled={loading}
              id="search-btn"
            >
              <span className="btn__icon">🔍</span>
              {loading ? 'Searching...' : 'Find Similar Sarees'}
            </button>
            <button
              className="btn btn--secondary"
              onClick={handleClear}
              disabled={loading}
              id="clear-btn"
            >
              <span className="btn__icon">✕</span>
              Clear
            </button>
          </div>
        )}
      </section>

      {/* Error */}
      {error && (
        <div className="error" id="error-message">
          <span className="error__icon">⚠️</span>
          <span className="error__text">{error}</span>
        </div>
      )}

      {/* Loading */}
      {loading && <LoadingSpinner />}

      {/* Results */}
      <div ref={resultsRef}>
        {results && results.length > 0 && (
          <ResultsGrid results={results} />
        )}
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Powered by MobileNet AI · Built with React & FastAPI</p>
      </footer>
    </div>
  )
}

export default App

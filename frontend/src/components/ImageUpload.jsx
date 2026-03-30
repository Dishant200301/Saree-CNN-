import { useRef, useState, useCallback } from 'react'

function ImageUpload({ onFileSelect, previewUrl, fileName, onClear }) {
  const inputRef = useRef(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (file.type.startsWith('image/')) {
        onFileSelect(file)
      }
    }
  }, [onFileSelect])

  const handleChange = useCallback((e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0])
    }
  }, [onFileSelect])

  const handleClick = useCallback(() => {
    inputRef.current?.click()
  }, [])

  // Show preview if image is selected
  if (previewUrl) {
    return (
      <div className="preview">
        <div className="preview__image-wrapper">
          <img
            src={previewUrl}
            alt="Selected saree"
            className="preview__image"
            id="preview-image"
          />
        </div>
        <span className="preview__filename">{fileName}</span>
      </div>
    )
  }

  // Show upload zone
  return (
    <div
      className={`upload-zone ${dragActive ? 'upload-zone--active' : ''}`}
      onClick={handleClick}
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
      id="upload-zone"
    >
      <div className="upload-zone__content">
        <span className="upload-zone__icon">
          {dragActive ? '📥' : '📤'}
        </span>
        <h3 className="upload-zone__title">
          {dragActive ? 'Drop your image here' : 'Upload a Saree Image'}
        </h3>
        <p className="upload-zone__hint">
          Drag & drop or click to browse · JPG, PNG, WebP
        </p>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/bmp"
        onChange={handleChange}
        className="upload-zone__input"
        id="file-input"
      />
    </div>
  )
}

export default ImageUpload

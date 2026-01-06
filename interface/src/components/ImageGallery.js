import React from 'react';

const ImageGallery = ({ images, filter, setFilter }) => {
    return (
        <div className="gallery-section">
            <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>Imported Gallery ({images.length})</h3>
                <select
                    className="select-input"
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                >
                    <option value="">All Sources</option>
                    <option value="google_drive">Google Drive</option>
                    <option value="dropbox">Dropbox</option>
                </select>
            </div>

            <div className="grid-container">
                {images.map(img => (
                    <div key={img.id} className="image-card">
                        <img src={img.storage_path} alt={img.name} className="image-preview" />
                        <div className="image-details">
                            <p className="image-name" title={img.name}>{img.name}</p>
                            <div className="image-meta">
                                <span>{(img.size / 1024).toFixed(2)} KB</span>
                            </div>
                        </div>
                    </div>
                ))}
                {images.length === 0 && (
                    <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
                        No images found. Start an import to see files here.
                    </div>
                )}
            </div>
        </div>
    );
};

export default ImageGallery;

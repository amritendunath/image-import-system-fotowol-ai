import React from 'react';

const ImageImporter = ({ folderUrl, setFolderUrl, handleImport, loading }) => {
    return (
        <div className="card">
            <h3 style={{ marginBottom: '16px' }}>Import Images</h3>
            <div className="input-group">
                <input
                    type="text"
                    className="form-input"
                    placeholder="Enter folder URL from external source"
                    value={folderUrl}
                    onChange={(e) => setFolderUrl(e.target.value)}
                />
            </div>
            <div className="input-group">
                <button
                    className="btn btn-primary"
                    onClick={() => handleImport('google_drive')}
                    disabled={loading}
                >
                    {loading ? 'Processing...' : 'Import from Google Drive'}
                </button>
                <button
                    className="btn btn-secondary"
                    onClick={() => handleImport('dropbox')}
                    disabled={loading}
                >
                    Import from Dropbox
                </button>
            </div>
        </div>
    );
};

export default ImageImporter;

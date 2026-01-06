import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Layout from './components/Layout';
import ImageImporter from './components/ImageImporter';
import ImageGallery from './components/ImageGallery';
import './styles/main.css';

const API_URL = process.env.REACT_APP_API_URL

function App() {
  const [folderUrl, setFolderUrl] = useState('');
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('');

  const fetchImages = async () => {
    try {
      const url = filter ? `${API_URL}/images?source=${filter}` : `${API_URL}/images`;
      const response = await axios.get(url);
      setImages(response.data.images);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  useEffect(() => {
    fetchImages();
  }, [filter]);

  const handleImport = async (source) => {
    if (!folderUrl && source !== 'dropbox') { // Dropbox might not need url if using oauth picker, but here we assume url for GD
      // keeping logic simple as per original
    }

    setLoading(true);
    try {
      const endpoint = source === 'dropbox' ? '/import/dropbox' : '/import/google-drive';
      await axios.post(`${API_URL}${endpoint}`, { folder_url: folderUrl });
      alert('Import started! Refresh in a few moments.');
      setFolderUrl('');
      // Optionally fetch images again after a delay or let user refresh
      setTimeout(fetchImages, 2000);
    } catch (error) {
      alert('Import failed: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <Layout>
      <ImageImporter
        folderUrl={folderUrl}
        setFolderUrl={setFolderUrl}
        handleImport={handleImport}
        loading={loading}
      />
      <ImageGallery
        images={images}
        filter={filter}
        setFilter={setFilter}
      />
    </Layout>
  );
}

export default App;
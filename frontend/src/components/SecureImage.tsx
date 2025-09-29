import React, { useState, useEffect } from 'react';

interface SecureImageProps {
  imageName: string;
  altText: string;
}

const SecureImage: React.FC<SecureImageProps> = ({ imageName, altText }) => {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setImageUrl(null);
    setError(null);

    if (!imageName) return;

    const fetchImageUrl = async () => {
      // --- LOG 1: Log the image we are trying to fetch ---
      console.log(`[SecureImage] 1. Fetching URL for: ${imageName}`);
      
      try {
        const response = await fetch(`http://localhost:8000/api/image-url/${imageName}`);

        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        
        // --- LOG 2: Log the raw data received from the API ---
        console.log(`[SecureImage] 2. Received data for ${imageName}:`, data);

        if (data && data.url) {
          // --- LOG 3: Log the URL we are about to set ---
          console.log(`[SecureImage] 3. Setting image URL for ${imageName}.`);
          setImageUrl(data.url);
        } else {
          throw new Error('The "url" property was not found in the API response.');
        }

      } catch (err: any) {
        // --- LOG 4: Log any errors that occur ---
        console.error(`[SecureImage] 4. ERROR fetching URL for ${imageName}:`, err);
        setError(err.message);
      }
    };

    fetchImageUrl();
  }, [imageName]);

  if (error) {
    // Display a visual indicator that something went wrong
    return <div className="recipe-image-placeholder" title={`Error: ${error}`} style={{ backgroundColor: 'red' }} />;
  }
  
  if (!imageUrl) {
    // This is the loading state
    return <div className="recipe-image-placeholder" />;
  }

  // If everything is successful, render the image
  return (
    <img src={imageUrl} alt={altText} className="recipe-image" />
  );
};

export default SecureImage;
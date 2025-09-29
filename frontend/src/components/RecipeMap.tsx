import React, { useRef, useLayoutEffect } from 'react';
import './RecipeMap.css';
import SecureImage from './SecureImage';

interface Recipe {
  title: string;
  image: string;
  x: number;
  y: number;
}
interface Coords {
  x: number;
  y: number;
}
interface RecipeMapProps {
  recipes: Recipe[];
  queryCoords: Coords | null;
}

const MAP_SCALE = 3000;
const MAP_CENTER = 5000;

export default function RecipeMap({ recipes, queryCoords }: RecipeMapProps) {
  const viewportRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (queryCoords && viewportRef.current) {
      const viewport = viewportRef.current;

      const queryPointX = MAP_CENTER + (queryCoords.x * MAP_SCALE);
      const queryPointY = MAP_CENTER + (queryCoords.y * MAP_SCALE);

      const scrollToX = queryPointX - (viewport.offsetWidth / 2);
      const scrollToY = queryPointY - (viewport.offsetHeight / 2);
      
      viewport.scrollTo({
        left: scrollToX,
        top: scrollToY,
        behavior: 'smooth'
      });
    }
  }, [queryCoords]);

  return (
    <div className="map-viewport" ref={viewportRef}>
      <div className="map-container">
        {recipes.map((recipe) => (
          <div
            key={recipe.title}
            className="recipe-point"
            style={{
              left: `${MAP_CENTER + (recipe.x * MAP_SCALE)}px`,
              top: `${MAP_CENTER + (recipe.y * MAP_SCALE)}px`,
            }}
            title={recipe.title}
          >

            <SecureImage imageName={recipe.image} altText={recipe.title} />
          </div>
        ))}
        
        {queryCoords && (
          <div
            className="query-point"
            style={{
              left: `${MAP_CENTER + (queryCoords.x * MAP_SCALE)}px`,
              top: `${MAP_CENTER + (queryCoords.y * MAP_SCALE)}px`,
            }}
            title="Your Search"
          ></div>
        )}
      </div>
    </div>
  );
}
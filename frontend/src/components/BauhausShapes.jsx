import React from 'react';

/**
 * Bauhaus Circle Component
 * Represents geometric purity and balance
 */
export const BauhausCircle = ({
  size = 'md',
  color = 'blue',
  className = ''
}) => {
  const sizeMap = {
    sm: 'w-12 h-12',
    md: 'w-24 h-24',
    lg: 'w-48 h-48',
  };

  const colorMap = {
    red: 'bg-[#e63946]',
    yellow: 'bg-[#ffd60a]',
    blue: 'bg-[#0077b6]',
    black: 'bg-[#1a1a1a]',
    white: 'bg-[#f8f9fa]',
  };

  return (
    <div
      className={`rounded-full ${sizeMap[size]} ${colorMap[color]} ${className}`}
      aria-hidden="true"
    />
  );
};

/**
 * Bauhaus Rectangle Component
 * Emphasizes functional structure
 */
export const BauhausRectangle = ({
  width = 'full',
  height = 'auto',
  color = 'white',
  className = ''
}) => {
  const widthMap = {
    full: 'w-full',
    half: 'w-1/2',
    third: 'w-1/3',
    quarter: 'w-1/4',
  };

  const heightMap = {
    auto: 'h-auto',
    full: 'h-full',
    screen: 'h-screen',
  };

  const colorMap = {
    red: 'bg-[#e63946]',
    yellow: 'bg-[#ffd60a]',
    blue: 'bg-[#0077b6]',
    black: 'bg-[#1a1a1a]',
    white: 'bg-[#f8f9fa]',
  };

  return (
    <div
      className={`${widthMap[width]} ${heightMap[height]} ${colorMap[color]} ${className}`}
      aria-hidden="true"
    />
  );
};

/**
 * Retro Card Component (1970s Style)
 * Rounded corners with earth tone accents
 */
export const BauhausCard = ({
  children,
  accentColor = 'orange',
  className = ''
}) => {
  const accentColorMap = {
    orange: 'bg-retro-orange',
    mustard: 'bg-retro-mustard',
    avocado: 'bg-retro-avocado',
    rust: 'bg-retro-rust',
    olive: 'bg-retro-olive',
    blue: 'bg-retro-avocado', // Map old blue to avocado
    red: 'bg-retro-rust', // Map old red to rust
    yellow: 'bg-retro-mustard', // Map old yellow to mustard
  };

  return (
    <div
      className={`
        bg-white rounded-retro-lg
        shadow-[0_8px_0_rgba(92,64,51,0.1),0_12px_24px_rgba(92,64,51,0.15)]
        p-6 relative overflow-hidden
        ${className}
      `}
    >
      {/* Retro accent stripe at top */}
      <div className={`absolute top-0 left-0 right-0 h-2 ${accentColorMap[accentColor]}`} />
      <div className="pt-2">
        {children}
      </div>
    </div>
  );
};

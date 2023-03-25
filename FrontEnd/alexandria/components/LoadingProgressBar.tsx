// LoadingProgressBar.tsx
import React from 'react';
import { Progress } from '@material-tailwind/react';

interface LoadingProgressBarProps {
  progress: number;
}

const LoadingProgressBar: React.FC<LoadingProgressBarProps> = ({ progress }) => {
  return (
    // <div className="h-1 w-full bg-neutral-200 dark:bg-neutral-600">
    //     <div className="h-1 bg-primary width: 45%"></div>
    // </div>
    <Progress value={progress} />
    
  );
};

export default LoadingProgressBar;

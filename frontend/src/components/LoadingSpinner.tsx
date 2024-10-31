import React from "react";

interface Props {
  size?: "small" | "medium" | "large";
  color?: string;
}

const LoadingSpinner: React.FC<Props> = ({
  size = "medium",
  color = "blue",
}) => {
  const sizeClass = {
    small: "w-4 h-4",
    medium: "w-8 h-8",
    large: "w-12 h-12",
  }[size];

  return (
    <div className="flex justify-center items-center">
      <div
        className={`${sizeClass} animate-spin rounded-full border-4 border-t-${color}-500`}
      />
    </div>
  );
};

export default LoadingSpinner;

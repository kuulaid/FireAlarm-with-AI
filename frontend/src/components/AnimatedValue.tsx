import { useEffect, useRef, useState } from "react";

interface AnimatedValueProps {
  value: string | number;
  className?: string;
}

// Re-renders the value with a unique key whenever it changes so the pop animation retriggers.
export function AnimatedValue({ value, className = "" }: AnimatedValueProps) {
  const [animKey, setAnimKey] = useState(0);
  const prevValue = useRef(value);

  useEffect(() => {
    if (prevValue.current !== value) {
      setAnimKey((current) => current + 1);
      prevValue.current = value;
    }
  }, [value]);

  return (
    <span key={animKey} className={`anim-value ${className}`}>
      {value}
    </span>
  );
}

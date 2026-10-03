// Measured element heights. Layout that depends on how tall something really
// is (push-down, region height, rail stacking) reads them here, so a node that
// grows, or rail text that wraps, never hides what is below it. Where
// ResizeObserver is missing (jsdom), nothing is measured and callers use
// nominal sizes.

import { useCallback, useEffect, useRef, useState } from "react";

export type MeasureRef = (key: string) => (element: HTMLElement | null) => void;

export function useMeasuredHeights(): [Record<string, number>, MeasureRef] {
  const [heights, setHeights] = useState<Record<string, number>>({});
  const observer = useRef<ResizeObserver | null>(null);
  const keys = useRef(new Map<Element, string>());
  const elements = useRef(new Map<string, Element>());

  useEffect(() => () => observer.current?.disconnect(), []);

  const measure = useCallback<MeasureRef>(
    (key) => (element) => {
      if (typeof ResizeObserver === "undefined") {
        return;
      }
      observer.current ??= new ResizeObserver((entries) => {
        setHeights((current) => {
          let next = current;
          for (const entry of entries) {
            const id = keys.current.get(entry.target);
            if (id === undefined || !(entry.target instanceof HTMLElement)) {
              continue;
            }
            const height = entry.target.offsetHeight;
            if (next[id] !== height) {
              next = next === current ? { ...current } : next;
              next[id] = height;
            }
          }
          return next;
        });
      });
      const previous = elements.current.get(key);
      if (previous === element) {
        return;
      }
      if (previous) {
        observer.current.unobserve(previous);
        keys.current.delete(previous);
        elements.current.delete(key);
      }
      if (element) {
        keys.current.set(element, key);
        elements.current.set(key, element);
        observer.current.observe(element);
      }
    },
    [],
  );

  return [heights, measure];
}

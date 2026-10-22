// A region's + Add menu (DESIGN.md Section 3, P3-EP04B §5.3). It lists only
// the contract types that belong to the region; the labels are the
// contracts' display labels. A menu button: arrows move, Escape closes.

import { useEffect, useId, useRef, useState } from "react";
import type { NodeContract } from "./api";

export function AddMenu({
  regionLabel,
  types,
  onAdd,
  registerButton,
}: {
  regionLabel: string;
  types: NodeContract[];
  onAdd: (type: string) => void;
  registerButton: (element: HTMLButtonElement | null) => void;
}) {
  const [open, setOpen] = useState(false);
  const menuId = useId();
  const button = useRef<HTMLButtonElement | null>(null);
  const menu = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (open) {
      menu.current
        ?.querySelector<HTMLButtonElement>("[role=menuitem]")
        ?.focus();
    }
  }, [open]);

  const close = (refocus: boolean) => {
    setOpen(false);
    if (refocus) {
      button.current?.focus();
    }
  };

  const items = () => [
    ...(menu.current?.querySelectorAll<HTMLButtonElement>("[role=menuitem]") ??
      []),
  ];

  return (
    <div
      className="add-menu"
      onBlur={(event) => {
        const next = event.relatedTarget;
        if (!(next instanceof Node && event.currentTarget.contains(next))) {
          setOpen(false);
        }
      }}
    >
      <button
        ref={(element) => {
          button.current = element;
          registerButton(element);
        }}
        type="button"
        className="button add-button"
        aria-haspopup="menu"
        aria-expanded={open}
        aria-controls={open ? menuId : undefined}
        aria-label={`Add node to ${regionLabel}`}
        onClick={() => setOpen((current) => !current)}
        onKeyDown={(event) => {
          if (event.key === "ArrowDown" && !open) {
            event.preventDefault();
            setOpen(true);
          }
        }}
      >
        + Add
      </button>
      {open && (
        <div
          ref={menu}
          id={menuId}
          className="add-list"
          role="menu"
          aria-label={`Node types for ${regionLabel}`}
          onKeyDown={(event) => {
            const list = items();
            const index = list.findIndex(
              (item) => item === globalThis.document.activeElement,
            );
            if (event.key === "ArrowDown" || event.key === "ArrowUp") {
              event.preventDefault();
              const step = event.key === "ArrowDown" ? 1 : -1;
              list[(index + step + list.length) % list.length]?.focus();
            } else if (event.key === "Home" || event.key === "End") {
              event.preventDefault();
              (event.key === "Home" ? list[0] : list.at(-1))?.focus();
            } else if (event.key === "Escape") {
              event.preventDefault();
              event.stopPropagation();
              close(true);
            } else if (event.key === "Tab") {
              close(false);
            }
          }}
        >
          {types.map((type) => (
            <button
              key={type.type}
              type="button"
              role="menuitem"
              tabIndex={-1}
              className="add-item"
              onClick={() => {
                setOpen(false);
                onAdd(type.type);
              }}
            >
              {type.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

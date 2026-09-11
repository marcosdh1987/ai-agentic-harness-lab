import type { SVGProps } from "react";

/**
 * The lab's own mark — a neutral, geometric stand-in for a brand logo.
 *
 * This repository deliberately carries no third-party branding (ADR-0060), so
 * the component that the shell and the login page reach for renders a shape
 * built from the design tokens instead of an imported logo. Every fill is
 * `var(--accent)` or `currentColor`, which means the mark re-themes with the
 * rest of the UI rather than pinning one company's colour into the markup.
 *
 * The glyph is three ascending bars: the harness ladder (ADR-0051), which is
 * the one picture this lab is actually about.
 */
export type LabMarkVariant =
  | "accent-white"
  | "accent-dark"
  | "white"
  | "icon-only"
  | "auto";

export type LabMarkProps = Omit<SVGProps<SVGSVGElement>, "ref"> & {
  variant?: LabMarkVariant;
  size?: number;
};

/** The three ladder bars, drawn inside a 30×33 box. */
const LADDER_BARS = [
  { x: 6, y: 20.5, width: 5.5, height: 7 },
  { x: 13.5, y: 15, width: 5.5, height: 12.5 },
  { x: 21, y: 9, width: 5.5, height: 18.5 }
];

export function LabMark({
  variant = "auto",
  size,
  width,
  height,
  className = "",
  style,
  ...rest
}: LabMarkProps) {
  if (variant === "icon-only") {
    const computedWidth = width ?? size ?? 28;
    const computedHeight = height ?? size ?? 28;
    return (
      <svg
        aria-label="Agentic Harness Lab"
        className={`lab-mark lab-mark--icon ${className}`}
        fill="none"
        height={computedHeight}
        role="img"
        style={style}
        viewBox="0 0 30 33"
        width={computedWidth}
        xmlns="http://www.w3.org/2000/svg"
        {...rest}
      >
        <rect fill="var(--accent)" height="32.3625" rx="6" width="29.9353" />
        {LADDER_BARS.map((bar) => (
          <rect
            fill="var(--accent-contrast, #FFFFFF)"
            height={bar.height}
            key={bar.x}
            rx="1.5"
            width={bar.width}
            x={bar.x}
            y={bar.y}
          />
        ))}
      </svg>
    );
  }

  // `auto` inherits the surrounding text colour so the mark reads correctly on
  // either theme without the caller having to know which one is active.
  const isDarkBg = variant === "accent-white";
  const isWhite = variant === "white";
  const letterFill = isWhite || isDarkBg ? "#FCFCFF" : "currentColor";

  const computedWidth = width ?? size ?? 140;
  const computedHeight = height ?? Math.round((Number(computedWidth) * 33) / 250);

  return (
    <svg
      aria-label="Agentic Harness Lab"
      className={`lab-mark lab-mark--wordmark lab-mark--${variant} ${className}`}
      fill="none"
      height={computedHeight}
      role="img"
      style={style}
      viewBox="0 0 250 33"
      width={computedWidth}
      xmlns="http://www.w3.org/2000/svg"
      {...rest}
    >
      <rect fill="var(--accent)" height="30" rx="6" width="30" y="1.5" />
      {LADDER_BARS.map((bar) => (
        <rect
          fill="var(--accent-contrast, #FFFFFF)"
          height={bar.height}
          key={bar.x}
          rx="1.5"
          width={bar.width}
          x={bar.x}
          y={bar.y}
        />
      ))}
      <text
        fill={letterFill}
        fontFamily="var(--font-display, system-ui, sans-serif)"
        fontSize="17"
        fontWeight="600"
        letterSpacing="0.6"
        x="42"
        y="23"
      >
        HARNESS LAB
      </text>
    </svg>
  );
}

// observable_theme.js — Observable Plot defaults for the linked view.
// Usage:
//   import { plotDefaults, sectorScale } from './observable_theme.js';
//   Plot.plot({ ...plotDefaults, marks: [...] });

export const palette = {
  total: "#1a1a1a", services: "#1f5fa6",
  education: "#2c8a57", manufacturing: "#c9602b",
  expLow: "#3a8fb7", expMid: "#c9b994", expHigh: "#a02030",
  quartile: ["#2e6b8c", "#6e9bab", "#c79568", "#a02030"],
  paper: "#fbf9f4", paper2: "#f3eee4", grid: "#e8e2d3",
  ink: "#1a1a1a", ink3: "#6b6660", rule: "#d8d1bf",
};

export const plotDefaults = {
  style: {
    background: "#fbf9f4",
    color: "#1a1a1a",
    fontFamily: "IBM Plex Sans, system-ui, sans-serif",
    fontSize: "12px",
  },
  marginTop: 28, marginRight: 16, marginBottom: 40, marginLeft: 56,
  x: { grid: false, tickSize: 0, labelOffset: 36, fontVariant: "tabular-nums" },
  y: { grid: true, tickSize: 0, labelOffset: 44, fontVariant: "tabular-nums" },
};

export const sectorScale = {
  domain: ["total", "services", "education", "manufacturing"],
  range: [palette.total, palette.services, palette.education, palette.manufacturing],
};

// AIOE-bipolar diverging scale, anchored at 0
export const aioeScale = {
  type: "diverging", pivot: 0,
  scheme: undefined,
  range: [palette.expLow, palette.expMid, palette.expHigh],
  domain: [-2.5, 1.5],
};

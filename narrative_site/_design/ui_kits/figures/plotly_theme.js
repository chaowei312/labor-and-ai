// plotly_theme.js — drop-in Plotly layout template for the narrative site.
// Usage:
//   import { plotlyTheme } from './plotly_theme.js';
//   Plotly.newPlot(el, traces, {...plotlyTheme.layout, ...overrides});

export const plotlyTheme = {
  colors: {
    total: "#1a1a1a", services: "#1f5fa6",
    education: "#2c8a57", manufacturing: "#c9602b",
    expLow: "#3a8fb7", expMid: "#c9b994", expHigh: "#a02030",
    quartile: ["#2e6b8c", "#6e9bab", "#c79568", "#a02030"],
    ink: "#1a1a1a", ink2: "#3d3a36", ink3: "#6b6660",
    paper: "#fbf9f4", paper2: "#f3eee4", rule: "#d8d1bf", grid: "#e8e2d3",
  },
  layout: {
    paper_bgcolor: "#fbf9f4",
    plot_bgcolor: "#fbf9f4",
    font: { family: "IBM Plex Sans, system-ui, sans-serif", size: 13, color: "#1a1a1a" },
    title: { font: { family: "Source Serif 4, Georgia, serif", size: 22, color: "#1a1a1a" }, x: 0, xanchor: "left", pad: { l: 0, t: 8, b: 12 } },
    margin: { l: 60, r: 24, t: 56, b: 56 },
    xaxis: {
      gridcolor: "#e8e2d3", gridwidth: 0.6,
      zerolinecolor: "#d8d1bf", zerolinewidth: 1,
      linecolor: "#888888", linewidth: 0.6,
      tickfont: { family: "IBM Plex Sans", size: 11, color: "#6b6660" },
      title: { font: { family: "IBM Plex Sans", size: 12, color: "#3d3a36" }, standoff: 10 },
    },
    yaxis: {
      gridcolor: "#e8e2d3", gridwidth: 0.6,
      zerolinecolor: "#d8d1bf", zerolinewidth: 1,
      linecolor: "transparent",
      tickfont: { family: "IBM Plex Sans", size: 11, color: "#6b6660" },
      title: { font: { family: "IBM Plex Sans", size: 12, color: "#3d3a36" }, standoff: 12 },
    },
    legend: {
      bgcolor: "rgba(0,0,0,0)", bordercolor: "transparent",
      font: { family: "IBM Plex Sans", size: 12, color: "#3d3a36" },
      orientation: "h", x: 0, y: 1.08, xanchor: "left", yanchor: "bottom",
    },
    hoverlabel: {
      bgcolor: "#fbf9f4", bordercolor: "#d8d1bf",
      font: { family: "IBM Plex Sans", size: 12, color: "#1a1a1a" },
    },
    transition: { duration: 720, easing: "cubic-out" },
  },
  config: { displayModeBar: false, responsive: true },
};

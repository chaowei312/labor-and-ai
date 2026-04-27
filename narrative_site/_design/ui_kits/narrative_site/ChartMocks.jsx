// ChartMocks.jsx — visual stand-ins for the eight figures from the bundle.
// These are NOT live charts — they're SVG mockups that establish the chart-chrome
// vocabulary (axes, gridlines, palette, annotation pencil). Real charts plug in via FigureFrame.

const SectorIndexChart = () => {
  const series = [
    { color: "var(--total)",         label: "Total nonfarm",       d: "M0 110 C 80 100, 160 88, 240 76 S 360 64, 520 50" },
    { color: "var(--services)",      label: "Pro & bus svcs",       d: "M0 110 C 80 80, 160 56, 240 38 L 270 30 L 285 90 C 320 70, 380 38, 480 18 L 520 22" },
    { color: "var(--education)",     label: "Edu & health",         d: "M0 110 C 80 92, 160 70, 240 52 L 270 48 L 282 100 C 320 80, 400 40, 520 8" },
    { color: "var(--manufacturing)", label: "Manufacturing",        d: "M0 110 C 80 102, 160 92, 240 82 L 270 78 L 285 122 C 320 110, 400 88, 520 72" },
  ];
  return (
    <div>
      <div style={{ display: "flex", gap: 18, marginBottom: 10, flexWrap: "wrap" }}>
        {series.map(s => (
          <div key={s.label} style={{ display: "flex", alignItems: "center", gap: 6, fontFamily: "var(--font-sans)", fontSize: 12, color: "var(--ink-2)" }}>
            <span style={{ width: 14, height: 2, background: s.color }} /> {s.label}
          </div>
        ))}
      </div>
      <svg viewBox="0 0 540 160" width="100%" height="240" style={{ display: "block" }}>
        {[40, 70, 100, 130].map(y => (
          <line key={y} x1="0" y1={y} x2="540" y2={y} stroke="var(--paper-3)" strokeWidth="0.6"/>
        ))}
        <line x1="0" y1="130" x2="540" y2="130" stroke="var(--ink-3)" strokeWidth="0.6" strokeDasharray="3 3"/>
        {series.map(s => (
          <path key={s.label} d={s.d} fill="none" stroke={s.color} strokeWidth="1.8"/>
        ))}
        {[0,90,180,270,360,450,540].map((x,i) => (
          <text key={x} x={x} y="155" fontFamily="Inter" fontSize="10" fill="var(--ink-3)" textAnchor={i===0?"start":i===6?"end":"middle"}>{2010+i*2.5|0}</text>
        ))}
        <text x="0" y="135" fontFamily="IBM Plex Mono" fontSize="10" fill="var(--ink-3)">100</text>
        <text x="0" y="103" fontFamily="IBM Plex Mono" fontSize="10" fill="var(--ink-3)">110</text>
        <text x="0" y="73" fontFamily="IBM Plex Mono" fontSize="10" fill="var(--ink-3)">120</text>
        <text x="0" y="43" fontFamily="IBM Plex Mono" fontSize="10" fill="var(--ink-3)">140</text>
      </svg>
    </div>
  );
};

const AioeWageScatter = () => {
  const pts = Array.from({length: 110}, (_, i) => {
    const x = (Math.random() * 4 - 2.3);
    const y = 50 + x * 18 + (Math.random() - 0.5) * 32;
    const r = 2 + Math.random() * Math.random() * 12;
    return { x, y, r };
  });
  return (
    <svg viewBox="0 0 540 220" width="100%" height="260" style={{ display: "block" }}>
      {[40, 80, 120, 160, 200].map(y => (
        <line key={y} x1="40" y1={y} x2="540" y2={y} stroke="var(--paper-3)" strokeWidth="0.6"/>
      ))}
      {pts.map((p, i) => (
        <circle key={i}
          cx={50 + ((p.x + 2.5) / 4) * 480}
          cy={210 - p.y * 1.6}
          r={p.r}
          fill="var(--exp-high)" opacity="0.22" stroke="white" strokeWidth="0.3"/>
      ))}
      <text x="50" y="218" fontFamily="Inter" fontSize="10" fill="var(--ink-3)">−2</text>
      <text x="290" y="218" fontFamily="Inter" fontSize="10" fill="var(--ink-3)" textAnchor="middle">0</text>
      <text x="530" y="218" fontFamily="Inter" fontSize="10" fill="var(--ink-3)" textAnchor="end">+1.5</text>
      <text x="50" y="20" fontFamily="Inter" fontSize="11" fill="var(--ink-3)">corr(AIOE, log wage) = +0.58</text>
      <text x="290" y="232" fontFamily="Inter" fontSize="11" fill="var(--ink-2)" textAnchor="middle">AIOE score</text>
    </svg>
  );
};

Object.assign(window, { SectorIndexChart, AioeWageScatter });

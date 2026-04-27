// LinkedView.jsx — the Act 3 AIOE-slider linked block: slider drives wage hist + emp density + SOC mix.
// Mocked with SVG (no live data); the editorial behaviour is real.

const LinkedView = () => {
  const [aioe, setAioe] = React.useState(0.74);
  const matched = Math.round(214 + (1.5 - aioe) * 95);
  const empPct = Math.max(8, Math.round(39 + (0.5 - aioe) * 28));

  const histBars = [
    { x: 30000, h: 24 },{ x: 40000, h: 56 },{ x: 50000, h: 78 },{ x: 60000, h: 64 },
    { x: 70000, h: 52 },{ x: 80000, h: 44 },{ x: 90000, h: 38 },{ x: 100000, h: 32 },
    { x: 120000, h: 22 },{ x: 140000, h: 14 },
  ];

  return (
    <div style={{ background: "var(--paper-2)", borderRadius: 4, padding: 24 }}>
      <div style={{ marginBottom: 18 }}>
        <div style={{ fontFamily: "var(--font-sans)", fontSize: 14, color: "var(--ink-2)", marginBottom: 12 }}>
          Show only occupations with AIOE ≥{" "}
          <b style={{ fontFamily: "var(--font-mono)", color: "var(--ink)", fontSize: 15 }}>{aioe >= 0 ? "+" : ""}{aioe.toFixed(2)}</b>
        </div>
        <div style={{ position: "relative", height: 36 }}>
          <div style={{
            position: "absolute", top: 16, left: 0, right: 0, height: 3,
            background: "linear-gradient(90deg, var(--exp-low), var(--exp-mid), var(--exp-high))",
            borderRadius: 2,
          }} />
          <div style={{
            position: "absolute", top: 16, left: `${((aioe + 2.5) / 4) * 100}%`, right: 0,
            height: 3, background: "var(--ink)", borderRadius: 2,
          }} />
          <input type="range" min="-2.5" max="1.5" step="0.05" value={aioe}
            onChange={e => setAioe(parseFloat(e.target.value))}
            style={{
              position: "absolute", inset: 0, width: "100%", height: 36,
              background: "transparent", appearance: "none", cursor: "pointer",
            }} />
          <div style={{
            position: "absolute", top: 6, left: `calc(${((aioe + 2.5) / 4) * 100}% - 11px)`,
            width: 22, height: 22, borderRadius: 999,
            background: "var(--paper)", border: "1.5px solid var(--ink)",
            boxShadow: "var(--shadow-1)", pointerEvents: "none",
          }} />
        </div>
        <div style={{
          display: "flex", justifyContent: "space-between",
          fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--ink-3)", marginTop: 4,
        }}>
          <span>−2.5 · low exposure (augment)</span>
          <span>0</span>
          <span>+1.5 · high exposure (displace)</span>
        </div>
        <div style={{
          fontFamily: "var(--font-sans)", fontSize: 13, color: "var(--ink-3)", marginTop: 14,
        }}>
          {matched} of 749 occupations match · {empPct}% of total employment
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 24, marginTop: 24 }}>
        <div>
          <div style={{
            fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
            letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--ink-3)",
            marginBottom: 8,
          }}>Wage distribution · 2018</div>
          <svg viewBox="0 0 400 160" width="100%" height="160" style={{ display: "block" }}>
            <line x1="20" y1="140" x2="400" y2="140" stroke="var(--rule)" strokeWidth="0.6"/>
            <line x1="20" y1="100" x2="400" y2="100" stroke="var(--paper-3)" strokeWidth="0.6"/>
            <line x1="20" y1="60" x2="400" y2="60" stroke="var(--paper-3)" strokeWidth="0.6"/>
            {histBars.map((b, i) => (
              <rect key={i} x={30 + i * 36} y={140 - b.h * (1 - aioe * 0.15)}
                width="28" height={b.h * (1 - aioe * 0.15)}
                fill={i >= 4 ? "var(--exp-high)" : "var(--rule)"}
                opacity={i >= 4 ? 0.85 : 0.35} />
            ))}
            <text x="20" y="156" fontFamily="JetBrains Mono" fontSize="10" fill="var(--ink-3)">$30k</text>
            <text x="380" y="156" fontFamily="JetBrains Mono" fontSize="10" fill="var(--ink-3)" textAnchor="end">$140k+</text>
          </svg>
        </div>
        <div>
          <div style={{
            fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
            letterSpacing: "0.06em", textTransform: "uppercase", color: "var(--ink-3)",
            marginBottom: 8,
          }}>SOC mix · top families</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {[
              { label: "Business & Financial", pct: 22 },
              { label: "Computer & Math", pct: 18 },
              { label: "Legal", pct: 12 },
              { label: "Mgmt", pct: 11 },
              { label: "Office & Admin", pct: 9 },
            ].map(s => (
              <div key={s.label} style={{ display: "flex", alignItems: "center", gap: 8, fontFamily: "var(--font-sans)", fontSize: 12 }}>
                <div style={{ width: 110, color: "var(--ink-2)" }}>{s.label}</div>
                <div style={{ flex: 1, height: 8, background: "var(--paper-3)" }}>
                  <div style={{ width: `${s.pct * 3.5}%`, height: "100%", background: "var(--exp-high)", opacity: 0.85 }}/>
                </div>
                <div style={{ fontFamily: "var(--font-mono)", color: "var(--ink-3)", width: 28, textAlign: "right" }}>{s.pct}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
window.LinkedView = LinkedView;

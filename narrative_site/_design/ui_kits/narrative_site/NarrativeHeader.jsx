// NarrativeHeader.jsx — page-level header: monogram + section nav + scroll progress
// The narrative site has minimal chrome. This is intentionally lightweight.

const NarrativeHeader = ({ activeAct = 1, onJump }) => {
  const acts = [
    { n: 1, label: "Where AI is positioned" },
    { n: 2, label: "Through 2023" },
    { n: 3, label: "Probing the thesis" },
    { n: 5, label: "Coda" },
  ];
  return (
    <header style={{
      position: "sticky", top: 0, zIndex: 50,
      background: "rgba(251,249,244,0.92)", backdropFilter: "blur(0px)",
      borderBottom: "1px solid var(--rule)",
      padding: "12px var(--page-pad-x)",
    }}>
      <div style={{
        maxWidth: "var(--page-max)", margin: "0 auto",
        display: "flex", alignItems: "center", gap: "var(--s-6)",
      }}>
        <a href="#top" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none", whiteSpace: "nowrap" }}>
          <img src="../../assets/monogram.svg" alt="" style={{ width: 28, height: 28 }} />
          <span style={{
            fontFamily: "var(--font-serif)", fontWeight: 600, fontSize: 17,
            letterSpacing: "-0.012em", color: "var(--ink)", whiteSpace: "nowrap",
          }}>Labor <i style={{ color: "var(--highlight)" }}>&amp;</i> AI</span>
        </a>
        <nav style={{ display: "flex", gap: 18, marginLeft: "auto" }}>
          {acts.map(a => (
            <button key={a.n} onClick={() => onJump?.(a.n)} style={{
              background: "none", border: 0, padding: "4px 0", cursor: "pointer",
              fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
              letterSpacing: "0.08em", textTransform: "uppercase",
              color: activeAct === a.n ? "var(--ink)" : "var(--ink-3)",
              borderBottom: activeAct === a.n ? "1.5px solid var(--ink)" : "1.5px solid transparent",
              transition: "color var(--dur-fast) var(--ease-out)",
            }}>
              {a.n === 5 ? "Coda" : `Act ${a.n}`}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};
window.NarrativeHeader = NarrativeHeader;

// FigureFrame.jsx — the standard chart container: kicker, title, deck, chart slot, source line.
// Every figure on the page uses this. Reuters/Upshot pattern; not negotiable.

const FigureFrame = ({ figId, kicker, title, deck, caveat, source, children, fullBleed }) => (
  <figure style={{
    margin: "var(--s-7) 0",
    maxWidth: fullBleed ? "none" : "var(--page-max)",
  }}>
    <div style={{ maxWidth: 720, marginBottom: 16 }}>
      {kicker && (
        <div style={{
          fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
          letterSpacing: "0.14em", textTransform: "uppercase",
          color: "var(--ink-3)", marginBottom: 8,
        }}>{kicker}</div>
      )}
      {title && (
        <h3 style={{
          fontFamily: "var(--font-serif)", fontSize: 26, fontWeight: 600,
          letterSpacing: "-0.012em", lineHeight: 1.2, color: "var(--ink)",
          margin: "0 0 8px 0", textWrap: "balance",
        }}>{title}</h3>
      )}
      {deck && (
        <p style={{
          fontFamily: "var(--font-serif)", fontSize: 18, fontStyle: "italic",
          lineHeight: 1.45, color: "var(--ink-2)", margin: 0,
        }}>{deck}</p>
      )}
    </div>
    <div style={{ background: "transparent" }}>{children}</div>
    {caveat && (
      <div style={{ marginTop: 10 }}>
        <span style={{
          display: "inline-flex", alignItems: "center", gap: 6,
          padding: "3px 9px", borderRadius: 999,
          border: "1px solid var(--rule)", color: "var(--ink-3)",
          fontFamily: "var(--font-sans)", fontSize: 12, letterSpacing: "0.04em",
        }}>{caveat}</span>
      </div>
    )}
    {source && (
      <figcaption style={{
        marginTop: 12, paddingTop: 8, borderTop: "1px solid var(--rule)",
        fontFamily: "var(--font-sans)", fontSize: 13, color: "var(--ink-3)",
        lineHeight: 1.5,
      }}>
        <b style={{ fontWeight: 600, color: "var(--ink-2)" }}>Source</b> · {source}
        {figId && <> &nbsp;·&nbsp; <span style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>{figId}</span></>}
      </figcaption>
    )}
  </figure>
);
window.FigureFrame = FigureFrame;

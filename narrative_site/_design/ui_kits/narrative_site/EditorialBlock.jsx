// EditorialBlock.jsx — the page's prose blocks: kicker, headline, deck, body
// This is the typographic atom of the entire narrative.

const Kicker = ({ children, color }) => (
  <div style={{
    fontFamily: "var(--font-sans)", fontSize: 12, fontWeight: 600,
    letterSpacing: "0.14em", textTransform: "uppercase",
    color: color || "var(--ink-3)", marginBottom: 8,
  }}>{children}</div>
);

const Headline = ({ level = 1, children }) => {
  const sizes = {
    hero: { fontSize: "clamp(44px, 4vw + 24px, 84px)", lineHeight: 1.02, letterSpacing: "-0.022em" },
    1:    { fontSize: "clamp(32px, 1.4vw + 24px, 52px)", lineHeight: 1.08, letterSpacing: "-0.02em" },
    2:    { fontSize: 28, lineHeight: 1.18, letterSpacing: "-0.015em" },
    3:    { fontSize: 22, lineHeight: 1.25, letterSpacing: "-0.012em" },
  };
  return (
    <h2 style={{
      fontFamily: "var(--font-serif)", fontWeight: 600, color: "var(--ink)",
      margin: "0 0 14px 0", textWrap: "balance", ...sizes[level],
    }}>{children}</h2>
  );
};

const Deck = ({ children }) => (
  <p style={{
    fontFamily: "var(--font-serif)", fontSize: 24, lineHeight: 1.55,
    fontStyle: "italic", color: "var(--ink-2)", fontWeight: 400,
    margin: "0 0 32px 0", maxWidth: "var(--reading-max)",
    textWrap: "pretty", letterSpacing: "-0.005em",
  }}>{children}</p>
);

const Body = ({ children }) => (
  <p style={{
    fontFamily: "var(--font-serif)", fontSize: 18, lineHeight: 1.7,
    color: "var(--ink)", margin: "0 0 22px 0", maxWidth: "var(--reading-max)",
    textWrap: "pretty",
  }}>{children}</p>
);

const Caveat = ({ children }) => (
  <span style={{
    display: "inline-flex", alignItems: "center", gap: 6,
    padding: "2px 8px", borderRadius: 999,
    border: "1px solid var(--rule)", color: "var(--ink-3)",
    fontFamily: "var(--font-sans)", fontSize: 12, letterSpacing: "0.04em",
  }}>{children}</span>
);

Object.assign(window, { Kicker, Headline, Deck, Body, Caveat });

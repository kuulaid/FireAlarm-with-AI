export default function BottomNav({ page, onNavTo }) {
  return (
    <nav className="bnav">
      <button
        className={`bn-item${page === "home" ? " active" : ""}`}
        onClick={() => onNavTo("home")}
      >
        <span className="bn-icon">⊞</span>
        Home
      </button>
      <button
        className={`bn-item${page === "history" || page === "detail" ? " active" : ""}`}
        onClick={() => onNavTo("history")}
      >
        <span className="bn-icon">🕒</span>
        History
      </button>
    </nav>
  );
}

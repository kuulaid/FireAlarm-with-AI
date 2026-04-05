export default function Sidebar({ open, page, onNavTo, onClose }) {
  return (
    <>
      <div className={`overlay${open ? " on" : ""}`} onClick={onClose} />

      <nav className={`sidebar${open ? " open" : ""}`}>
        <div className="s-logo">
          <div className="s-logo-icon">🏭</div>
          <div className="s-logo-text">Industrial<br />Precision</div>
        </div>
        <div className="s-nav">
          <button className={`s-item${page === "home" ? " active" : ""}`} onClick={() => onNavTo("home")}>
            <span className="s-icon">⊞</span> Home
          </button>
          <button
            className={`s-item${page === "history" || page === "detail" ? " active" : ""}`}
            onClick={() => onNavTo("history")}
          >
            <span className="s-icon">🕒</span> History
          </button>
        </div>
        <div className="s-footer">
          <div className="avatar">👤</div>
          <div>
            <div className="av-name">Admin</div>
            <div className="av-role">Safety Officer</div>
          </div>
        </div>
      </nav>
    </>
  );
}

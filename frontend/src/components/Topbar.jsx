export default function Topbar({ page, onBurgerClick, titles }) {
  return (
    <div className="topbar">
      <div className="tb-left">
        <button className="burger" onClick={onBurgerClick}>☰</button>
        <div className="tb-titles">
          <div className="tb-title">{titles[page]}</div>
          <div className="tb-sub">Environmental Monitoring</div>
        </div>
      </div>
      <div className="live-pill">
        <div className="live-dot" /> LIVE
      </div>
    </div>
  );
}

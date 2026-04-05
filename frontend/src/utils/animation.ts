// Animation CSS is injected at runtime so the frontend can animate page enters and banners without a separate stylesheet.
export const ANIMATION_CSS = `
  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .anim-page { animation: fadeSlideUp 0.32s cubic-bezier(0.22,1,0.36,1) both; }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .anim-item { opacity: 0; animation: fadeIn 0.28s cubic-bezier(0.22,1,0.36,1) forwards; }
  .anim-item:nth-child(1)  { animation-delay: 0.04s; }
  .anim-item:nth-child(2)  { animation-delay: 0.09s; }
  .anim-item:nth-child(3)  { animation-delay: 0.14s; }
  .anim-item:nth-child(4)  { animation-delay: 0.19s; }
  .anim-item:nth-child(5)  { animation-delay: 0.24s; }
  .anim-item:nth-child(6)  { animation-delay: 0.28s; }

  @keyframes bannerIn {
    from { opacity: 0; transform: scale(0.97) translateY(-6px); }
    to   { opacity: 1; transform: scale(1) translateY(0); }
  }
  .anim-banner { animation: bannerIn 0.38s cubic-bezier(0.22,1,0.36,1) both; }

  @keyframes criticalGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
    50%       { box-shadow: 0 0 0 10px rgba(239,68,68,0.2); }
  }
  .anim-critical-glow { animation: criticalGlow 2s ease-in-out infinite; }

  @keyframes mediumGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(249,115,22,0); }
    50%       { box-shadow: 0 0 0 8px rgba(249,115,22,0.18); }
  }
  .anim-medium-glow { animation: mediumGlow 2.5s ease-in-out infinite; }

  @keyframes valuePop {
    0%   { opacity: 0; transform: scale(0.75); }
    70%  { transform: scale(1.06); }
    100% { opacity: 1; transform: scale(1); }
  }
  .anim-value { animation: valuePop 0.45s cubic-bezier(0.34,1.56,0.64,1) both; }

  .hover-lift {
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }
  .hover-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px -4px rgba(0,0,0,0.10);
  }

  @keyframes wobble {
    0%,100% { transform: rotate(0deg); }
    20%     { transform: rotate(-8deg); }
    40%     { transform: rotate(8deg); }
    60%     { transform: rotate(-5deg); }
    80%     { transform: rotate(4deg); }
  }
  .anim-wobble { animation: wobble 1.4s ease-in-out infinite; }

  .btn-press { transition: transform 0.12s ease, filter 0.12s ease; }
  .btn-press:active { transform: scale(0.96); filter: brightness(0.95); }

  @keyframes overlayIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  .anim-overlay { animation: overlayIn 0.2s ease both; }

  .hover-chev:hover .chev-icon { transform: translateX(3px); }
  .chev-icon { transition: transform 0.18s ease; display: inline-flex; }
`;

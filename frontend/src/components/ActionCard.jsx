import "./ActionCard.css";

function ActionCard() {
  return (
    <aside className="action-card">
      <h2 className="action-title">Action Required</h2>

      <ul className="action-list">

        <li className="action-item">
          <span className="status-dot"></span>
          <span className="text">O2 is low</span>
        </li>

        <li className="action-item">
          <span className="status-dot"></span>
          <span className="text">ship hull is weak</span>
        </li>

        <li className="action-item">
          <span className="status-dot"></span>
          <span className="text">fuel is low</span>
        </li>

      </ul>
    </aside>
  );
}

export default ActionCard;
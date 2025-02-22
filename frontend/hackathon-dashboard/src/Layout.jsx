import { Link } from "react-router-dom";
import { useState } from "react";
import { Menu, X } from "lucide-react";
import "./Layout.css"; // Import the CSS file

const Layout = ({ children }) => {
    const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${isOpen ? "open" : "closed"}`}>
        {/* Toggle Button */}
        <button className="toggle-btn" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>        

        <h2 className="sidebar-title">My App</h2>

        {/* Navigation Links */}
        <nav>
            <ul>
                <li>
                  <Link to="/Home"><span>🏠</span> <span className={isOpen ? "show" : "hide"}>Home</span></Link>
                </li>
                <li>
                  <Link to="/TopPerformers"><span>📊</span> <span className={isOpen ? "show" : "hide"}>Top Performers</span></Link>
                </li>
                <li>
                  <Link to="/MacroOutlook"><span>📈</span> <span className={isOpen ? "show" : "hide"}>Macro Outlook</span></Link>
                </li>
                <li>
                  <Link to="/StockProfile"><span>📜</span> <span className={isOpen ? "show" : "hide"}>Stock Profile</span></Link>
                </li>
            </ul>
        </nav>
      </aside>

      {/* Main content */}
      <main className="content">{children}</main>
    </div>
  );
};

export default Layout;

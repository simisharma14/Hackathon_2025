// components/Layout.jsx
import { Link } from "react-router-dom";
import { useState } from "react";
import { Menu, X } from "lucide-react";

const Layout = ({ children }) => {
    const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside
        className={`bg-gray-800 text-white p-4 transition-all duration-300 ${
          isOpen ? "w-64" : "w-16"
        } flex flex-col h-full`}
      >
        {/* Toggle Button */}
        <button
          className="text-white mb-4 self-end"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>        
        <h2 className="text-xl font-bold">My App</h2>
        {/* Navigation Links */}
        <nav className="mt-4">
            <ul>
                <li className="mb-2">
                <Link to="/Home" className="hover:text-gray-300">Home</Link>
                </li>
                <li className="mb-2">
                <Link to="/TopPerformers" className="hover:text-gray-300">Top Performers</Link>
                </li>
                <li className="mb-2">
                <Link to="/MacroOutlook" className="hover:text-gray-300">Macro Outlook</Link>
                </li>
                <li className="mb-2">
                <Link to="/StockProfile" className="hover:text-gray-300">Stock Profile</Link>
                </li>
            </ul>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
};

export default Layout;

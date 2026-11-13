import {
  Home,
  FileText,
  BarChart2,
  Terminal,
  LogIn,
  Settings,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const navItems = [
    { icon: Home, label: "Home", path: "/" },
    { icon: FileText, label: "Leave Requests", path: "/leave" },
    { icon: BarChart2, label: "Statistics", path: "/statistics" },
    { icon: Terminal, label: "App Logs", path: "/logs" },
  ];

  return (
    <aside className="w-64 bg-sidebar border-r border-gray-800 flex flex-col justify-between h-screen select-none">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-800/60">
          <div className="w-8 h-8 rounded-lg bg-accentBlue flex items-center justify-center font-bold text-white shadow-lg shadow-blue-600/30">
            P
          </div>
          <span className="font-bold text-lg text-white tracking-wide">
            PoukAdmin
          </span>
        </div>

        {/* Nav Links */}
        <nav className="px-3 py-4 space-y-1">
          {navItems.map((item, idx) => {
            const Icon = item.icon;
            return (
              <button
                key={idx}
                onClick={() => navigate(item.path)}
                className="w-full flex items-center gap-3.5 px-3.5 py-2.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800/50 transition-all font-medium text-sm group"
              >
                <Icon
                  size={18}
                  className="group-hover:text-accentBlue transition-colors"
                />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer / Login Action */}
      <div className="p-4 border-t border-gray-800/60 space-y-3">
        {user ? (
          <div className="flex items-center justify-between px-2">
            <div className="truncate">
              <p className="text-sm font-medium text-white truncate">
                {user.full_name}
              </p>
              <p className="text-xs text-gray-400 capitalize">{user.role}</p>
            </div>
            <button
              onClick={logout}
              className="text-xs text-red-400 hover:text-red-300 font-medium px-2.5 py-1.5 rounded bg-red-500/10 hover:bg-red-500/20 transition"
            >
              Logout
            </button>
          </div>
        ) : (
          <button
            onClick={() => navigate("/login")}
            className="w-full py-2.5 px-4 bg-accentBlue hover:bg-blue-700 text-white font-medium rounded-lg shadow-lg shadow-blue-600/20 transition flex items-center justify-center gap-2 text-sm"
          >
            <LogIn size={16} />
            LOGIN
          </button>
        )}

        <div className="flex items-center justify-between text-xs text-gray-500 px-2 pt-1 cursor-pointer hover:text-gray-400">
          <span className="flex items-center gap-1.5">
            <Settings size={14} /> Quick Settings
          </span>
          <span>v1.0</span>
        </div>
      </div>
    </aside>
  );
}

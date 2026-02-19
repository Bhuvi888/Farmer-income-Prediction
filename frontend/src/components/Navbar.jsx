import { useState } from "react";
import { Menu, X, Sprout } from "lucide-react";

const links = [
  { label: "Dashboard", href: "#dashboard" },
  { label: "Prediction", href: "#prediction" },
  { label: "Insights", href: "#insights" },
  { label: "About", href: "#about" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <a href="#" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-lg bg-primary-600 flex items-center justify-center group-hover:bg-primary-700 transition-colors">
              <Sprout className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">
              Agri<span className="text-primary-600">Predict</span> AI
            </span>
          </a>

          {/* Desktop menu */}
          <div className="hidden md:flex items-center gap-1">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="px-4 py-2 text-sm font-medium text-gray-600 rounded-lg hover:text-primary-700 hover:bg-primary-50 transition-all"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Mobile hamburger */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition"
            onClick={() => setOpen(!open)}
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile menu */}
        {open && (
          <div className="md:hidden pb-4 border-t border-gray-100 mt-2 pt-2">
            {links.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="block px-4 py-2.5 text-sm font-medium text-gray-600 rounded-lg hover:text-primary-700 hover:bg-primary-50 transition-all"
                onClick={() => setOpen(false)}
              >
                {link.label}
              </a>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}

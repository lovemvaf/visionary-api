"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Globe,
  BookOpen,
  Radio,
  Award,
  Calendar,
  Briefcase,
  Users,
  Compass,
  Menu,
  X,
  User,
  LogOut,
  LayoutDashboard,
  Moon,
  Sun
} from "lucide-react";
import { api } from "../lib/api";
import { UserProfile } from "../lib/types";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Check dark mode
    if (localStorage.getItem("theme") === "dark" || (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      document.documentElement.classList.add("dark");
      setIsDark(true);
    } else {
      document.documentElement.classList.remove("dark");
      setIsDark(false);
    }

    // Check auth
    api.getMe().then((res) => {
      if (res.success && res.data) {
        setUser(res.data);
      }
    });
  }, [pathname]);

  const toggleTheme = () => {
    if (isDark) {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
      setIsDark(false);
    } else {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
      setIsDark(true);
    }
  };

  const handleLogout = () => {
    api.logout();
    setUser(null);
    router.push("/");
  };

  const navLinks = [
    { name: "Trang chủ", href: "/" },
    { name: "CLB DNTU", href: "/about" },
    { name: "English for IT", href: "/english-for-it", icon: BookOpen },
    { name: "Tech Radar", href: "/tech-radar", icon: Radio },
    { name: "Cuộc thi & Hội nhập", href: "/opportunities", icon: Compass },
    { name: "Career Gateway", href: "/careers", icon: Briefcase },
    { name: "Sự kiện", href: "/events", icon: Calendar },
    { name: "Bảng vàng", href: "/achievements", icon: Award },
    { name: "Tin tức", href: "/posts" },
  ];

  const isManager = user?.roles.includes("Admin") || user?.roles.includes("Committee");

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-surface-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-navy to-visionary flex items-center justify-center text-white shadow-md shadow-visionary/20 group-hover:scale-105 transition-transform">
              <Globe className="w-5 h-5 text-tealAccent" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-navy to-visionary dark:from-white dark:to-tealAccent bg-clip-text text-transparent">
                VISIONARY
              </span>
              <span className="block text-[10px] uppercase tracking-wider font-semibold text-tealAccent -mt-1">
                DNTU Platform
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden xl:flex items-center gap-1">
            {navLinks.map((link) => {
              const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                    isActive
                      ? "bg-visionary text-white shadow-sm"
                      : "text-navy dark:text-gray-200 hover:bg-visionary/10 dark:hover:bg-white/10"
                  }`}
                >
                  {link.name}
                </Link>
              );
            })}
          </nav>

          {/* Right Actions: Dark Mode + Auth */}
          <div className="hidden sm:flex items-center gap-3">
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-navy-light transition-colors"
            >
              {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-navy" />}
            </button>

            {user ? (
              <div className="flex items-center gap-2">
                <Link
                  href={isManager ? "/dashboard/admin" : "/dashboard"}
                  className="flex items-center gap-2 px-3 py-1.5 text-xs font-semibold rounded-lg bg-navy/5 dark:bg-white/10 text-navy dark:text-white hover:bg-navy/10 transition-colors"
                >
                  <User className="w-3.5 h-3.5 text-tealAccent" />
                  <span>{user.fullName}</span>
                  {isManager && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-tealAccent/20 text-tealAccent font-bold">
                      BCN/Admin
                    </span>
                  )}
                </Link>

                <button
                  onClick={handleLogout}
                  title="Đăng xuất"
                  className="p-2 rounded-lg text-gray-500 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/auth/login"
                  className="px-3.5 py-1.5 text-xs font-semibold text-navy dark:text-gray-200 hover:text-visionary transition-colors"
                >
                  Đăng nhập
                </Link>
                <Link
                  href="/auth/register"
                  className="px-3.5 py-1.5 text-xs font-semibold text-white bg-visionary hover:bg-visionary-hover rounded-lg shadow-sm shadow-visionary/30 transition-all hover:scale-[1.02]"
                >
                  Đăng ký
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center gap-2 xl:hidden">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-navy-light"
            >
              {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-navy" />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-navy dark:text-white hover:bg-gray-100 dark:hover:bg-navy-light"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t border-surface-border bg-white dark:bg-navy-dark px-4 pt-3 pb-6 space-y-1 shadow-xl">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileMenuOpen(false)}
              className={`block px-3 py-2 text-sm font-medium rounded-lg ${
                pathname === link.href
                  ? "bg-visionary text-white"
                  : "text-navy dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-navy"
              }`}
            >
              {link.name}
            </Link>
          ))}

          <div className="pt-4 border-t border-gray-200 dark:border-gray-800 flex flex-col gap-2">
            {user ? (
              <>
                <Link
                  href={isManager ? "/dashboard/admin" : "/dashboard"}
                  onClick={() => setMobileMenuOpen(false)}
                  className="w-full flex items-center justify-center gap-2 py-2 text-sm font-semibold rounded-lg bg-visionary/10 text-visionary dark:text-tealAccent"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  Bảng điều khiển ({user.fullName})
                </Link>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full py-2 text-sm font-semibold rounded-lg text-red-500 bg-red-50 dark:bg-red-950/20"
                >
                  Đăng xuất
                </button>
              </>
            ) : (
              <div className="grid grid-cols-2 gap-2">
                <Link
                  href="/auth/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center py-2 text-sm font-semibold rounded-lg border border-gray-300 dark:border-gray-700 text-navy dark:text-white"
                >
                  Đăng nhập
                </Link>
                <Link
                  href="/auth/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center py-2 text-sm font-semibold rounded-lg bg-visionary text-white"
                >
                  Đăng ký
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

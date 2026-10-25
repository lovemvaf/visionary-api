"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Globe,
  BookOpen,
  Radio,
  Award,
  Calendar,
  Briefcase,
  Compass,
  Menu,
  X,
  User,
  LogOut,
  Moon,
  Sun,
  ChevronDown,
  ShieldCheck,
  Users,
  Sparkles,
  Layers,
  GraduationCap
} from "lucide-react";
import { api } from "../lib/api";
import { UserProfile } from "../lib/types";

export default function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isDark, setIsDark] = useState(false);
  
  // Active desktop dropdown
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  // Mobile submenu expansion
  const [expandedMobileGroup, setExpandedMobileGroup] = useState<string | null>(null);

  const navRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Theme initialization
    if (
      localStorage.getItem("theme") === "dark" ||
      (!("theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
      document.documentElement.classList.add("dark");
      setIsDark(true);
    } else {
      document.documentElement.classList.remove("dark");
      setIsDark(false);
    }

    // Auth check
    api.getMe().then((res) => {
      if (res.success && res.data) {
        setUser(res.data);
      }
    });
  }, [pathname]);

  // Click outside to close dropdowns
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (navRef.current && !navRef.current.contains(event.target as Node)) {
        setOpenDropdown(null);
        setUserMenuOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close menus on route change
  useEffect(() => {
    setOpenDropdown(null);
    setUserMenuOpen(false);
    setMobileMenuOpen(false);
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

  // Determine user's primary display role badge (NO "BCN/Admin" conflation!)
  const getPrimaryRoleBadge = (roles: string[] = []) => {
    if (roles.includes("Admin")) {
      return { label: "Admin", style: "bg-red-500/15 text-red-600 dark:text-red-400 border-red-500/30" };
    }
    if (roles.includes("Committee")) {
      return { label: "Ban Chủ Nhiệm", style: "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30" };
    }
    if (roles.includes("Supervisor")) {
      return { label: "Cố vấn / GV", style: "bg-purple-500/15 text-purple-600 dark:text-purple-400 border-purple-500/30" };
    }
    if (roles.includes("Collaborator")) {
      return { label: "Cộng tác viên", style: "bg-indigo-500/15 text-indigo-600 dark:text-indigo-400 border-indigo-500/30" };
    }
    if (roles.includes("ClubMember")) {
      return { label: "Thành viên CLB", style: "bg-tealAccent/15 text-tealAccent border-tealAccent/30" };
    }
    return { label: "Sinh viên", style: "bg-blue-500/15 text-blue-600 dark:text-blue-400 border-blue-500/30" };
  };

  const isAdmin = user?.roles.includes("Admin");
  const isCommittee = user?.roles.includes("Committee");
  const roleBadge = getPrimaryRoleBadge(user?.roles);

  // Grouped Navigation structure
  const navGroups = [
    {
      title: "Học tập",
      id: "learning",
      items: [
        {
          name: "English for IT",
          href: "/english-for-it",
          desc: "Từ vựng chuyên ngành, ngữ pháp & thuật ngữ kỹ thuật",
          icon: BookOpen
        }
      ]
    },
    {
      title: "Công nghệ",
      id: "tech",
      items: [
        {
          name: "Tech Radar",
          href: "/tech-radar",
          desc: "Xu hướng GitHub Trending & AI Models Hugging Face",
          icon: Radio
        }
      ]
    },
    {
      title: "Cơ hội",
      id: "opportunities",
      items: [
        {
          name: "Cuộc thi & Học bổng",
          href: "/opportunities",
          desc: "Hackathon, giao lưu quốc tế & học bổng DNTU",
          icon: Compass
        },
        {
          name: "Career Gateway",
          href: "/careers",
          desc: "Việc làm IT, thực tập doanh nghiệp & cơ hội Remote",
          icon: Briefcase
        }
      ]
    },
    {
      title: "Hoạt động",
      id: "activities",
      items: [
        {
          name: "Sự kiện CLB",
          href: "/events",
          desc: "Workshop kỹ thuật, seminar học thuật & điểm danh QR",
          icon: Calendar
        },
        {
          name: "Bảng vàng Thành tích",
          href: "/achievements",
          desc: "Vinh danh sinh viên đạt giải thưởng quốc tế & NCKH",
          icon: Award
        }
      ]
    }
  ];

  return (
    <header ref={navRef} className="sticky top-0 z-50 glass-card border-b border-surface-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo Zone */}
          <Link href="/" className="flex items-center gap-3 group flex-shrink-0">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-navy to-visionary flex items-center justify-center text-white shadow-md shadow-visionary/25 group-hover:scale-105 transition-transform">
              <Globe className="w-5 h-5 text-tealAccent" />
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-navy via-visionary to-tealAccent dark:from-white dark:to-tealAccent bg-clip-text text-transparent">
                VISIONARY
              </span>
              <span className="block text-[10px] uppercase tracking-wider font-bold text-tealAccent -mt-1">
                DNTU Platform
              </span>
            </div>
          </Link>

          {/* Centered Desktop Navigation - Clean grouped dropdowns (NO MORE 9 AWKWARD TEXT WRAPS) */}
          <nav className="hidden lg:flex items-center gap-1 xl:gap-2">
            {/* 1. Trang chủ */}
            <Link
              href="/"
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                pathname === "/"
                  ? "bg-visionary text-white shadow-sm"
                  : "text-navy dark:text-gray-200 hover:bg-visionary/10 dark:hover:bg-white/10"
              }`}
            >
              Trang chủ
            </Link>

            {/* 2. CLB DNTU */}
            <Link
              href="/about"
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                pathname === "/about"
                  ? "bg-visionary text-white shadow-sm"
                  : "text-navy dark:text-gray-200 hover:bg-visionary/10 dark:hover:bg-white/10"
              }`}
            >
              CLB DNTU
            </Link>

            {/* 3. Grouped Dropdowns: Học tập, Công nghệ, Cơ hội, Hoạt động */}
            {navGroups.map((group) => {
              const isGroupActive = group.items.some((item) => pathname.startsWith(item.href));
              const isOpen = openDropdown === group.id;

              return (
                <div key={group.id} className="relative">
                  <button
                    onClick={() => setOpenDropdown(isOpen ? null : group.id)}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors flex items-center gap-1 ${
                      isGroupActive
                        ? "bg-visionary/15 text-visionary dark:text-tealAccent"
                        : "text-navy dark:text-gray-200 hover:bg-visionary/10 dark:hover:bg-white/10"
                    }`}
                  >
                    <span>{group.title}</span>
                    <ChevronDown
                      className={`w-3.5 h-3.5 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
                    />
                  </button>

                  {/* Dropdown Menu */}
                  {isOpen && (
                    <div className="absolute top-full left-0 mt-2 w-72 p-2 rounded-2xl glass-card border border-surface-border shadow-xl shadow-navy/10 dark:shadow-black/40 animate-fadeIn z-50">
                      <div className="space-y-1">
                        {group.items.map((item) => {
                          const Icon = item.icon;
                          const isActive = pathname.startsWith(item.href);
                          return (
                            <Link
                              key={item.href}
                              href={item.href}
                              onClick={() => setOpenDropdown(null)}
                              className={`flex items-start gap-3 p-2.5 rounded-xl transition-all ${
                                isActive
                                  ? "bg-visionary text-white"
                                  : "hover:bg-navy/5 dark:hover:bg-white/5 text-navy dark:text-gray-200"
                              }`}
                            >
                              <div
                                className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5 ${
                                  isActive
                                    ? "bg-white/20 text-white"
                                    : "bg-visionary/10 text-visionary dark:bg-white/10 dark:text-tealAccent"
                                }`}
                              >
                                <Icon className="w-4 h-4" />
                              </div>
                              <div>
                                <div className="text-xs font-bold leading-tight">{item.name}</div>
                                <div
                                  className={`text-[10px] leading-tight mt-0.5 ${
                                    isActive ? "text-white/80" : "text-gray-400"
                                  }`}
                                >
                                  {item.desc}
                                </div>
                              </div>
                            </Link>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}

            {/* 4. Tin tức */}
            <Link
              href="/posts"
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
                pathname.startsWith("/posts")
                  ? "bg-visionary text-white shadow-sm"
                  : "text-navy dark:text-gray-200 hover:bg-visionary/10 dark:hover:bg-white/10"
              }`}
            >
              Tin tức
            </Link>
          </nav>

          {/* Right Action Zone: Theme Toggle + User Menu / Auth Buttons */}
          <div className="hidden sm:flex items-center gap-3">
            <button
              onClick={toggleTheme}
              aria-label="Chuyển chế độ sáng/tối"
              className="p-2 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-navy-light transition-colors"
            >
              {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-navy" />}
            </button>

            {user ? (
              <div className="relative">
                {/* User Trigger Button */}
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-surface-border hover:border-tealAccent/50 bg-navy/5 dark:bg-white/5 transition-all text-xs font-semibold text-navy dark:text-white"
                >
                  <div className="w-6 h-6 rounded-lg bg-visionary text-white flex items-center justify-center font-bold text-xs">
                    {user.fullName[0]}
                  </div>
                  <span className="max-w-[120px] truncate">{user.fullName}</span>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${roleBadge.style}`}
                  >
                    {roleBadge.label}
                  </span>
                  <ChevronDown className="w-3.5 h-3.5 text-gray-400" />
                </button>

                {/* User Menu Dropdown */}
                {userMenuOpen && (
                  <div className="absolute right-0 top-full mt-2 w-64 p-2 rounded-2xl glass-card border border-surface-border shadow-2xl shadow-navy/20 dark:shadow-black/50 animate-fadeIn z-50 space-y-1">
                    <div className="px-3 py-2 border-b border-surface-border">
                      <div className="text-xs font-bold text-navy dark:text-white truncate">
                        {user.fullName}
                      </div>
                      <div className="text-[10px] text-gray-400 truncate">{user.email}</div>
                      <div className="mt-1">
                        <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${roleBadge.style}`}>
                          {roleBadge.label}
                        </span>
                      </div>
                    </div>

                    {/* Dedicated Dashboard Routing based on Exact Role */}
                    {isAdmin && (
                      <Link
                        href="/dashboard/admin"
                        onClick={() => setUserMenuOpen(false)}
                        className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl"
                      >
                        <ShieldCheck className="w-4 h-4" />
                        <span>Admin Control Center</span>
                      </Link>
                    )}

                    {(isAdmin || isCommittee) && (
                      <Link
                        href="/dashboard/committee"
                        onClick={() => setUserMenuOpen(false)}
                        className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-amber-600 dark:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950/20 rounded-xl"
                      >
                        <Users className="w-4 h-4" />
                        <span>Ban Chủ Nhiệm Portal</span>
                      </Link>
                    )}

                    <Link
                      href="/dashboard"
                      onClick={() => setUserMenuOpen(false)}
                      className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-navy dark:text-gray-200 hover:bg-navy/5 dark:hover:bg-white/5 rounded-xl"
                    >
                      <GraduationCap className="w-4 h-4 text-tealAccent" />
                      <span>Bảng điều khiển Cá nhân</span>
                    </Link>

                    <div className="pt-1 border-t border-surface-border">
                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2 px-3 py-2 text-xs font-semibold text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        <span>Đăng xuất</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/auth/login"
                  className="px-3.5 py-1.5 text-xs font-bold text-navy dark:text-gray-200 hover:text-visionary transition-colors"
                >
                  Đăng nhập
                </Link>
                <Link
                  href="/auth/register"
                  className="px-4 py-1.5 text-xs font-bold text-white bg-visionary hover:bg-visionary-hover rounded-xl shadow-sm shadow-visionary/30 transition-all hover:scale-[1.02]"
                >
                  Đăng ký
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Trigger & Dark toggle */}
          <div className="flex items-center gap-2 lg:hidden">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-navy-light"
            >
              {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-navy" />}
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-navy-light"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer (Responsive for 320px - 1024px) */}
      {mobileMenuOpen && (
        <div className="lg:hidden glass-card border-b border-surface-border px-4 pt-3 pb-6 space-y-4 animate-fadeIn">
          {/* User Status Card in Mobile */}
          {user ? (
            <div className="p-3 rounded-2xl bg-navy/5 dark:bg-white/5 space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-navy dark:text-white">{user.fullName}</div>
                  <div className="text-[10px] text-gray-400">{user.email}</div>
                </div>
                <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${roleBadge.style}`}>
                  {roleBadge.label}
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5 pt-1">
                {isAdmin && (
                  <Link
                    href="/dashboard/admin"
                    className="px-2.5 py-1 rounded-lg bg-red-500/10 text-red-600 text-[11px] font-bold"
                  >
                    Admin Portal
                  </Link>
                )}
                {(isAdmin || isCommittee) && (
                  <Link
                    href="/dashboard/committee"
                    className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-600 text-[11px] font-bold"
                  >
                    BCN Portal
                  </Link>
                )}
                <Link
                  href="/dashboard"
                  className="px-2.5 py-1 rounded-lg bg-tealAccent/10 text-tealAccent text-[11px] font-bold"
                >
                  Bảng cá nhân
                </Link>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-2 pt-2">
              <Link
                href="/auth/login"
                className="py-2 text-center text-xs font-bold rounded-xl border border-surface-border text-navy dark:text-white"
              >
                Đăng nhập
              </Link>
              <Link
                href="/auth/register"
                className="py-2 text-center text-xs font-bold rounded-xl bg-visionary text-white shadow-sm"
              >
                Đăng ký
              </Link>
            </div>
          )}

          {/* Navigation Links Accordion */}
          <div className="space-y-1 text-xs font-semibold">
            <Link
              href="/"
              className="block px-3 py-2 rounded-xl text-navy dark:text-gray-200 hover:bg-navy/5 dark:hover:bg-white/5"
            >
              Trang chủ
            </Link>
            <Link
              href="/about"
              className="block px-3 py-2 rounded-xl text-navy dark:text-gray-200 hover:bg-navy/5 dark:hover:bg-white/5"
            >
              CLB DNTU
            </Link>

            {navGroups.map((group) => {
              const isExpanded = expandedMobileGroup === group.id;
              return (
                <div key={group.id} className="space-y-1">
                  <button
                    onClick={() => setExpandedMobileGroup(isExpanded ? null : group.id)}
                    className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-navy dark:text-gray-200 hover:bg-navy/5 dark:hover:bg-white/5"
                  >
                    <span>{group.title}</span>
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform ${isExpanded ? "rotate-180" : ""}`} />
                  </button>
                  {isExpanded && (
                    <div className="pl-4 space-y-1 border-l-2 border-tealAccent/30 ml-3">
                      {group.items.map((sub) => (
                        <Link
                          key={sub.href}
                          href={sub.href}
                          className="block px-3 py-1.5 text-xs text-gray-600 dark:text-gray-300 hover:text-visionary"
                        >
                          {sub.name}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}

            <Link
              href="/posts"
              className="block px-3 py-2 rounded-xl text-navy dark:text-gray-200 hover:bg-navy/5 dark:hover:bg-white/5"
            >
              Tin tức
            </Link>

            {user && (
              <button
                onClick={handleLogout}
                className="w-full text-left px-3 py-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-950/20 rounded-xl flex items-center gap-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Đăng xuất</span>
              </button>
            )}
          </div>
        </div>
      )}
    </header>
  );
}

"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Globe, Lock, Mail, ArrowRight, ShieldCheck, UserCheck } from "lucide-react";
import { api } from "../../../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const res = await api.login(email, password);
    setLoading(false);

    if (res.success && res.data) {
      if (res.data.user.roles.includes("Admin") || res.data.user.roles.includes("Committee")) {
        router.push("/dashboard/admin");
      } else {
        router.push("/dashboard");
      }
    } else {
      setError(res.message || "Email hoặc mật khẩu không chính xác.");
    }
  };

  const fillQuickAccount = (e: string, p: string) => {
    setEmail(e);
    setPassword(p);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full glass-card p-8 rounded-3xl border border-surface-border space-y-6 shadow-xl">
        <div className="text-center space-y-2">
          <div className="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-navy to-visionary items-center justify-center text-white shadow-md mb-2">
            <Globe className="w-6 h-6 text-tealAccent" />
          </div>
          <h1 className="text-2xl font-extrabold text-navy dark:text-white tracking-tight">
            Đăng nhập VISIONARY
          </h1>
          <p className="text-xs text-gray-500">
            Cổng quản lý hoạt động hội nhập & CLB Tiếng Anh DNTU
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 text-red-600 dark:text-red-400 text-xs font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-bold text-navy dark:text-gray-200">Email sinh viên / quản trị</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@visionary.dntu.edu.vn"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-navy dark:text-gray-200">Mật khẩu</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 hover:scale-[1.01] transition-all disabled:opacity-50"
          >
            {loading ? "Đang xác thực..." : "Đăng nhập"}
          </button>
        </form>

        {/* Quick Demo Credentials */}
        <div className="pt-4 border-t border-gray-100 dark:border-gray-800 space-y-2">
          <div className="text-[11px] font-bold text-gray-400 uppercase tracking-wider text-center">
            Tài khoản Thử nghiệm Nhanh:
          </div>
          <div className="grid grid-cols-2 gap-2 text-[11px]">
            <button
              type="button"
              onClick={() => fillQuickAccount("quachkhoaduc@visionary.dntu.edu.vn", "Visionary@2026")}
              className="p-2 rounded-lg bg-surface dark:bg-navy-light text-navy dark:text-white border border-surface-border hover:border-tealAccent transition-colors text-left"
            >
              <div className="font-bold text-tealAccent">Quách Khoa Đức</div>
              <div className="text-[10px] text-gray-400">Admin / Lead</div>
            </button>
            <button
              type="button"
              onClick={() => fillQuickAccount("vongocminhdat@visionary.dntu.edu.vn", "Visionary@2026")}
              className="p-2 rounded-lg bg-surface dark:bg-navy-light text-navy dark:text-white border border-surface-border hover:border-tealAccent transition-colors text-left"
            >
              <div className="font-bold text-visionary">Võ Ngọc Minh Đạt</div>
              <div className="text-[10px] text-gray-400">BCN CLB</div>
            </button>
          </div>
        </div>

        <div className="text-center text-xs text-gray-500">
          Chưa có tài khoản?{" "}
          <Link href="/auth/register" className="text-visionary dark:text-tealAccent font-bold hover:underline">
            Đăng ký sinh viên
          </Link>
        </div>
      </div>
    </div>
  );
}

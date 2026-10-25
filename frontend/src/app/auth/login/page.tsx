"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Globe, Lock, Mail, ArrowRight, ShieldCheck, UserCheck, AlertCircle } from "lucide-react";
import { api } from "../../../lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [googleLoading, setGoogleLoading] = useState(false);

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

  const handleGoogleLogin = async () => {
    setGoogleLoading(true);
    setError("");

    const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
    if (!clientId) {
      setError("Dịch vụ Google OAuth yêu cầu cấu hình GOOGLE_CLIENT_ID từ Google Cloud Console. Vui lòng xem hướng dẫn chi tiết tại docs/REQUIRED_ACCESS.md.");
      setGoogleLoading(false);
      return;
    }

    try {
      const redirectUri = encodeURIComponent(`${window.location.origin}/api/auth/callback/google`);
      const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=token%20id_token&scope=openid%20email%20profile&nonce=${Date.now()}`;
      window.location.href = googleAuthUrl;
    } catch (err: any) {
      setError(err?.message || "Lỗi khởi tạo đăng nhập Google.");
      setGoogleLoading(false);
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
          <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 text-amber-700 dark:text-amber-400 text-xs font-medium flex items-start gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>{error}</span>
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
            {loading ? "Đang xác thực..." : "Đăng nhập với Email"}
          </button>
        </form>

        {/* Google OAuth Button */}
        <div className="relative flex py-1 items-center">
          <div className="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
          <span className="flex-shrink mx-3 text-gray-400 text-[11px] uppercase tracking-wider">Hoặc</span>
          <div className="flex-grow border-t border-gray-200 dark:border-gray-800"></div>
        </div>

        <button
          type="button"
          onClick={handleGoogleLogin}
          disabled={googleLoading}
          className="w-full py-2.5 rounded-xl border border-surface-border bg-white dark:bg-navy hover:bg-gray-50 dark:hover:bg-navy-light text-navy dark:text-white text-xs font-semibold shadow-sm transition-all flex items-center justify-center gap-2 hover:scale-[1.01]"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
            />
          </svg>
          <span>Đăng nhập với Google DNTU</span>
        </button>

        {/* Collapsible Test Fixtures for Academic Evaluation */}
        <details className="pt-2 border-t border-gray-100 dark:border-gray-800 text-[11px] group">
          <summary className="font-semibold text-gray-400 hover:text-tealAccent cursor-pointer flex items-center justify-between list-none">
            <span>🧪 Tài khoản Kiểm định Học phần (TH71108)</span>
            <span className="text-[10px] text-gray-400 group-open:rotate-180 transition-transform">▼</span>
          </summary>
          <div className="mt-3 grid grid-cols-2 gap-2">
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
        </details>

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

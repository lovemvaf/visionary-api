"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Globe, User, Mail, Lock, GraduationCap, Building, ArrowRight } from "lucide-react";
import { api } from "../../../lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [studentId, setStudentId] = useState("");
  const [department, setDepartment] = useState("Công nghệ Thông tin");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password.length < 6) {
      setError("Mật khẩu phải có độ dài tối thiểu 6 ký tự để bảo đảm an toàn.");
      return;
    }

    setLoading(true);

    const res = await api.register({
      fullName: fullName.trim(),
      email: email.trim().toLowerCase(),
      password,
      studentId: studentId.trim(),
      department
    });
    setLoading(false);

    if (res.success && res.data) {
      router.push("/dashboard");
    } else {
      setError(res.message || "Đăng ký không thành công. Vui lòng kiểm tra lại thông tin.");
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full glass-card p-8 rounded-3xl border border-surface-border space-y-6 shadow-xl">
        <div className="text-center space-y-2">
          <div className="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-navy to-visionary items-center justify-center text-white shadow-md mb-2">
            <Globe className="w-6 h-6 text-tealAccent" />
          </div>
          <h1 className="text-2xl font-extrabold text-navy dark:text-white tracking-tight">
            Đăng ký Tài khoản Sinh viên
          </h1>
          <p className="text-xs text-gray-500">
            Tạo tài khoản để tham gia hoạt động CLB Tiếng Anh và học tập English for IT
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 text-red-600 dark:text-red-400 text-xs font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-3.5">
          <div className="space-y-1">
            <label className="text-xs font-bold text-navy dark:text-gray-200">Họ và tên đầy đủ</label>
            <div className="relative">
              <User className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Nguyễn Văn A"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-navy dark:text-gray-200">Email sinh viên</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@dntu.edu.vn"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Mã số sinh viên (MSSV)</label>
              <div className="relative">
                <GraduationCap className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={studentId}
                  onChange={(e) => setStudentId(e.target.value)}
                  placeholder="1923040001"
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Khoa / Ngành</label>
              <div className="relative">
                <Building className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                  placeholder="Công nghệ Thông tin"
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
                />
              </div>
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-bold text-navy dark:text-gray-200">Mật khẩu bảo mật</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Tối thiểu 6 ký tự"
                className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 hover:scale-[1.01] transition-all disabled:opacity-50 mt-2"
          >
            {loading ? "Đang xử lý đăng ký..." : "Hoàn tất đăng ký"}
          </button>
        </form>

        <div className="text-center text-xs text-gray-500">
          Đã có tài khoản?{" "}
          <Link href="/auth/login" className="text-visionary dark:text-tealAccent font-bold hover:underline">
            Đăng nhập ngay
          </Link>
        </div>
      </div>
    </div>
  );
}

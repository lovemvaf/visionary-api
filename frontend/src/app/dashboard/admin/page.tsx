"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Users,
  Calendar,
  Radio,
  Award,
  RefreshCw,
  ShieldCheck,
  Activity,
  Sparkles,
  Search,
  Database,
  FileText,
  AlertCircle,
  ExternalLink,
  CheckCircle2,
  Lock
} from "lucide-react";
import { api } from "../../../lib/api";
import {
  DashboardStats,
  UserListItem,
  ContentSourceItem,
  AuditLogItem
} from "../../../lib/types";

type AdminTab = "overview" | "users" | "sources" | "audit";

export default function AdminDashboardPage() {
  const router = useRouter();
  const [authStatus, setAuthStatus] = useState<"checking" | "authorized" | "unauthorized">("checking");
  const [activeTab, setActiveTab] = useState<AdminTab>("overview");
  
  // Data states
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [users, setUsers] = useState<UserListItem[]>([]);
  const [sources, setSources] = useState<ContentSourceItem[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  
  // Action states
  const [userSearch, setUserSearch] = useState("");
  const [actionMessage, setActionMessage] = useState("");
  const [syncingSourceId, setSyncingSourceId] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const statsRes = await api.getDashboardStats();
      if (statsRes.success && statsRes.data) {
        setStats(statsRes.data);
      }
    } catch {
      // Handled politely without crashing
    } finally {
      setLoading(false);
    }
  }, []);

  const loadUsers = useCallback(async (query: string = "") => {
    const res = await api.getUsers(query);
    if (res.success && res.data) {
      setUsers(res.data);
    }
  }, []);

  const loadSources = useCallback(async () => {
    const res = await api.getSources();
    if (res.success && res.data) {
      setSources(res.data);
    }
  }, []);

  const loadAuditLogs = useCallback(async () => {
    const res = await api.getAuditLogs();
    if (res.success && res.data) {
      setAuditLogs(res.data);
    }
  }, []);

  useEffect(() => {
    // Single centralized auth check on mount
    api.getMe().then((res) => {
      if (!res.success || !res.data) {
        router.push("/auth/login");
        return;
      }
      const isAdmin = res.data.roles.includes("Admin");
      const isCommittee = res.data.roles.includes("Committee");

      if (isAdmin) {
        setAuthStatus("authorized");
        loadData();
      } else if (isCommittee) {
        // Redirect Committee to dedicated BCN dashboard
        router.push("/dashboard/committee");
      } else {
        setAuthStatus("unauthorized");
      }
    });
  }, [router, loadData]);

  // Tab change handlers
  useEffect(() => {
    if (authStatus !== "authorized") return;
    if (activeTab === "users") loadUsers(userSearch);
    if (activeTab === "sources") loadSources();
    if (activeTab === "audit") loadAuditLogs();
  }, [activeTab, authStatus, loadUsers, loadSources, loadAuditLogs, userSearch]);

  const handleTriggerSource = async (id: string, name: string) => {
    setSyncingSourceId(id);
    setActionMessage(`Đang kích hoạt nạp dữ liệu từ nguồn: ${name}...`);
    const res = await api.triggerSource(id);
    setSyncingSourceId(null);
    if (res.success) {
      setActionMessage(`Thành công: ${res.data || res.message}`);
      loadSources();
      loadData();
    } else {
      setActionMessage(res.message || "Lỗi đồng bộ nguồn.");
    }
  };

  const handleToggleRole = async (user: UserListItem, roleName: string) => {
    const currentRoles = [...user.roles];
    const exists = currentRoles.includes(roleName);
    const newRoles = exists
      ? currentRoles.filter((r) => r !== roleName)
      : [...currentRoles, roleName];

    if (newRoles.length === 0) {
      setActionMessage("Người dùng phải có ít nhất một vai trò (mặc định Student).");
      return;
    }

    const res = await api.updateUserRoles(user.id, newRoles);
    if (res.success) {
      setActionMessage(`Đã cập nhật vai trò của ${user.fullName}`);
      loadUsers(userSearch);
    } else {
      setActionMessage(res.message || "Không thể cập nhật vai trò.");
    }
  };

  if (authStatus === "checking") {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-10 h-10 border-4 border-visionary border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-sm font-semibold text-gray-500">Đang xác thực quyền Quản trị viên...</p>
      </div>
    );
  }

  if (authStatus === "unauthorized") {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-red-100 dark:bg-red-950/40 text-red-600 flex items-center justify-center mx-auto">
          <Lock className="w-7 h-7" />
        </div>
        <h1 className="text-xl font-bold text-navy dark:text-white">Truy cập bị từ chối</h1>
        <p className="text-xs text-gray-500">
          Trang quản trị toàn quyền (Admin Control Center) chỉ dành cho Quản trị viên hệ thống.
        </p>
        <div className="pt-2">
          <Link
            href="/dashboard"
            className="px-4 py-2 text-xs font-bold rounded-xl bg-visionary text-white shadow-sm"
          >
            Quay lại Bảng điều khiển cá nhân
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-surface-border pb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="badge-teal inline-flex items-center gap-1 px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider">
              <ShieldCheck className="w-3.5 h-3.5" />
              Admin Control Center
            </span>
            <Link
              href="/dashboard/committee"
              className="text-[11px] text-tealAccent hover:underline font-semibold"
            >
              Chuyển sang BCN Portal →
            </Link>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-navy dark:text-white mt-1">
            Trung tâm Quản trị Toàn quyền VISIONARY
          </h1>
          <p className="text-xs text-gray-500 mt-0.5">
            Giám sát vận hành hệ sinh thái, phân quyền người dùng, tự động hóa dữ liệu và nhật ký kiểm toán
          </p>
        </div>

        {/* Global Refresh Action */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              loadData();
              if (activeTab === "users") loadUsers(userSearch);
              if (activeTab === "sources") loadSources();
              if (activeTab === "audit") loadAuditLogs();
            }}
            disabled={loading}
            className="px-4 py-2 rounded-xl glass-card text-navy dark:text-white text-xs font-bold hover:border-tealAccent flex items-center gap-1.5 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>{loading ? "Đang tải dữ liệu..." : "Làm mới"}</span>
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-3.5 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-xs text-tealAccent font-semibold flex items-center gap-2 animate-fadeIn">
          <Sparkles className="w-4 h-4 flex-shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-surface-border pb-2">
        <button
          onClick={() => setActiveTab("overview")}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === "overview"
              ? "bg-visionary text-white shadow-sm shadow-visionary/25"
              : "text-navy dark:text-gray-300 hover:bg-navy/5 dark:hover:bg-white/5"
          }`}
        >
          <Activity className="w-4 h-4" />
          <span>Tổng quan Hệ thống</span>
        </button>

        <button
          onClick={() => setActiveTab("users")}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === "users"
              ? "bg-visionary text-white shadow-sm shadow-visionary/25"
              : "text-navy dark:text-gray-300 hover:bg-navy/5 dark:hover:bg-white/5"
          }`}
        >
          <Users className="w-4 h-4" />
          <span>Quản lý Người dùng & Quyền</span>
        </button>

        <button
          onClick={() => setActiveTab("sources")}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === "sources"
              ? "bg-visionary text-white shadow-sm shadow-visionary/25"
              : "text-navy dark:text-gray-300 hover:bg-navy/5 dark:hover:bg-white/5"
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Nguồn Tự động hóa</span>
        </button>

        <button
          onClick={() => setActiveTab("audit")}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            activeTab === "audit"
              ? "bg-visionary text-white shadow-sm shadow-visionary/25"
              : "text-navy dark:text-gray-300 hover:bg-navy/5 dark:hover:bg-white/5"
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Nhật ký Hoạt động (Audit Logs)</span>
        </button>
      </div>

      {/* TAB 1: OVERVIEW */}
      {activeTab === "overview" && (
        <div className="space-y-8">
          {/* Metrics Grid - Real data with pulsing skeleton loader (NO HARDCODED NUMBERS) */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: "Tổng Người dùng", val: stats?.totalUsers, color: "border-visionary" },
              { label: "Thành viên CLB", val: stats?.totalMembers, color: "border-tealAccent" },
              { label: "Đơn chờ duyệt", val: stats?.pendingApplications, color: "border-amber-500" },
              { label: "Sự kiện", val: stats?.totalEvents, color: "border-visionary" },
              { label: "Tech Radar Repos", val: stats?.totalTechResources, color: "border-tealAccent" },
              { label: "Thành tích", val: stats?.totalAchievements, color: "border-purple-500" },
            ].map((card, i) => (
              <div key={i} className={`glass-card p-4 rounded-2xl text-center border-t-2 ${card.color}`}>
                {loading && !stats ? (
                  <div className="h-8 w-14 bg-slate-200 dark:bg-navy-light/60 rounded animate-pulse mx-auto mb-1" />
                ) : (
                  <div className="text-2xl font-extrabold text-navy dark:text-white">
                    {card.val !== undefined ? card.val : 0}
                  </div>
                )}
                <div className="text-[11px] text-gray-500 font-medium mt-0.5">{card.label}</div>
              </div>
            ))}
          </div>

          {/* Quick Platform Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass-card rounded-2xl p-5 space-y-3 border border-surface-border">
              <h3 className="text-xs font-bold uppercase tracking-wider text-tealAccent flex items-center gap-1.5">
                <Database className="w-4 h-4" />
                Dữ liệu Cơ hội & Việc làm
              </h3>
              <div className="flex items-center justify-between py-2 border-b border-surface-border">
                <span className="text-xs text-gray-600 dark:text-gray-300">Cuộc thi & Học bổng:</span>
                <span className="text-sm font-bold text-navy dark:text-white">
                  {stats ? stats.totalOpportunities : "—"}
                </span>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-surface-border">
                <span className="text-xs text-gray-600 dark:text-gray-300">Cơ hội Việc làm IT:</span>
                <span className="text-sm font-bold text-navy dark:text-white">
                  {stats ? stats.totalJobs : "—"}
                </span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="text-xs text-gray-600 dark:text-gray-300">Bài viết & Tin tức:</span>
                <span className="text-sm font-bold text-navy dark:text-white">
                  {stats ? stats.totalPosts : "—"}
                </span>
              </div>
            </div>

            <div className="glass-card rounded-2xl p-5 space-y-3 border border-surface-border md:col-span-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-visionary flex items-center gap-1.5">
                <Activity className="w-4 h-4" />
                Hoạt động Hệ thống Gần đây
              </h3>
              {loading && !stats ? (
                <div className="space-y-2">
                  <div className="h-10 bg-slate-200 dark:bg-navy-light/60 rounded-xl animate-pulse" />
                  <div className="h-10 bg-slate-200 dark:bg-navy-light/60 rounded-xl animate-pulse" />
                </div>
              ) : stats?.recentActivities && stats.recentActivities.length > 0 ? (
                <div className="space-y-2">
                  {stats.recentActivities.map((act, i) => (
                    <div
                      key={i}
                      className="p-2.5 rounded-xl bg-navy/5 dark:bg-white/5 flex items-center justify-between text-xs"
                    >
                      <div className="flex items-center gap-2">
                        <span className="badge-blue text-[10px] px-2 py-0.5 rounded font-bold font-mono">
                          {act.action}
                        </span>
                        <span className="text-navy dark:text-gray-200">{act.description}</span>
                        {act.userName && (
                          <span className="text-gray-400">by {act.userName}</span>
                        )}
                      </div>
                      <span className="text-[10px] text-gray-400">
                        {new Date(act.timestamp).toLocaleTimeString("vi-VN")}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-gray-500">Chưa ghi nhận hoạt động gần đây.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: USERS & ROLES */}
      {activeTab === "users" && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="relative w-full sm:w-80">
              <Search className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
              <input
                type="text"
                value={userSearch}
                onChange={(e) => {
                  setUserSearch(e.target.value);
                  loadUsers(e.target.value);
                }}
                placeholder="Tìm theo tên, email, MSSV..."
                className="w-full pl-9 pr-4 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>
            <div className="text-xs text-gray-500">
              Hiển thị {users.length} tài khoản trong hệ thống
            </div>
          </div>

          <div className="glass-card rounded-2xl border border-surface-border overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-navy/5 dark:bg-white/5 text-gray-500 uppercase tracking-wider font-semibold border-b border-surface-border">
                <tr>
                  <th className="px-4 py-3">Họ và tên</th>
                  <th className="px-4 py-3">Email & MSSV</th>
                  <th className="px-4 py-3">Trạng thái CLB</th>
                  <th className="px-4 py-3">Vai trò Hệ thống</th>
                  <th className="px-4 py-3 text-right">Phân quyền</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-navy/5 dark:hover:bg-white/5 transition-colors">
                    <td className="px-4 py-3.5 font-bold text-navy dark:text-white">
                      {u.fullName}
                    </td>
                    <td className="px-4 py-3.5 space-y-0.5">
                      <div className="text-gray-600 dark:text-gray-300 font-mono text-[11px]">{u.email}</div>
                      {u.studentId && (
                        <div className="text-[10px] text-gray-400">MSSV: {u.studentId} • {u.department || "DNTU"}</div>
                      )}
                    </td>
                    <td className="px-4 py-3.5">
                      {u.isMember ? (
                        <span className="badge-teal text-[10px] px-2 py-0.5 rounded-full font-bold">
                          {u.clubRole || "Thành viên CLB"}
                        </span>
                      ) : (
                        <span className="text-[10px] text-gray-400">Chưa gia nhập</span>
                      )}
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex flex-wrap gap-1">
                        {u.roles.map((r) => (
                          <span
                            key={r}
                            className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                              r === "Admin"
                                ? "bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-300"
                                : r === "Committee"
                                ? "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
                                : r === "Collaborator"
                                ? "bg-purple-100 text-purple-700 dark:bg-purple-950 dark:text-purple-300"
                                : "bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300"
                            }`}
                          >
                            {r}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-right space-x-1">
                      <button
                        onClick={() => handleToggleRole(u, "Committee")}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-bold border transition-colors ${
                          u.roles.includes("Committee")
                            ? "border-amber-500 text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-950/20"
                            : "border-surface-border text-gray-500 hover:border-amber-500 hover:text-amber-600"
                        }`}
                      >
                        {u.roles.includes("Committee") ? "Bỏ BCN" : "+ BCN"}
                      </button>
                      <button
                        onClick={() => handleToggleRole(u, "Admin")}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-bold border transition-colors ${
                          u.roles.includes("Admin")
                            ? "border-red-500 text-red-600 hover:bg-red-50 dark:hover:bg-red-950/20"
                            : "border-surface-border text-gray-500 hover:border-red-500 hover:text-red-600"
                        }`}
                      >
                        {u.roles.includes("Admin") ? "Bỏ Admin" : "+ Admin"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 3: AUTOMATION SOURCES */}
      {activeTab === "sources" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-navy dark:text-white flex items-center gap-2">
              <Database className="w-4 h-4 text-tealAccent" />
              <span>Nguồn Dữ liệu Tự động hóa Đang Đăng ký</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {sources.map((s) => (
              <div key={s.id} className="glass-card rounded-2xl p-5 border border-surface-border space-y-4">
                <div className="flex items-center justify-between">
                  <div className="badge-teal text-[10px] px-2 py-0.5 rounded font-bold font-mono">
                    {s.type}
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${s.isEnabled ? "bg-tealAccent/15 text-tealAccent" : "bg-gray-200 text-gray-600"}`}>
                    {s.isEnabled ? "Đang bật" : "Tạm ngắt"}
                  </span>
                </div>

                <div>
                  <h3 className="font-bold text-sm text-navy dark:text-white">{s.name}</h3>
                  <p className="text-[11px] text-gray-400 font-mono truncate mt-0.5">{s.endpointUrl}</p>
                </div>

                <div className="text-xs text-gray-500 space-y-1 pt-2 border-t border-surface-border">
                  <div className="flex justify-between">
                    <span>Chu kỳ chạy:</span>
                    <span className="font-semibold text-navy dark:text-white">{s.intervalMinutes} phút</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Lần chạy cuối:</span>
                    <span className="font-semibold text-navy dark:text-white">
                      {s.lastRunAt ? new Date(s.lastRunAt).toLocaleTimeString("vi-VN") : "Chưa chạy"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Trạng thái:</span>
                    <span className="font-semibold text-tealAccent">{s.lastStatus || "Sẵn sàng"}</span>
                  </div>
                </div>

                <button
                  onClick={() => handleTriggerSource(s.id, s.name)}
                  disabled={syncingSourceId === s.id}
                  className="w-full py-2 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-sm flex items-center justify-center gap-1.5 transition-all disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${syncingSourceId === s.id ? "animate-spin" : ""}`} />
                  <span>{syncingSourceId === s.id ? "Đang nạp dữ liệu..." : "Chạy nạp ngay"}</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: AUDIT LOGS */}
      {activeTab === "audit" && (
        <div className="space-y-4">
          <h2 className="text-sm font-bold text-navy dark:text-white flex items-center gap-2">
            <FileText className="w-4 h-4 text-tealAccent" />
            <span>50 Hoạt động Hệ thống Gần nhất (Audit Trail)</span>
          </h2>

          <div className="glass-card rounded-2xl border border-surface-border overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-navy/5 dark:bg-white/5 text-gray-500 uppercase tracking-wider font-semibold border-b border-surface-border">
                <tr>
                  <th className="px-4 py-3">Thời gian</th>
                  <th className="px-4 py-3">Hành động</th>
                  <th className="px-4 py-3">Tài nguyên</th>
                  <th className="px-4 py-3">Người thực hiện</th>
                  <th className="px-4 py-3">Địa chỉ IP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border font-mono text-[11px]">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-navy/5 dark:hover:bg-white/5">
                    <td className="px-4 py-2.5 text-gray-400">
                      {new Date(log.timestamp).toLocaleString("vi-VN")}
                    </td>
                    <td className="px-4 py-2.5 font-bold text-navy dark:text-white">
                      <span className="badge-blue px-2 py-0.5 rounded text-[10px]">
                        {log.action}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-gray-600 dark:text-gray-300">
                      {log.resource} {log.resourceId && `(${log.resourceId.slice(0, 8)}...)`}
                    </td>
                    <td className="px-4 py-2.5 font-sans font-semibold text-tealAccent">
                      {log.userName || "System"}
                    </td>
                    <td className="px-4 py-2.5 text-gray-400">
                      {log.ipAddress || "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

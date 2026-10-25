"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  Users,
  Calendar,
  BookOpen,
  Award,
  Radio,
  RefreshCw,
  CheckCircle,
  XCircle,
  Plus,
  ShieldCheck,
  Activity,
  Sparkles
} from "lucide-react";
import { api } from "../../../lib/api";
import { DashboardStats, MembershipApplicationItem, Department } from "../../../lib/types";

export default function AdminDashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [applications, setApplications] = useState<MembershipApplicationItem[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [actionMessage, setActionMessage] = useState("");
  const [syncing, setSyncing] = useState(false);

  // New Event Form State
  const [showEventForm, setShowEventForm] = useState(false);
  const [eventTitle, setEventTitle] = useState("");
  const [eventDesc, setEventDesc] = useState("");
  const [eventLoc, setEventLoc] = useState("");
  const [eventCap, setEventCap] = useState(100);
  const [eventLoading, setEventLoading] = useState(false);

  useEffect(() => {
    // Check permission
    api.getMe().then((res) => {
      if (!res.success || !res.data) {
        router.push("/auth/login");
        return;
      }
      const isManager = res.data.roles.includes("Admin") || res.data.roles.includes("Committee");
      if (!isManager) {
        router.push("/dashboard");
      }
    });

    loadData();
  }, [router]);

  const loadData = () => {
    api.getDashboardStats().then((res) => {
      if (res.success && res.data) setStats(res.data);
    });

    api.getApplications("Pending").then((res) => {
      if (res.success && res.data) setApplications(res.data);
    });

    api.getDepartments().then((res) => {
      if (res.success && res.data) setDepartments(res.data);
    });
  };

  const handleReview = async (id: string, isApproved: boolean) => {
    setActionMessage("Đang xử lý đơn...");
    const res = await api.reviewApplication(id, isApproved, isApproved ? "Thành viên" : undefined);
    if (res.success) {
      setActionMessage(isApproved ? "Đã duyệt và kết nạp thành viên!" : "Đã từ chối đơn đăng ký.");
      loadData();
    } else {
      setActionMessage(res.message || "Lỗi thao tác.");
    }
  };

  const handleTriggerSync = async () => {
    setSyncing(true);
    setActionMessage("Đang kích hoạt nạp dữ liệu từ GitHub & Hugging Face...");
    const res = await api.syncTechResources("All");
    setSyncing(false);
    if (res.success) {
      setActionMessage("Đã nạp và cập nhật dữ liệu tự động thành công!");
      loadData();
    } else {
      setActionMessage(res.message || "Lỗi đồng bộ nguồn.");
    }
  };

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    setEventLoading(true);
    const now = new Date();
    const startTime = new Date(now.getTime() + 7 * 86400000).toISOString();
    const endTime = new Date(now.getTime() + 7 * 86400000 + 3 * 3600000).toISOString();
    const regDeadline = new Date(now.getTime() + 6 * 86400000).toISOString();

    const res = await api.createEvent({
      title: eventTitle,
      description: eventDesc,
      location: eventLoc,
      startTime,
      endTime,
      registrationDeadline: regDeadline,
      maxCapacity: eventCap
    });
    setEventLoading(false);

    if (res.success) {
      setActionMessage("Tạo sự kiện mới thành công!");
      setShowEventForm(false);
      setEventTitle("");
      setEventDesc("");
      setEventLoc("");
      loadData();
    } else {
      setActionMessage(res.message || "Không thể tạo sự kiện.");
    }
  };

  const defaultStats: DashboardStats = {
    totalUsers: 8,
    totalMembers: 4,
    pendingApplications: applications.length,
    totalEvents: 2,
    totalPosts: 2,
    totalAchievements: 4,
    totalOpportunities: 4,
    totalJobs: 4,
    totalTechResources: 4,
    recentActivities: [
      { action: "LOGIN", description: "Đăng nhập hệ thống", timestamp: new Date().toISOString(), userName: "Quách Khoa Đức" }
    ]
  };

  const st = stats || defaultStats;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title & Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-surface-border pb-6">
        <div>
          <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
            Admin & BCN Portal
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-navy dark:text-white mt-1">
            Bảng Quản trị Hệ sinh thái VISIONARY
          </h1>
          <p className="text-xs text-gray-500 mt-0.5">
            Quản lý thành viên CLB, xét duyệt đơn, tổ chức sự kiện và giám sát tự động hóa
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEventForm(!showEventForm)}
            className="px-4 py-2 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Tạo Sự kiện mới</span>
          </button>

          <button
            onClick={handleTriggerSync}
            disabled={syncing}
            className="px-4 py-2 rounded-xl glass-card text-navy dark:text-white text-xs font-bold hover:border-tealAccent flex items-center gap-1.5 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${syncing ? "animate-spin" : ""}`} />
            <span>{syncing ? "Đang đồng bộ..." : "Nạp Dữ liệu Tự động"}</span>
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-3.5 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-xs text-tealAccent font-semibold flex items-center gap-2">
          <Sparkles className="w-4 h-4 flex-shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-visionary">
          <div className="text-2xl font-extrabold text-navy dark:text-white">{st.totalUsers}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Người dùng</div>
        </div>
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-tealAccent">
          <div className="text-2xl font-extrabold text-navy dark:text-white">{st.totalMembers}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Thành viên CLB</div>
        </div>
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-amber-500">
          <div className="text-2xl font-extrabold text-amber-500">{applications.length}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Đơn chờ duyệt</div>
        </div>
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-visionary">
          <div className="text-2xl font-extrabold text-navy dark:text-white">{st.totalEvents}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Sự kiện</div>
        </div>
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-tealAccent">
          <div className="text-2xl font-extrabold text-navy dark:text-white">{st.totalTechResources}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Mã nguồn Radar</div>
        </div>
        <div className="glass-card p-4 rounded-2xl text-center border-t-2 border-purple-500">
          <div className="text-2xl font-extrabold text-navy dark:text-white">{st.totalAchievements}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-0.5">Thành tích</div>
        </div>
      </div>

      {/* Create Event Form (Toggle) */}
      {showEventForm && (
        <div className="glass-card rounded-2xl p-6 border-l-4 border-visionary space-y-4">
          <h2 className="text-sm font-bold text-navy dark:text-white">Tạo Sự kiện Mới</h2>
          <form onSubmit={handleCreateEvent} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Tiêu đề sự kiện</label>
              <input
                type="text"
                required
                value={eventTitle}
                onChange={(e) => setEventTitle(e.target.value)}
                placeholder="Ví dụ: Workshop English for Full-Stack Developers 2026"
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Mô tả sự kiện</label>
              <textarea
                required
                rows={3}
                value={eventDesc}
                onChange={(e) => setEventDesc(e.target.value)}
                placeholder="Nội dung, diễn giả, lộ trình..."
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Địa điểm tổ chức</label>
              <input
                type="text"
                required
                value={eventLoc}
                onChange={(e) => setEventLoc(e.target.value)}
                placeholder="Hội trường Edison, DNTU"
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Số lượng tham gia tối đa</label>
              <input
                type="number"
                required
                value={eventCap}
                onChange={(e) => setEventCap(parseInt(e.target.value) || 100)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="sm:col-span-2 flex items-center justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setShowEventForm(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-gray-500 hover:bg-gray-100 dark:hover:bg-navy-light"
              >
                Hủy bỏ
              </button>
              <button
                type="submit"
                disabled={eventLoading}
                className="px-5 py-2 rounded-xl bg-visionary text-white text-xs font-bold shadow-md shadow-visionary/25 disabled:opacity-50"
              >
                {eventLoading ? "Đang tạo..." : "Xác nhận Đăng Sự kiện"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Pending Membership Applications Queue */}
      <section className="space-y-4">
        <h2 className="text-base font-bold text-navy dark:text-white flex items-center gap-2">
          <Users className="w-5 h-5 text-tealAccent" />
          <span>Hàng đợi Xét duyệt Đơn Gia nhập CLB ({applications.length})</span>
        </h2>

        {applications.length === 0 ? (
          <div className="glass-card rounded-2xl p-8 text-center text-xs text-gray-500">
            Hiện tại không có đơn đăng ký nào đang chờ xét duyệt.
          </div>
        ) : (
          <div className="space-y-3">
            {applications.map((app) => (
              <div
                key={app.id}
                className="glass-card rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 border"
              >
                <div className="space-y-1.5 max-w-2xl">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-navy dark:text-white">{app.applicantName}</span>
                    <span className="text-xs text-gray-400 font-mono">({app.applicantEmail})</span>
                    {app.studentId && (
                      <span className="badge-blue text-[10px] px-2 py-0.5 rounded-full font-bold">
                        MSSV: {app.studentId}
                      </span>
                    )}
                  </div>
                  <div className="text-xs text-tealAccent font-semibold">
                    Ban nguyện vọng: {app.preferredDepartmentName || "Chưa chọn"} • Trình độ: {app.englishProficiency || "Chưa ghi"}
                  </div>
                  <p className="text-xs text-gray-600 dark:text-gray-300 italic">
                    &quot;{app.selfIntroduction}&quot; — {app.motivation}
                  </p>
                </div>

                <div className="flex items-center gap-2 self-end md:self-auto flex-shrink-0">
                  <button
                    onClick={() => handleReview(app.id, false)}
                    className="px-3.5 py-1.5 rounded-xl border border-red-200 dark:border-red-900 text-red-600 dark:text-red-400 text-xs font-semibold hover:bg-red-50 dark:hover:bg-red-950/20 flex items-center gap-1"
                  >
                    <XCircle className="w-3.5 h-3.5" />
                    <span>Từ chối</span>
                  </button>

                  <button
                    onClick={() => handleReview(app.id, true)}
                    className="px-4 py-1.5 rounded-xl bg-tealAccent hover:bg-tealAccent-hover text-white text-xs font-bold shadow-sm flex items-center gap-1"
                  >
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>Duyệt kết nạp</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

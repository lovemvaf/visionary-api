"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Users,
  Calendar,
  CheckCircle,
  XCircle,
  Plus,
  Clock,
  Sparkles,
  BookOpen,
  Lock,
  RefreshCw,
  Award
} from "lucide-react";
import { api } from "../../../lib/api";
import {
  DashboardStats,
  MembershipApplicationItem,
  Department,
  EventItem
} from "../../../lib/types";

export default function CommitteeDashboardPage() {
  const router = useRouter();
  const [authStatus, setAuthStatus] = useState<"checking" | "authorized" | "unauthorized">("checking");
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [applications, setApplications] = useState<MembershipApplicationItem[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [actionMessage, setActionMessage] = useState("");

  // Create Event Form State with accurate date inputs
  const [showEventForm, setShowEventForm] = useState(false);
  const [eventTitle, setEventTitle] = useState("");
  const [eventDesc, setEventDesc] = useState("");
  const [eventLoc, setEventLoc] = useState("");
  const [eventCap, setEventCap] = useState(100);
  const [eventStartTime, setEventStartTime] = useState("");
  const [eventEndTime, setEventEndTime] = useState("");
  const [eventRegDeadline, setEventRegDeadline] = useState("");
  const [eventLoading, setEventLoading] = useState(false);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [statsRes, appsRes, deptsRes] = await Promise.all([
        api.getDashboardStats(),
        api.getApplications("Pending"),
        api.getDepartments()
      ]);

      if (statsRes.success && statsRes.data) setStats(statsRes.data);
      if (appsRes.success && appsRes.data) setApplications(appsRes.data);
      if (deptsRes.success && deptsRes.data) setDepartments(deptsRes.data);
    } catch {
      // Handled politely
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    api.getMe().then((res) => {
      if (!res.success || !res.data) {
        router.push("/auth/login");
        return;
      }
      const isCommitteeOrAdmin =
        res.data.roles.includes("Committee") || res.data.roles.includes("Admin");

      if (isCommitteeOrAdmin) {
        setAuthStatus("authorized");
        loadData();
      } else {
        setAuthStatus("unauthorized");
      }
    });

    // Default event dates: tomorrow at 08:00
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(8, 0, 0, 0);
    const endT = new Date(tomorrow);
    endT.setHours(11, 30, 0, 0);

    const pad = (n: number) => n.toString().padStart(2, "0");
    const fmt = (d: Date) =>
      `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;

    setEventStartTime(fmt(tomorrow));
    setEventEndTime(fmt(endT));
    setEventRegDeadline(fmt(tomorrow));
  }, [router, loadData]);

  const handleReview = async (id: string, isApproved: boolean) => {
    setActionMessage("Đang xử lý đơn đăng ký...");
    const res = await api.reviewApplication(id, isApproved, isApproved ? "Thành viên CLB" : undefined);
    if (res.success) {
      setActionMessage(isApproved ? "Đã phê duyệt và kết nạp thành viên mới!" : "Đã từ chối đơn đăng ký.");
      loadData();
    } else {
      setActionMessage(res.message || "Lỗi thao tác.");
    }
  };

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    setEventLoading(true);
    setActionMessage("");

    const res = await api.createEvent({
      title: eventTitle,
      description: eventDesc,
      location: eventLoc,
      startTime: new Date(eventStartTime).toISOString(),
      endTime: new Date(eventEndTime).toISOString(),
      registrationDeadline: new Date(eventRegDeadline).toISOString(),
      maxCapacity: eventCap
    });
    setEventLoading(false);

    if (res.success) {
      setActionMessage("Tổ chức sự kiện CLB mới thành công!");
      setShowEventForm(false);
      setEventTitle("");
      setEventDesc("");
      setEventLoc("");
      loadData();
    } else {
      setActionMessage(res.message || "Không thể tạo sự kiện.");
    }
  };

  if (authStatus === "checking") {
    return (
      <div className="max-w-7xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-10 h-10 border-4 border-visionary border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-sm font-semibold text-gray-500">Đang xác thực quyền Ban Chủ Nhiệm...</p>
      </div>
    );
  }

  if (authStatus === "unauthorized") {
    return (
      <div className="max-w-xl mx-auto px-4 py-24 text-center space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-amber-100 dark:bg-amber-950/40 text-amber-600 flex items-center justify-center mx-auto">
          <Lock className="w-7 h-7" />
        </div>
        <h1 className="text-xl font-bold text-navy dark:text-white">Khu vực Ban Chủ Nhiệm</h1>
        <p className="text-xs text-gray-500">
          Trang điều hành này chỉ dành cho Ban Chủ Nhiệm CLB Tiếng Anh DNTU và cán bộ phụ trách.
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
      {/* Title & Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-surface-border pb-6">
        <div>
          <div className="badge-teal inline-block px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider">
            Ban Chủ Nhiệm Portal
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-navy dark:text-white mt-1">
            Điều Hành CLB Tiếng Anh DNTU
          </h1>
          <p className="text-xs text-gray-500 mt-0.5">
            Quản lý thành viên, xét duyệt đơn đăng ký, tổ chức workshop và điều phối hoạt động
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowEventForm(!showEventForm)}
            className="px-4 py-2 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>{showEventForm ? "Đóng Form" : "Tạo Sự kiện CLB"}</span>
          </button>

          <button
            onClick={loadData}
            disabled={loading}
            className="px-4 py-2 rounded-xl glass-card text-navy dark:text-white text-xs font-bold hover:border-tealAccent flex items-center gap-1.5 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Làm mới</span>
          </button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-3.5 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-xs text-tealAccent font-semibold flex items-center gap-2 animate-fadeIn">
          <Sparkles className="w-4 h-4 flex-shrink-0" />
          <span>{actionMessage}</span>
        </div>
      )}

      {/* Real Metrics Grid - Pulsing skeleton on loading, zero hardcoded numbers */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: "Thành viên CLB", val: stats?.totalMembers, color: "border-tealAccent" },
          { label: "Đơn chờ duyệt", val: applications.length, color: "border-amber-500" },
          { label: "Sự kiện CLB", val: stats?.totalEvents, color: "border-visionary" },
          { label: "Ban Chuyên môn", val: departments.length, color: "border-purple-500" },
        ].map((card, i) => (
          <div key={i} className={`glass-card p-5 rounded-2xl text-center border-t-2 ${card.color}`}>
            {loading && !stats ? (
              <div className="h-8 w-14 bg-slate-200 dark:bg-navy-light/60 rounded animate-pulse mx-auto mb-1" />
            ) : (
              <div className="text-3xl font-extrabold text-navy dark:text-white">
                {card.val !== undefined ? card.val : 0}
              </div>
            )}
            <div className="text-xs text-gray-500 font-medium mt-1">{card.label}</div>
          </div>
        ))}
      </div>

      {/* Create Event Form (Toggle) */}
      {showEventForm && (
        <div className="glass-card rounded-2xl p-6 border-l-4 border-visionary space-y-4 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-surface-border pb-3">
            <h2 className="text-sm font-bold text-navy dark:text-white flex items-center gap-2">
              <Calendar className="w-4 h-4 text-visionary" />
              <span>Tổ chức Sự kiện / Workshop CLB Mới</span>
            </h2>
            <button
              onClick={() => setShowEventForm(false)}
              className="text-xs text-gray-400 hover:text-gray-600"
            >
              Đóng
            </button>
          </div>

          <form onSubmit={handleCreateEvent} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Tiêu đề sự kiện</label>
              <input
                type="text"
                required
                value={eventTitle}
                onChange={(e) => setEventTitle(e.target.value)}
                placeholder="Ví dụ: Workshop English for Software Engineering & Tech Interviews"
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
                placeholder="Nội dung chi tiết, mục tiêu, lộ trình và diễn giả..."
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
                placeholder="Hội trường Edison / Phòng Lab A3.02"
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Số lượng chỗ tối đa</label>
              <input
                type="number"
                required
                min={10}
                max={500}
                value={eventCap}
                onChange={(e) => setEventCap(parseInt(e.target.value) || 100)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Thời gian bắt đầu</label>
              <input
                type="datetime-local"
                required
                value={eventStartTime}
                onChange={(e) => setEventStartTime(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none font-mono"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Thời gian kết thúc</label>
              <input
                type="datetime-local"
                required
                value={eventEndTime}
                onChange={(e) => setEventEndTime(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none font-mono"
              />
            </div>

            <div className="space-y-1 sm:col-span-2">
              <label className="text-xs font-bold text-navy dark:text-gray-200">Hạn chót đăng ký</label>
              <input
                type="datetime-local"
                required
                value={eventRegDeadline}
                onChange={(e) => setEventRegDeadline(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none font-mono"
              />
            </div>

            <div className="sm:col-span-2 flex items-center justify-end gap-2 pt-2 border-t border-surface-border">
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
                {eventLoading ? "Đang xuất bản..." : "Xác nhận Xuất bản Sự kiện"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Pending Membership Applications Queue */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-navy dark:text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-tealAccent" />
            <span>Đơn Xin Gia Nhập Chờ Duyệt ({applications.length})</span>
          </h2>
          <span className="text-xs text-gray-500">
            Duyệt kết nạp thành viên chính thức và gán ban chuyên môn
          </span>
        </div>

        {applications.length === 0 ? (
          <div className="glass-card rounded-2xl p-8 text-center text-xs text-gray-500">
            Hiện tại không có đơn đăng ký nào đang chờ xét duyệt.
          </div>
        ) : (
          <div className="space-y-3">
            {applications.map((app) => (
              <div
                key={app.id}
                className="glass-card rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 border border-surface-border hover:border-tealAccent/40 transition-all"
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

      {/* Departments Overview */}
      <section className="space-y-4">
        <h2 className="text-base font-bold text-navy dark:text-white flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-visionary" />
          <span>Cơ cấu Các Ban Chuyên môn CLB</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {departments.map((d) => (
            <div key={d.id} className="glass-card rounded-2xl p-5 border border-surface-border space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="font-bold text-sm text-navy dark:text-white">{d.name}</h3>
                <span className="badge-teal text-[10px] px-2 py-0.5 rounded-full font-bold">
                  {d.memberCount} thành viên
                </span>
              </div>
              <p className="text-xs text-gray-500 line-clamp-3">{d.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

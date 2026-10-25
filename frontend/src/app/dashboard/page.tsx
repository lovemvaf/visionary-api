"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { User, Calendar, Award, QrCode, BookOpen, Send, CheckCircle, Clock } from "lucide-react";
import { api } from "../../lib/api";
import { UserProfile, EventItem, Department } from "../../lib/types";

export default function StudentDashboardPage() {
  const router = useRouter();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [events, setEvents] = useState<EventItem[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);

  // Application form state
  const [prefDept, setPrefDept] = useState("");
  const [selfIntro, setSelfIntro] = useState("");
  const [motivation, setMotivation] = useState("");
  const [englishLevel, setEnglishLevel] = useState("");
  const [appMessage, setAppMessage] = useState("");
  const [appLoading, setAppLoading] = useState(false);

  useEffect(() => {
    api.getMe().then((res) => {
      if (res.success && res.data) {
        setProfile(res.data);
      } else {
        router.push("/auth/login");
      }
    });

    api.getMyEvents().then((res) => {
      if (res.success && res.data) {
        setEvents(res.data);
      }
    });

    api.getDepartments().then((res) => {
      if (res.success && res.data) {
        setDepartments(res.data);
      }
    });
  }, [router]);

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault();
    setAppLoading(true);
    setAppMessage("");

    const res = await api.applyMembership({
      preferredDepartmentId: prefDept || undefined,
      selfIntroduction: selfIntro,
      motivation: motivation,
      englishProficiency: englishLevel
    });
    setAppLoading(false);

    if (res.success) {
      setAppMessage("Nộp đơn đăng ký gia nhập CLB thành công! Ban Chủ Nhiệm sẽ duyệt trong thời gian sớm nhất.");
      setSelfIntro("");
      setMotivation("");
    } else {
      setAppMessage(res.message || "Không thể gửi đơn đăng ký.");
    }
  };

  if (!profile) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center text-sm text-gray-500">
        Đang tải thông tin bảng điều khiển...
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Welcome Banner */}
      <div className="glass-card rounded-3xl p-6 lg:p-8 border border-surface-border flex flex-col sm:flex-row items-center justify-between gap-6 bg-gradient-to-r from-navy/5 via-visionary/5 to-tealAccent/5">
        <div className="flex items-center gap-4 text-center sm:text-left">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-navy to-visionary flex items-center justify-center text-white text-2xl font-bold shadow-md">
            {profile.fullName[0]}
          </div>
          <div>
            <div className="flex items-center gap-2 justify-center sm:justify-start">
              <h1 className="text-2xl font-bold text-navy dark:text-white">
                Chào mừng, {profile.fullName}!
              </h1>
              {profile.isMember && (
                <span className="badge-teal text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  {profile.clubRole || "Thành viên CLB"}
                </span>
              )}
            </div>
            <p className="text-xs text-gray-500 mt-0.5">
              {profile.department || "Sinh viên DNTU"} {profile.studentId && `• MSSV: ${profile.studentId}`}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {profile.roles.map((r) => (
            <span key={r} className="badge-blue text-[11px] px-2.5 py-1 rounded-lg font-bold">
              {r}
            </span>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Registered Events */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-navy dark:text-white flex items-center gap-2">
              <Calendar className="w-5 h-5 text-tealAccent" />
              <span>Sự kiện đã đăng ký ({events.length})</span>
            </h2>
          </div>

          {events.length === 0 ? (
            <div className="glass-card rounded-2xl p-8 text-center space-y-3">
              <Calendar className="w-10 h-10 text-gray-400 mx-auto" />
              <p className="text-xs text-gray-500">Bạn chưa đăng ký sự kiện nào.</p>
              <a
                href="/events"
                className="inline-block px-4 py-2 rounded-xl bg-visionary text-white text-xs font-semibold shadow-sm"
              >
                Khám phá sự kiện sắp tới
              </a>
            </div>
          ) : (
            <div className="space-y-4">
              {events.map((ev) => (
                <div key={ev.id} className="glass-card rounded-2xl p-5 border-l-4 border-tealAccent flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="space-y-1 text-center sm:text-left">
                    <h3 className="text-sm font-bold text-navy dark:text-white">{ev.title}</h3>
                    <div className="text-xs text-gray-500 flex items-center gap-2 justify-center sm:justify-start">
                      <span>{new Date(ev.startTime).toLocaleDateString("vi-VN")}</span>
                      <span>•</span>
                      <span>{ev.location}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    {ev.isCheckedInByCurrentUser ? (
                      <span className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 text-xs font-bold flex items-center gap-1">
                        <CheckCircle className="w-3.5 h-3.5" />
                        <span>Đã tham dự</span>
                      </span>
                    ) : (
                      <div className="text-center p-2 rounded-lg bg-surface dark:bg-navy-light text-[11px] font-mono font-bold text-tealAccent">
                        Mã: {ev.qrCheckInCode || "CHECKIN-OK"}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Membership Application */}
        <div className="space-y-6">
          <h2 className="text-lg font-bold text-navy dark:text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-visionary" />
            <span>CLB Tiếng Anh DNTU</span>
          </h2>

          <div className="glass-card rounded-2xl p-6 border space-y-4">
            {profile.isMember ? (
              <div className="space-y-3 text-center py-4">
                <CheckCircle className="w-12 h-12 text-tealAccent mx-auto" />
                <h3 className="text-sm font-bold text-navy dark:text-white">
                  Bạn là Thành viên Chính thức
                </h3>
                <p className="text-xs text-gray-500">
                  Vai trò: <strong>{profile.clubRole || "Thành viên"}</strong>
                </p>
                <div className="text-[11px] text-tealAccent font-semibold">
                  Tích cực tham gia các buổi sinh hoạt chuyên đề để nhận vinh danh tại Bảng vàng Thành tích!
                </div>
              </div>
            ) : (
              <form onSubmit={handleApply} className="space-y-3.5">
                <div className="space-y-1">
                  <h3 className="text-xs font-bold text-navy dark:text-white">
                    Đăng ký Gia nhập CLB Tiếng Anh
                  </h3>
                  <p className="text-[11px] text-gray-500">
                    Nộp đơn để sinh hoạt chuyên ban và tham gia các dự án hội nhập.
                  </p>
                </div>

                {appMessage && (
                  <div className="p-2.5 rounded-lg bg-tealAccent/10 text-tealAccent text-xs font-semibold">
                    {appMessage}
                  </div>
                )}

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-gray-700 dark:text-gray-300">Ban chuyên môn mong muốn</label>
                  <select
                    value={prefDept}
                    onChange={(e) => setPrefDept(e.target.value)}
                    className="w-full px-3 py-1.5 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
                  >
                    <option value="">Chọn ban chuyên môn</option>
                    {departments.map((d) => (
                      <option key={d.id} value={d.id}>{d.name}</option>
                    ))}
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-gray-700 dark:text-gray-300">Trình độ tiếng Anh hiện tại</label>
                  <input
                    type="text"
                    value={englishLevel}
                    onChange={(e) => setEnglishLevel(e.target.value)}
                    placeholder="TOEIC 650, IELTS 6.0, Giao tiếp cơ bản..."
                    className="w-full px-3 py-1.5 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-gray-700 dark:text-gray-300">Giới thiệu bản thân</label>
                  <textarea
                    required
                    rows={2}
                    value={selfIntro}
                    onChange={(e) => setSelfIntro(e.target.value)}
                    placeholder="Sở thích, định hướng nghề nghiệp..."
                    className="w-full px-3 py-1.5 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-gray-700 dark:text-gray-300">Mục tiêu khi tham gia CLB</label>
                  <textarea
                    required
                    rows={2}
                    value={motivation}
                    onChange={(e) => setMotivation(e.target.value)}
                    placeholder="Em muốn rèn luyện kỹ năng gì..."
                    className="w-full px-3 py-1.5 text-xs rounded-xl border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
                  />
                </div>

                <button
                  type="submit"
                  disabled={appLoading}
                  className="w-full py-2 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 transition-all flex items-center justify-center gap-1.5 disabled:opacity-50"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>{appLoading ? "Đang gửi..." : "Gửi đơn đăng ký"}</span>
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

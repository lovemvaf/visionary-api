"use client";

import React, { useState, useEffect } from "react";
import { Award, Calendar, ExternalLink, ShieldCheck, User, AlertCircle, RotateCcw, Medal } from "lucide-react";
import { api } from "../../lib/api";
import { AchievementItem } from "../../lib/types";

export default function AchievementsPage() {
  const [achievements, setAchievements] = useState<AchievementItem[]>([]);
  const [status, setStatus] = useState<"loading" | "success" | "empty" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");

  const fetchAchievements = () => {
    setStatus("loading");
    setErrorMessage("");

    api.getAchievements()
      .then((res) => {
        if (res.success && res.data) {
          const verified = res.data.filter((a) => a.isVerified);
          setAchievements(verified);
          if (verified.length === 0) {
            setStatus("empty");
          } else {
            setStatus("success");
          }
        } else {
          setAchievements([]);
          setStatus("error");
          setErrorMessage(res.message || "Không thể tải bảng vàng thành tích.");
        }
      })
      .catch((err) => {
        setAchievements([]);
        setStatus("error");
        setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
      });
  };

  useEffect(() => {
    fetchAchievements();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Hall of Achievement
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Bảng vàng Vinh danh Thành tích
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Tôn vinh những cá nhân và tập thể sinh viên DNTU có thành tích xuất sắc trong học thuật, giải thưởng công nghệ, chứng chỉ ngoại ngữ và hoạt động hội nhập toàn cầu đã qua kiểm chứng minh chứng.
        </p>
      </div>

      {/* 1. LOADING */}
      {status === "loading" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="glass-card rounded-2xl p-6 space-y-4 animate-pulse">
              <div className="h-5 w-1/3 bg-gray-200 dark:bg-gray-800 rounded-full" />
              <div className="h-6 w-3/4 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-4 w-full bg-gray-200 dark:bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 max-w-md mx-auto border border-red-200 dark:border-red-900/50">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải bảng thành tích</h3>
          <p className="text-xs text-gray-500">{errorMessage}</p>
          <button
            onClick={fetchAchievements}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-visionary text-white text-xs font-semibold"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Thử lại</span>
          </button>
        </div>
      )}

      {/* 3. EMPTY: Authentic Empty State - No Fake Person Awards */}
      {status === "empty" && (
        <div className="glass-card rounded-3xl p-16 text-center space-y-5 max-w-lg mx-auto border border-surface-border shadow-sm">
          <div className="w-16 h-16 rounded-2xl bg-tealAccent/10 text-tealAccent flex items-center justify-center mx-auto">
            <Medal className="w-8 h-8" />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-navy dark:text-white">
              Chưa có thành tích công bố
            </h3>
            <p className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
              Hệ thống hiện chưa có bản ghi thành tích nào được phê duyệt minh chứng chính thức. Sau khi các giải thưởng nghiên cứu, chứng chỉ ngoại ngữ và thành tích thi đấu được Hội đồng cố vấn thẩm định, danh sách vinh danh sẽ hiển thị công khai tại đây.
            </p>
          </div>
          <div className="pt-2 text-[11px] text-gray-400 italic">
            Quy trình xác minh tuân thủ tiêu chuẩn minh bạch của Nhà trường và CLB Tiếng Anh DNTU.
          </div>
        </div>
      )}

      {/* 4. SUCCESS: Verified Authentic Achievements Only */}
      {status === "success" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {achievements.map((item) => (
            <div
              key={item.id}
              className="glass-card rounded-2xl p-6 border-l-4 border-tealAccent flex flex-col justify-between hover:shadow-lg transition-all"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="badge-teal text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                    {item.categoryName}
                  </span>
                  <div className="flex items-center gap-1 text-[11px] text-tealAccent font-semibold">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>Đã thẩm định minh chứng</span>
                  </div>
                </div>

                <div className="space-y-1">
                  <h3 className="text-base font-bold text-navy dark:text-white">
                    {item.title}
                  </h3>
                  <div className="flex items-center gap-2 text-xs text-gray-500">
                    <User className="w-3.5 h-3.5 text-visionary" />
                    <span>
                      <strong>{item.recipientName}</strong>
                      {item.studentId && ` • MSSV: ${item.studentId}`}
                      {item.department && ` • ${item.department}`}
                    </span>
                  </div>
                </div>

                <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                  {item.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between text-xs text-gray-500">
                <div className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-tealAccent" />
                  <span>{new Date(item.awardedDate).toLocaleDateString("vi-VN")}</span>
                </div>

                {item.evidenceUrl && (
                  <a
                    href={item.evidenceUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1"
                  >
                    <span>Xem minh chứng</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

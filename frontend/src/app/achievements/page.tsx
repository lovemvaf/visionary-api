"use client";

import React, { useState, useEffect } from "react";
import { Award, Calendar, ExternalLink, ShieldCheck, User } from "lucide-react";
import { api } from "../../lib/api";
import { AchievementItem } from "../../lib/types";

export default function AchievementsPage() {
  const [achievements, setAchievements] = useState<AchievementItem[]>([]);

  const fallbackAchievements: AchievementItem[] = [
    {
      id: "1",
      categoryId: "cat1",
      categoryName: "Academic & Tech Excellence",
      recipientUserId: "u1",
      recipientName: "Quách Khoa Đức",
      studentId: "1923040025",
      department: "Khoa CNTT",
      title: "Giải Nhất Cuộc thi Sáng tạo Khoa học Công nghệ Sinh viên DNTU 2026",
      description: "Nghiên cứu và phát triển giải pháp Trí tuệ Nhân tạo ứng dụng trong giám sát và dự báo thời gian thực.",
      awardedDate: "2026-05-15",
      evidenceUrl: "https://dntu.edu.vn",
      isVerified: true
    },
    {
      id: "2",
      categoryId: "cat2",
      categoryName: "English Achievement",
      recipientUserId: "u2",
      recipientName: "Võ Ngọc Minh Đạt",
      department: "Khoa CNTT",
      title: "Chứng chỉ Ngoại ngữ Quốc tế TOEIC 850 Điểm",
      description: "Đạt thành tích xuất sắc trong kỳ thi chuẩn hóa năng lực tiếng Anh quốc tế.",
      awardedDate: "2026-03-20",
      isVerified: true
    },
    {
      id: "3",
      categoryId: "cat3",
      categoryName: "Global Engagement",
      recipientUserId: "u3",
      recipientName: "Hồ Đoàng Nguyên Khang",
      department: "Khoa CNTT",
      title: "Đại biểu Sinh viên Giao lưu Văn hóa & Công nghệ Thanh niên ASEAN 2026",
      description: "Đại diện sinh viên tham gia đoàn giao lưu thanh niên quốc tế tại Singapore & Malaysia.",
      awardedDate: "2026-07-10",
      isVerified: true
    },
    {
      id: "4",
      categoryId: "cat4",
      categoryName: "Technology & Innovation",
      recipientUserId: "u4",
      recipientName: "Đào Trí Khang",
      department: "Khoa CNTT",
      title: "Top 10 Chung kết Cuộc thi Lập trình Di động Quốc gia",
      description: "Xây dựng ứng dụng di động bản địa phục vụ kết nối học tập và nâng cao năng lực ngoại ngữ.",
      awardedDate: "2026-04-12",
      isVerified: true
    }
  ];

  useEffect(() => {
    api.getAchievements()
      .then((res) => {
        if (res.success && res.data?.length) {
          setAchievements(res.data);
        } else {
          setAchievements(fallbackAchievements);
        }
      })
      .catch(() => setAchievements(fallbackAchievements));
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
          Tôn vinh những cá nhân và tập thể sinh viên DNTU có thành tích xuất sắc trong học thuật, giải thưởng công nghệ, chứng chỉ ngoại ngữ và hoạt động hội nhập toàn cầu đã qua kiểm chứng.
        </p>
      </div>

      {/* Grid */}
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
                <span className="text-xs text-gray-500 font-medium flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-tealAccent" />
                  {new Date(item.awardedDate).toLocaleDateString("vi-VN")}
                </span>
              </div>

              <div>
                <h3 className="text-lg font-bold text-navy dark:text-white">
                  {item.title}
                </h3>
                <div className="flex items-center gap-2 text-xs text-visionary dark:text-tealAccent font-semibold mt-1">
                  <User className="w-3.5 h-3.5" />
                  <span>{item.recipientName}</span>
                  {item.studentId && <span>(MSSV: {item.studentId})</span>}
                  {item.department && <span>• {item.department}</span>}
                </div>
              </div>

              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed bg-surface dark:bg-navy-light p-3 rounded-xl">
                {item.description}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs">
              <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-semibold">
                <ShieldCheck className="w-4 h-4" />
                <span>Thành tích Đã kiểm chứng (Verified)</span>
              </div>

              {item.evidenceUrl && (
                <a
                  href={item.evidenceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-visionary hover:underline flex items-center gap-1 font-medium"
                >
                  <span>Minh chứng</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

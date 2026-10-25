"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Calendar, MapPin, Users, QrCode, CheckCircle, Clock } from "lucide-react";
import { api } from "../../../lib/api";
import { EventItem } from "../../../lib/types";

export default function EventDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [event, setEvent] = useState<EventItem | null>(null);
  const [registered, setRegistered] = useState(false);
  const [message, setMessage] = useState("");

  const defaultEvent: EventItem = {
    id: "ev1",
    title: "VISIONARY Tech & English Talk 2026: Lộ trình làm chủ AI và Hội nhập Toàn cầu",
    slug: slug || "visionary-tech-english-talk-2026",
    description: `Buổi tọa đàm chuyên sâu về cách kết hợp năng lực tiếng Anh chuyên ngành với các công nghệ AI hiện đại (LLMs, RAG, Web API) để tự tin ứng tuyển các tập đoàn công nghệ đa quốc gia.

Nội dung chương trình:
1. Tổng quan thị trường công nghệ và xu hướng hội nhập quốc tế của kỹ sư phần mềm Việt Nam.
2. Phương pháp tiếp cận tiếng Anh chuyên ngành: Đọc tài liệu, viết RFC, giao tiếp qua Slack/GitHub PR và phỏng vấn trực tiếp.
3. Live Demo: Xây dựng hệ sinh thái một Web API phục vụ đồng thời Web Next.js, Desktop C# và Android Java.
4. Giao lưu và hỏi đáp trực tiếp cùng các khách mời và Ban Chủ Nhiệm CLB Tiếng Anh DNTU.`,
    location: "Hội trường Edison, Trường Đại học Công nghệ Đồng Nai & Online MS Teams",
    startTime: new Date(Date.now() + 7 * 86400000).toISOString(),
    endTime: new Date(Date.now() + 7 * 86400000 + 3 * 3600000).toISOString(),
    registrationDeadline: new Date(Date.now() + 6 * 86400000).toISOString(),
    maxCapacity: 150,
    currentRegistrationsCount: 42,
    status: "Published",
    isRegisteredByCurrentUser: false,
    isCheckedInByCurrentUser: false,
    qrCheckInCode: "VIS-QR-TALK2026-CHECKIN"
  };

  useEffect(() => {
    if (slug) {
      api.getEventBySlug(slug).then((res) => {
        if (res.success && res.data) {
          setEvent(res.data);
          setRegistered(res.data.isRegisteredByCurrentUser);
        }
      });
    }
  }, [slug]);

  const ev = event || defaultEvent;

  const handleRegister = async () => {
    const res = await api.registerEvent(ev.id);
    if (res.success) {
      setRegistered(true);
      setMessage("Đăng ký thành công! Vui lòng lưu lại mã QR check-in dưới đây để điểm danh tại sự kiện.");
    } else {
      setMessage(res.message || "Vui lòng đăng nhập tài khoản sinh viên trước khi đăng ký.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      <Link
        href="/events"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-visionary dark:text-tealAccent hover:underline"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Quay lại lịch sự kiện</span>
      </Link>

      <div className="space-y-4">
        <span className="badge-teal text-xs px-3 py-1 rounded-full font-bold">
          {ev.status}
        </span>
        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-navy dark:text-white leading-tight">
          {ev.title}
        </h1>

        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500 pt-2">
          <div className="flex items-center gap-1.5">
            <Clock className="w-4 h-4 text-tealAccent" />
            <span>
              {new Date(ev.startTime).toLocaleString("vi-VN")} - {new Date(ev.endTime).toLocaleTimeString("vi-VN")}
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <MapPin className="w-4 h-4 text-visionary" />
            <span>{ev.location}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Users className="w-4 h-4 text-tealAccent" />
            <span>{ev.currentRegistrationsCount} / {ev.maxCapacity} người tham gia</span>
          </div>
        </div>
      </div>

      {message && (
        <div className="p-4 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-xs text-tealAccent font-semibold">
          {message}
        </div>
      )}

      {/* Main Content */}
      <div className="glass-card rounded-2xl p-8 space-y-6">
        <h2 className="text-lg font-bold text-navy dark:text-white">Chi tiết Sự kiện</h2>
        <div className="prose dark:prose-invert max-w-none text-xs sm:text-sm text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-line">
          {ev.description}
        </div>

        {/* QR Check-in Code Box */}
        {ev.qrCheckInCode && (
          <div className="pt-6 border-t border-gray-100 dark:border-gray-800 flex flex-col sm:flex-row items-center gap-6 p-6 rounded-2xl bg-surface dark:bg-navy-light">
            <div className="w-24 h-24 bg-white p-2 rounded-xl shadow border flex items-center justify-center text-navy font-mono font-bold text-xs text-center">
              <QrCode className="w-16 h-16 text-navy" />
            </div>
            <div className="space-y-1 text-center sm:text-left">
              <h3 className="text-sm font-bold text-navy dark:text-white">Mã Điểm Danh Sự Kiện (Check-in Code)</h3>
              <p className="text-xs text-gray-500 font-mono tracking-wider font-bold text-tealAccent">
                {ev.qrCheckInCode}
              </p>
              <p className="text-[11px] text-gray-500">
                Xuất trình mã này cho Ban Chủ Nhiệm hoặc quét trên ứng dụng di động để được xác nhận tham dự.
              </p>
            </div>
          </div>
        )}

        <div className="pt-6 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
          <span className="text-xs text-gray-500">
            Hạn đăng ký: {new Date(ev.registrationDeadline).toLocaleDateString("vi-VN")}
          </span>

          {registered ? (
            <div className="flex items-center gap-1.5 text-xs text-emerald-600 font-bold">
              <CheckCircle className="w-4 h-4" />
              <span>Bạn đã đăng ký tham gia</span>
            </div>
          ) : (
            <button
              onClick={handleRegister}
              className="px-6 py-2.5 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 transition-all hover:scale-105"
            >
              Đăng ký tham gia ngay
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

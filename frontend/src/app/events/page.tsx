"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Calendar, MapPin, Users, Search, CheckCircle, Clock, ExternalLink, ArrowRight } from "lucide-react";
import { api } from "../../lib/api";
import { EventItem } from "../../lib/types";

export default function EventsPage() {
  const [events, setEvents] = useState<EventItem[]>([]);
  const [search, setSearch] = useState("");
  const [registerStatus, setRegisterStatus] = useState<Record<string, string>>({});

  const fallbackEvents: EventItem[] = [
    {
      id: "ev1",
      title: "VISIONARY Tech & English Talk 2026: Lộ trình làm chủ AI và Hội nhập Toàn cầu",
      slug: "visionary-tech-english-talk-2026",
      description: "Buổi tọa đàm chuyên sâu về cách kết hợp năng lực tiếng Anh chuyên ngành với các công nghệ AI hiện đại (LLMs, RAG, Web API) để tự tin ứng tuyển các tập đoàn công nghệ đa quốc gia.",
      location: "Hội trường Edison, Trường Đại học Công nghệ Đồng Nai & Online MS Teams",
      startTime: new Date(Date.now() + 7 * 86400000).toISOString(),
      endTime: new Date(Date.now() + 7 * 86400000 + 3 * 3600000).toISOString(),
      registrationDeadline: new Date(Date.now() + 6 * 86400000).toISOString(),
      maxCapacity: 150,
      currentRegistrationsCount: 42,
      status: "Published",
      isRegisteredByCurrentUser: false,
      isCheckedInByCurrentUser: false,
      qrCheckInCode: "VIS-QR-EVENT1"
    },
    {
      id: "ev2",
      title: "Workshop: Làm chủ thuật ngữ REST API & Clean Architecture trong phỏng vấn quốc tế",
      slug: "workshop-rest-api-clean-architecture",
      description: "Thực hành phỏng vấn kỹ thuật bằng tiếng Anh cho các vị trí Backend .NET, Frontend Next.js và Mobile Developer.",
      location: "Phòng Lab CNTT, Trường ĐH Công nghệ Đồng Nai",
      startTime: new Date(Date.now() + 14 * 86400000).toISOString(),
      endTime: new Date(Date.now() + 14 * 86400000 + 3 * 3600000).toISOString(),
      registrationDeadline: new Date(Date.now() + 13 * 86400000).toISOString(),
      maxCapacity: 60,
      currentRegistrationsCount: 28,
      status: "Published",
      isRegisteredByCurrentUser: false,
      isCheckedInByCurrentUser: false,
      qrCheckInCode: "VIS-QR-EVENT2"
    }
  ];

  useEffect(() => {
    api.getEvents({ search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setEvents(res.data.items);
        } else {
          setEvents(fallbackEvents);
        }
      })
      .catch(() => setEvents(fallbackEvents));
  }, [search]);

  const handleRegister = async (id: string) => {
    setRegisterStatus((prev) => ({ ...prev, [id]: "Đang đăng ký..." }));
    const res = await api.registerEvent(id);
    if (res.success) {
      setRegisterStatus((prev) => ({ ...prev, [id]: "Đã đăng ký thành công!" }));
      setEvents((prev) =>
        prev.map((e) => (e.id === id ? { ...e, isRegisteredByCurrentUser: true, currentRegistrationsCount: e.currentRegistrationsCount + 1 } : e))
      );
    } else {
      setRegisterStatus((prev) => ({ ...prev, [id]: res.message || "Vui lòng đăng nhập để đăng ký sự kiện." }));
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Sự kiện & Hoạt động CLB
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Lịch Trình Hoạt Động & Hội Thảo
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Tham gia các buổi sinh hoạt chuyên đề tiếng Anh, tọa đàm công nghệ, hackathon nội bộ và hoạt động cộng đồng của CLB Tiếng Anh DNTU.
        </p>
      </div>

      {/* Search */}
      <div className="glass-card p-4 rounded-2xl flex items-center justify-between max-w-xl mx-auto">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm theo tên sự kiện, địa điểm..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
          />
        </div>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {events.map((e) => (
          <div
            key={e.id}
            className="glass-card rounded-2xl p-6 border-l-4 border-visionary flex flex-col justify-between hover:shadow-lg transition-all"
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="badge-teal text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  {e.status}
                </span>
                <span className="text-xs text-gray-500 font-medium flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5 text-tealAccent" />
                  {new Date(e.startTime).toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" })} •{" "}
                  {new Date(e.startTime).toLocaleDateString("vi-VN")}
                </span>
              </div>

              <h3 className="text-lg font-bold text-navy dark:text-white">
                {e.title}
              </h3>

              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                {e.description}
              </p>

              <div className="space-y-1.5 text-xs text-gray-500">
                <div className="flex items-center gap-2">
                  <MapPin className="w-3.5 h-3.5 text-tealAccent flex-shrink-0" />
                  <span>{e.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-3.5 h-3.5 text-visionary flex-shrink-0" />
                  <span>
                    Đã đăng ký: <strong>{e.currentRegistrationsCount}</strong> / {e.maxCapacity} chỗ
                  </span>
                </div>
              </div>

              {registerStatus[e.id] && (
                <div className="p-2.5 rounded-lg bg-tealAccent/10 text-tealAccent text-xs font-semibold">
                  {registerStatus[e.id]}
                </div>
              )}
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <Link
                href={`/events/${e.slug}`}
                className="text-xs font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1"
              >
                <span>Xem chi tiết</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>

              {e.isRegisteredByCurrentUser ? (
                <span className="px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-600 dark:bg-emerald-950/30 dark:text-emerald-400 text-xs font-bold flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Đã đăng ký</span>
                </span>
              ) : (
                <button
                  onClick={() => handleRegister(e.id)}
                  className="px-4 py-2 rounded-lg bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 hover:scale-[1.02] transition-all"
                >
                  Đăng ký tham gia
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

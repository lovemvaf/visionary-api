"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  Calendar,
  MapPin,
  Users,
  Search,
  CheckCircle,
  Clock,
  ExternalLink,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { EventItem } from "../../lib/types";

function EventsContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [events, setEvents] = useState<EventItem[]>([]);
  const [search, setSearch] = useState<string>(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState<string>(initialSearch);
  const [pageIndex, setPageIndex] = useState<number>(initialPage > 0 ? initialPage : 1);
  const pageSize = 6;

  const [totalCount, setTotalCount] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(false);
  const [hasPreviousPage, setHasPreviousPage] = useState<boolean>(false);

  const [status, setStatus] = useState<"loading" | "success" | "empty" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [registerStatus, setRegisterStatus] = useState<Record<string, string>>({});
  const requestSeq = useRef(0);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const updateUrl = useCallback((s: string, p: number) => {
    const params = new URLSearchParams();
    if (s.trim()) params.set("search", s.trim());
    if (p > 1) params.set("page", p.toString());
    const qs = params.toString();
    router.replace(`${pathname}${qs ? `?${qs}` : ""}`, { scroll: false });
  }, [pathname, router]);

  const fetchEvents = useCallback(async () => {
    const seq = ++requestSeq.current;
    setStatus("loading");
    setErrorMessage("");

    try {
      const res = await api.getEvents({
        search: debouncedSearch.trim() || undefined,
        pageIndex,
        pageSize,
      });

      if (seq !== requestSeq.current) return;

      if (res.success && res.data) {
        setEvents(res.data.items || []);
        setTotalCount(res.data.totalCount || 0);
        setTotalPages(res.data.totalPages || 1);
        setHasNextPage(res.data.hasNextPage || false);
        setHasPreviousPage(res.data.hasPreviousPage || false);

        if (!res.data.items || res.data.items.length === 0) {
          setStatus("empty");
        } else {
          setStatus("success");
        }
      } else {
        setEvents([]);
        setStatus("error");
        setErrorMessage(res.message || "Không thể tải danh sách sự kiện.");
      }
    } catch (err: any) {
      if (seq !== requestSeq.current) return;
      setEvents([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
    }
  }, [debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchEvents();
    updateUrl(debouncedSearch, pageIndex);
  }, [fetchEvents, updateUrl, debouncedSearch, pageIndex]);

  const handleRegister = async (eventId: string) => {
    setRegisterStatus((prev) => ({ ...prev, [eventId]: "loading" }));
    try {
      const res = await api.registerEvent(eventId);
      if (res.success) {
        setRegisterStatus((prev) => ({ ...prev, [eventId]: "success" }));
        fetchEvents();
      } else {
        setRegisterStatus((prev) => ({ ...prev, [eventId]: "error: " + (res.message || "Đăng ký không thành công") }));
      }
    } catch (err: any) {
      setRegisterStatus((prev) => ({ ...prev, [eventId]: "error: " + (err?.message || "Lỗi kết nối") }));
    }
  };

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages && newPage !== pageIndex) {
      setPageIndex(newPage);
      window.scrollTo({ top: 250, behavior: "smooth" });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Club Activities
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Sự kiện & Hội thảo Công nghệ DNTU
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Lịch trình sinh hoạt định kỳ, workshop chuyên đề và các buổi giao lưu học thuật do CLB Tiếng Anh và nhóm kỹ thuật VISIONARY tổ chức.
        </p>
      </div>

      {/* Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 border border-surface-border">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm theo tên sự kiện, địa điểm..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPageIndex(1); }}
            className="w-full pl-9 pr-8 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
          />
          {search && (
            <button
              onClick={() => { setSearch(""); setDebouncedSearch(""); setPageIndex(1); }}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs font-bold"
            >
              ×
            </button>
          )}
        </div>

        <span className="text-xs text-gray-500">
          {status === "loading"
            ? "Đang tải sự kiện..."
            : `Hiển thị ${events.length} sự kiện (Tổng số: ${totalCount})`}
        </span>
      </div>

      {/* 1. LOADING */}
      {status === "loading" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="glass-card rounded-2xl p-6 space-y-4 animate-pulse">
              <div className="h-5 w-3/4 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-1/2 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-full bg-gray-200 dark:bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 max-w-md mx-auto border border-red-200 dark:border-red-900/50">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải danh sách sự kiện</h3>
          <p className="text-xs text-gray-500">{errorMessage}</p>
          <button
            onClick={() => fetchEvents()}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-visionary text-white text-xs font-semibold"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Thử lại</span>
          </button>
        </div>
      )}

      {/* 3. EMPTY */}
      {status === "empty" && (
        <div className="glass-card rounded-2xl p-12 text-center space-y-4 max-w-md mx-auto">
          <Calendar className="w-8 h-8 text-gray-400 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Chưa có sự kiện phù hợp</h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không tìm thấy sự kiện nào khớp với từ khóa "${debouncedSearch}".`
              : "Hiện tại chưa có sự kiện mới nào được công bố."}
          </p>
        </div>
      )}

      {/* 4. SUCCESS */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {events.map((ev) => (
              <div
                key={ev.id}
                className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all border border-surface-border shadow-sm group"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                      {ev.status}
                    </span>
                    <span className="text-xs text-gray-500 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-tealAccent" />
                      <span>{new Date(ev.startTime).toLocaleDateString("vi-VN", { hour: "2-digit", minute: "2-digit" })}</span>
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                    {ev.title}
                  </h3>

                  <div className="text-xs text-gray-500 flex items-center gap-1.5">
                    <MapPin className="w-3.5 h-3.5 text-visionary flex-shrink-0" />
                    <span>{ev.location}</span>
                  </div>

                  <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                    {ev.description}
                  </p>

                  <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-surface-border">
                    <span className="flex items-center gap-1">
                      <Users className="w-3.5 h-3.5 text-tealAccent" />
                      <span>{ev.currentRegistrationsCount} / {ev.maxCapacity} chỗ</span>
                    </span>
                    <span>
                      Hạn: {new Date(ev.registrationDeadline).toLocaleDateString("vi-VN")}
                    </span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between">
                  <span className="text-[11px] text-gray-400">
                    Mã Check-in: <strong className="font-mono text-gray-600 dark:text-gray-300">{ev.qrCheckInCode || "Chưa phát"}</strong>
                  </span>

                  <button
                    onClick={() => handleRegister(ev.id)}
                    disabled={registerStatus[ev.id] === "loading" || registerStatus[ev.id] === "success" || ev.isRegisteredByCurrentUser}
                    className="px-3.5 py-1.5 rounded-xl bg-visionary text-white text-xs font-semibold hover:bg-visionary/90 transition-all disabled:opacity-50"
                  >
                    {registerStatus[ev.id] === "loading" ? "Đang xử lý..." :
                     registerStatus[ev.id] === "success" || ev.isRegisteredByCurrentUser ? "Đã đăng ký" :
                     "Đăng ký tham gia"}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-surface-border">
              <span className="text-xs text-gray-500">
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> sự kiện)
              </span>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => handlePageChange(pageIndex - 1)}
                  disabled={!hasPreviousPage}
                  className="px-3 py-1.5 rounded-lg border border-surface-border text-xs font-semibold disabled:opacity-30 hover:bg-gray-100 dark:hover:bg-navy-light flex items-center gap-1"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                  <span>Trước</span>
                </button>

                {Array.from({ length: totalPages }).map((_, idx) => {
                  const pNum = idx + 1;
                  return (
                    <button
                      key={pNum}
                      onClick={() => handlePageChange(pNum)}
                      className={`w-8 h-8 rounded-lg text-xs font-bold transition-all ${
                        pNum === pageIndex
                          ? "bg-visionary text-white shadow-sm"
                          : "border border-surface-border hover:bg-gray-100 dark:hover:bg-navy-light"
                      }`}
                    >
                      {pNum}
                    </button>
                  );
                })}

                <button
                  onClick={() => handlePageChange(pageIndex + 1)}
                  disabled={!hasNextPage}
                  className="px-3 py-1.5 rounded-lg border border-surface-border text-xs font-semibold disabled:opacity-30 hover:bg-gray-100 dark:hover:bg-navy-light flex items-center gap-1"
                >
                  <span>Sau</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default function EventsPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo lịch sự kiện...
      </div>
    }>
      <EventsContent />
    </Suspense>
  );
}

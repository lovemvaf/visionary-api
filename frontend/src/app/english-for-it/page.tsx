"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  BookOpen,
  Search,
  ArrowRight,
  Volume2,
  Bookmark,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { LearningResource } from "../../lib/types";

function EnglishForItContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const initialLevel = searchParams.get("level") || "";
  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [resources, setResources] = useState<LearningResource[]>([]);
  const [level, setLevel] = useState<string>(initialLevel);
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
  const requestSeq = useRef(0);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  // URL sync
  const updateUrl = useCallback((lvl: string, s: string, p: number) => {
    const params = new URLSearchParams();
    if (lvl) params.set("level", lvl);
    if (s.trim()) params.set("search", s.trim());
    if (p > 1) params.set("page", p.toString());
    const qs = params.toString();
    router.replace(`${pathname}${qs ? `?${qs}` : ""}`, { scroll: false });
  }, [pathname, router]);

  const fetchResources = useCallback(async () => {
    const seq = ++requestSeq.current;
    setStatus("loading");
    setErrorMessage("");

    try {
      const res = await api.getEnglishResources({
        level: level || undefined,
        search: debouncedSearch.trim() || undefined,
        pageIndex,
        pageSize,
      });

      if (seq !== requestSeq.current) return;

      if (res.success && res.data) {
        setResources(res.data.items || []);
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
        setResources([]);
        setStatus("error");
        setErrorMessage(res.message || "Không thể tải danh sách tài liệu English for IT.");
      }
    } catch (err: any) {
      if (seq !== requestSeq.current) return;
      setResources([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
    }
  }, [level, debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchResources();
    updateUrl(level, debouncedSearch, pageIndex);
  }, [fetchResources, updateUrl, level, debouncedSearch, pageIndex]);

  const handleLevelSelect = (lvl: string) => {
    if (level !== lvl) {
      setLevel(lvl);
      setPageIndex(1);
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPageIndex(1);
  };

  const handleResetFilters = () => {
    setLevel("");
    setSearch("");
    setDebouncedSearch("");
    setPageIndex(1);
  };

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages && newPage !== pageIndex) {
      setPageIndex(newPage);
      window.scrollTo({ top: 250, behavior: "smooth" });
    }
  };

  const levels = ["Beginner", "Intermediate", "Advanced", "Professional"];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Learning Center
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          English for IT – Tiếng Anh Chuyên ngành CNTT
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Chương trình học tập tương tác thuật ngữ kỹ thuật, giao tiếp Agile và rèn luyện kỹ năng phỏng vấn tuyển dụng quốc tế.
        </p>
      </div>

      {/* Filter and Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-surface-border">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <button
            onClick={() => handleLevelSelect("")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              level === ""
                ? "bg-visionary text-white shadow-sm"
                : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
            }`}
          >
            Tất cả cấp độ
          </button>
          {levels.map((lvl) => (
            <button
              key={lvl}
              onClick={() => handleLevelSelect(lvl)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                level === lvl
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {lvl}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm theo chủ đề, thuật ngữ..."
            value={search}
            onChange={handleSearchChange}
            className="w-full pl-9 pr-8 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
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
      </div>

      {/* Scope Header */}
      <div className="flex items-center justify-between text-xs text-gray-500 border-b border-surface-border pb-3">
        <span>
          {status === "loading"
            ? "Đang tải bài học..."
            : `Hiển thị ${resources.length} bài học (Tổng số: ${totalCount})`}
          {level && ` • Cấp độ: ${level}`}
        </span>

        {(level || debouncedSearch) && (
          <button
            onClick={handleResetFilters}
            className="inline-flex items-center gap-1 text-visionary dark:text-tealAccent hover:underline font-semibold"
          >
            <FilterX className="w-3.5 h-3.5" />
            <span>Xóa bộ lọc</span>
          </button>
        )}
      </div>

      {/* 1. LOADING */}
      {status === "loading" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="glass-card rounded-2xl p-6 space-y-4 animate-pulse">
              <div className="h-4 w-20 bg-gray-200 dark:bg-gray-800 rounded-full" />
              <div className="h-5 w-3/4 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-full bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-2/3 bg-gray-200 dark:bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 max-w-md mx-auto border border-red-200 dark:border-red-900/50">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải tài liệu học tập</h3>
          <p className="text-xs text-gray-500">{errorMessage}</p>
          <button
            onClick={() => fetchResources()}
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
          <BookOpen className="w-8 h-8 text-gray-400 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Chưa có tài liệu phù hợp</h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không tìm thấy tài liệu phù hợp với từ khóa "${debouncedSearch}".`
              : "Hiện chưa có bài giảng nào trong cấp độ này."}
          </p>
          {(level || debouncedSearch) && (
            <button
              onClick={handleResetFilters}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-navy-light text-xs font-semibold text-navy dark:text-gray-200"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Xem tất cả cấp độ</span>
            </button>
          )}
        </div>
      )}

      {/* 4. SUCCESS */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((item) => {
              let glossary = [];
              try {
                glossary = item.glossaryJson ? JSON.parse(item.glossaryJson) : [];
              } catch {
                glossary = [];
              }

              return (
                <div
                  key={item.id}
                  className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all border border-surface-border shadow-sm group"
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                        {item.level}
                      </span>
                      <span className="text-[11px] text-gray-500 font-medium">
                        {item.topic}
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                      {item.title}
                    </h3>

                    <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                      {item.summary}
                    </p>

                    {glossary.length > 0 && (
                      <div className="space-y-2 pt-2 border-t border-surface-border">
                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                          Thuật ngữ tiêu biểu:
                        </span>
                        <div className="space-y-1.5">
                          {glossary.slice(0, 2).map((g: any, idx: number) => (
                            <div key={idx} className="p-2 rounded-lg bg-gray-50 dark:bg-navy-light/50 text-xs">
                              <div className="flex items-center justify-between font-semibold text-navy dark:text-white">
                                <span>{g.term}</span>
                                <span className="text-[10px] text-tealAccent font-normal">{g.phonetic}</span>
                              </div>
                              <p className="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5">{g.meaning}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between text-xs">
                    <span className="text-gray-400">{item.viewCount || 0} lượt học</span>
                    <Link
                      href={`/english-for-it/${item.slug}`}
                      className="font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1 group-hover:gap-1.5 transition-all"
                    >
                      <span>Vào bài học</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-surface-border">
              <span className="text-xs text-gray-500">
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> tài liệu)
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

export default function EnglishForItPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo trung tâm học tập English for IT...
      </div>
    }>
      <EnglishForItContent />
    </Suspense>
  );
}

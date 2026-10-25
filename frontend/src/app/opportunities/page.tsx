"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  Compass,
  Search,
  Calendar,
  Globe,
  ExternalLink,
  ShieldCheck,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { OpportunityItem } from "../../lib/types";

function OpportunitiesContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const initialCat = searchParams.get("category") || "";
  const initialScope = searchParams.get("scope") || "";
  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [category, setCategory] = useState<string>(initialCat);
  const [scope, setScope] = useState<string>(initialScope);
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

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const updateUrl = useCallback((cat: string, sc: string, s: string, p: number) => {
    const params = new URLSearchParams();
    if (cat) params.set("category", cat);
    if (sc) params.set("scope", sc);
    if (s.trim()) params.set("search", s.trim());
    if (p > 1) params.set("page", p.toString());
    const qs = params.toString();
    router.replace(`${pathname}${qs ? `?${qs}` : ""}`, { scroll: false });
  }, [pathname, router]);

  const fetchOpportunities = useCallback(async () => {
    const seq = ++requestSeq.current;
    setStatus("loading");
    setErrorMessage("");

    try {
      const res = await api.getOpportunities({
        category: category || undefined,
        scope: scope || undefined,
        search: debouncedSearch.trim() || undefined,
        pageIndex,
        pageSize,
      });

      if (seq !== requestSeq.current) return;

      if (res.success && res.data) {
        setOpportunities(res.data.items || []);
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
        setOpportunities([]);
        setStatus("error");
        setErrorMessage(res.message || "Không thể tải danh sách cơ hội hội nhập.");
      }
    } catch (err: any) {
      if (seq !== requestSeq.current) return;
      setOpportunities([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
    }
  }, [category, scope, debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchOpportunities();
    updateUrl(category, scope, debouncedSearch, pageIndex);
  }, [fetchOpportunities, updateUrl, category, scope, debouncedSearch, pageIndex]);

  const handleResetFilters = () => {
    setCategory("");
    setScope("");
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

  const categories = [
    { id: "", label: "Tất cả lĩnh vực" },
    { id: "Hackathon", label: "Hackathon & Sáng tạo" },
    { id: "AlgorithmIcpc", label: "ICPC & Thuật toán" },
    { id: "AiChallenge", label: "AI Challenge" },
    { id: "Scholarship", label: "Học bổng" },
    { id: "ExchangeProgram", label: "Trao đổi sinh viên" }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Global Opportunities
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Cơ hội Hội nhập & Cuộc thi Quốc tế
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Cổng thông tin kiểm chứng về các sân chơi lập trình ICPC, Hackathon quốc tế, học bổng ASEAN và chương trình trao đổi sinh viên toàn cầu.
        </p>
      </div>

      {/* Filters */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-surface-border">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {categories.map((c) => (
            <button
              key={c.id}
              onClick={() => { setCategory(c.id); setPageIndex(1); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                category === c.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {c.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <select
            value={scope}
            onChange={(e) => { setScope(e.target.value); setPageIndex(1); }}
            className="px-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
          >
            <option value="">Tất cả quy mô</option>
            <option value="Global">Toàn cầu (Global)</option>
            <option value="ASEAN">Khu vực ASEAN</option>
            <option value="Vietnam">Việt Nam</option>
          </select>

          <div className="relative w-full md:w-56">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm cuộc thi..."
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
        </div>
      </div>

      {/* Scope Header */}
      <div className="flex items-center justify-between text-xs text-gray-500 border-b border-surface-border pb-3">
        <span>
          {status === "loading"
            ? "Đang tải dữ liệu cơ hội..."
            : `Hiển thị ${opportunities.length} cơ hội (Tổng số: ${totalCount})`}
        </span>

        {(category || scope || debouncedSearch) && (
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
              <div className="h-5 w-4/5 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-full bg-gray-200 dark:bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 max-w-md mx-auto border border-red-200 dark:border-red-900/50">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải danh sách cơ hội</h3>
          <p className="text-xs text-gray-500">{errorMessage}</p>
          <button
            onClick={() => fetchOpportunities()}
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
          <Compass className="w-8 h-8 text-gray-400 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Chưa có cơ hội phù hợp</h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không tìm thấy cơ hội nào khớp với từ khóa "${debouncedSearch}".`
              : "Hiện chưa có cuộc thi hoặc chương trình nào trong danh mục này."}
          </p>
        </div>
      )}

      {/* 4. SUCCESS */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {opportunities.map((item) => (
              <div
                key={item.id}
                className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all border border-surface-border shadow-sm group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                      {item.category}
                    </span>
                    <span className="text-[11px] text-gray-500 font-semibold flex items-center gap-1">
                      <Globe className="w-3 h-3 text-tealAccent" />
                      <span>{item.scope}</span>
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                    {item.title}
                  </h3>

                  <div className="text-xs text-gray-500 font-medium">
                    Đơn vị tổ chức: <strong className="text-navy dark:text-gray-200">{item.organizer}</strong>
                  </div>

                  <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                    {item.eligibility}
                  </p>

                  <div className="text-[11px] text-gray-500 flex items-center gap-1.5 pt-2 border-t border-surface-border">
                    <Calendar className="w-3.5 h-3.5 text-tealAccent" />
                    <span>
                      Hạn đăng ký: {item.registrationDeadline ? new Date(item.registrationDeadline).toLocaleDateString("vi-VN") : "Đang mở"}
                    </span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between text-xs">
                  {item.verifiedSource ? (
                    <span className="text-[10px] text-tealAccent font-semibold flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{item.verifiedSource}</span>
                    </span>
                  ) : <span />}

                  {item.officialUrl && (
                    <a
                      href={item.officialUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1"
                    >
                      <span>Trang chính thức</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-surface-border">
              <span className="text-xs text-gray-500">
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> cơ hội)
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

export default function OpportunitiesPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo cổng cơ hội hội nhập...
      </div>
    }>
      <OpportunitiesContent />
    </Suspense>
  );
}

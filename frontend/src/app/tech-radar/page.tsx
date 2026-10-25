"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  Radio,
  Search,
  Star,
  GitFork,
  ExternalLink,
  RefreshCw,
  Sparkles,
  Shield,
  Cpu,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { TechResource } from "../../lib/types";

function TechRadarContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const initialSource = searchParams.get("sourceType") || "";
  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [resources, setResources] = useState<TechResource[]>([]);
  const [sourceType, setSourceType] = useState<string>(initialSource);
  const [search, setSearch] = useState<string>(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState<string>(initialSearch);
  const [pageIndex, setPageIndex] = useState<number>(initialPage > 0 ? initialPage : 1);
  const pageSize = 9;

  const [totalCount, setTotalCount] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(false);
  const [hasPreviousPage, setHasPreviousPage] = useState<boolean>(false);

  const [status, setStatus] = useState<"loading" | "success" | "empty" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [syncMessage, setSyncMessage] = useState<string>("");
  const requestSeq = useRef(0);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(search), 300);
    return () => clearTimeout(timer);
  }, [search]);

  const updateUrl = useCallback((src: string, s: string, p: number) => {
    const params = new URLSearchParams();
    if (src) params.set("sourceType", src);
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
      const res = await api.getTechResources({
        sourceType: sourceType || undefined,
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
        setErrorMessage(res.message || "Không thể tải dữ liệu Technology Radar.");
      }
    } catch (err: any) {
      if (seq !== requestSeq.current) return;
      setResources([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
    }
  }, [sourceType, debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchResources();
    updateUrl(sourceType, debouncedSearch, pageIndex);
  }, [fetchResources, updateUrl, sourceType, debouncedSearch, pageIndex]);

  const handleSourceSelect = (src: string) => {
    if (sourceType !== src) {
      setSourceType(src);
      setPageIndex(1);
    }
  };

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages && newPage !== pageIndex) {
      setPageIndex(newPage);
      window.scrollTo({ top: 250, behavior: "smooth" });
    }
  };

  const handleSync = async () => {
    setIsSyncing(true);
    setSyncMessage("");
    try {
      const res = await api.syncTechResources(sourceType || "All");
      if (res.success) {
        setSyncMessage("Đồng bộ thành công dữ liệu mới nhất!");
        fetchResources();
      } else {
        setSyncMessage(res.message || "Không thể đồng bộ vào lúc này.");
      }
    } catch {
      setSyncMessage("Lỗi kết nối khi đồng bộ.");
    } finally {
      setIsSyncing(false);
      setTimeout(() => setSyncMessage(""), 4000);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Technology Radar
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Radar Công nghệ & Xu hướng Toàn cầu
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Tổng hợp tự động các kho mã nguồn nổi bật từ GitHub API và mô hình AI từ Hugging Face Hub phục vụ nghiên cứu và hội nhập kỹ thuật.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-surface-border">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {[
            { id: "", label: "Tất cả nguồn" },
            { id: "GitHubRepository", label: "GitHub Repositories" },
            { id: "HuggingFaceModel", label: "Hugging Face Models" },
            { id: "DevToArticle", label: "Kỹ thuật & Bài báo" },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => handleSourceSelect(item.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                sourceType === item.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="relative w-full md:w-64">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm repository, model..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPageIndex(1); }}
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

          <button
            onClick={handleSync}
            disabled={isSyncing}
            className="flex-shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200 text-xs font-semibold transition-all disabled:opacity-50"
            title="Đồng bộ dữ liệu"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? "animate-spin text-tealAccent" : ""}`} />
            <span className="hidden sm:inline">{isSyncing ? "Đang cập nhật..." : "Đồng bộ"}</span>
          </button>
        </div>
      </div>

      {syncMessage && (
        <div className="p-3 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-teal-700 dark:text-teal-300 text-xs font-medium text-center">
          {syncMessage}
        </div>
      )}

      {/* Scope Header */}
      <div className="flex items-center justify-between text-xs text-gray-500 border-b border-surface-border pb-3">
        <span>
          {status === "loading"
            ? "Đang tải dữ liệu Radar..."
            : `Hiển thị ${resources.length} tài nguyên (Tổng số: ${totalCount})`}
        </span>

        {(sourceType || debouncedSearch) && (
          <button
            onClick={() => { setSourceType(""); setSearch(""); setDebouncedSearch(""); setPageIndex(1); }}
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
              <div className="h-4 w-24 bg-gray-200 dark:bg-gray-800 rounded-full" />
              <div className="h-5 w-3/4 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-full bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="h-3 w-1/2 bg-gray-200 dark:bg-gray-800 rounded" />
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 max-w-md mx-auto border border-red-200 dark:border-red-900/50">
          <AlertCircle className="w-8 h-8 text-red-500 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải Technology Radar</h3>
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
          <Cpu className="w-8 h-8 text-gray-400 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Chưa có tài nguyên phù hợp</h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không tìm thấy tài nguyên khớp với từ khóa "${debouncedSearch}".`
              : "Hiện chưa có tài nguyên công nghệ trong nguồn này."}
          </p>
        </div>
      )}

      {/* 4. SUCCESS */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((item) => {
              let metrics: any = {};
              try {
                metrics = item.metricsJson ? JSON.parse(item.metricsJson) : {};
              } catch {
                metrics = {};
              }

              return (
                <div
                  key={item.id}
                  className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all border border-surface-border shadow-sm group"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                        {item.sourceType === "GitHubRepository" ? "GitHub" : item.sourceType === "HuggingFaceModel" ? "Hugging Face" : item.sourceType}
                      </span>
                      {item.isVerified && (
                        <span className="text-[10px] text-tealAccent font-semibold flex items-center gap-1">
                          <Shield className="w-3 h-3" />
                          <span>Đã xác thực</span>
                        </span>
                      )}
                    </div>

                    <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors truncate">
                      {item.name}
                    </h3>

                    <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                      {item.description || "Tài nguyên công nghệ nghiên cứu và ứng dụng."}
                    </p>

                    <div className="flex flex-wrap items-center gap-2 pt-2 text-[11px] text-gray-500">
                      {item.primaryLanguage && (
                        <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-navy-light font-medium">
                          {item.primaryLanguage}
                        </span>
                      )}
                      {item.license && (
                        <span className="px-2 py-0.5 rounded-md bg-gray-100 dark:bg-navy-light">
                          {item.license}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between text-xs">
                    <div className="flex items-center gap-3 text-gray-500">
                      {metrics.stars !== undefined && (
                        <span className="flex items-center gap-1">
                          <Star className="w-3.5 h-3.5 text-amber-500" />
                          <span>{Number(metrics.stars).toLocaleString()}</span>
                        </span>
                      )}
                      {metrics.downloads !== undefined && (
                        <span className="flex items-center gap-1">
                          <Cpu className="w-3.5 h-3.5 text-visionary" />
                          <span>{Number(metrics.downloads).toLocaleString()} tải</span>
                        </span>
                      )}
                    </div>

                    {item.officialUrl && (
                      <a
                        href={item.officialUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1"
                      >
                        <span>Mở liên kết</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-surface-border">
              <span className="text-xs text-gray-500">
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> tài nguyên)
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

export default function TechRadarPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo radar công nghệ...
      </div>
    }>
      <TechRadarContent />
    </Suspense>
  );
}

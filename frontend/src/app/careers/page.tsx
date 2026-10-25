"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  Briefcase,
  MapPin,
  Building,
  ExternalLink,
  Search,
  CheckCircle,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { JobItem } from "../../lib/types";

function CareersContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const initialJobType = searchParams.get("jobType") || "";
  const initialWorkplace = searchParams.get("workplaceType") || "";
  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [jobType, setJobType] = useState<string>(initialJobType);
  const [workplaceType, setWorkplaceType] = useState<string>(initialWorkplace);
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

  const updateUrl = useCallback((jt: string, wp: string, s: string, p: number) => {
    const params = new URLSearchParams();
    if (jt) params.set("jobType", jt);
    if (wp) params.set("workplaceType", wp);
    if (s.trim()) params.set("search", s.trim());
    if (p > 1) params.set("page", p.toString());
    const qs = params.toString();
    router.replace(`${pathname}${qs ? `?${qs}` : ""}`, { scroll: false });
  }, [pathname, router]);

  const fetchJobs = useCallback(async () => {
    const seq = ++requestSeq.current;
    setStatus("loading");
    setErrorMessage("");

    try {
      const res = await api.getJobs({
        jobType: jobType || undefined,
        workplaceType: workplaceType || undefined,
        search: debouncedSearch.trim() || undefined,
        pageIndex,
        pageSize,
      });

      if (seq !== requestSeq.current) return;

      if (res.success && res.data) {
        setJobs(res.data.items || []);
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
        setJobs([]);
        setStatus("error");
        setErrorMessage(res.message || "Không thể tải danh sách việc làm.");
      }
    } catch (err: any) {
      if (seq !== requestSeq.current) return;
      setJobs([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối máy chủ.");
    }
  }, [jobType, workplaceType, debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchJobs();
    updateUrl(jobType, workplaceType, debouncedSearch, pageIndex);
  }, [fetchJobs, updateUrl, jobType, workplaceType, debouncedSearch, pageIndex]);

  const handleResetFilters = () => {
    setJobType("");
    setWorkplaceType("");
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

  const jobTypes = [
    { id: "", label: "Tất cả vị trí" },
    { id: "Internship", label: "Thực tập sinh (Internship)" },
    { id: "Fresher", label: "Mới tốt nghiệp (Fresher)" },
    { id: "Junior", label: "Junior Engineer" },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Career Gateway
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Cổng Cơ hội Việc làm & Thực tập Quốc tế
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Kết nối sinh viên DNTU với các tập đoàn công nghệ toàn cầu, yêu cầu năng lực kỹ thuật và tiếng Anh chuyên nghiệp.
        </p>
      </div>

      {/* Filters */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-surface-border">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {jobTypes.map((t) => (
            <button
              key={t.id}
              onClick={() => { setJobType(t.id); setPageIndex(1); }}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                jobType === t.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <select
            value={workplaceType}
            onChange={(e) => { setWorkplaceType(e.target.value); setPageIndex(1); }}
            className="px-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
          >
            <option value="">Tất cả hình thức</option>
            <option value="Onsite">Tại văn phòng (Onsite)</option>
            <option value="Hybrid">Linh hoạt (Hybrid)</option>
            <option value="Remote">Làm từ xa (Remote)</option>
          </select>

          <div className="relative w-full md:w-56">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm công ty, kỹ năng..."
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
            ? "Đang tải dữ liệu việc làm..."
            : `Hiển thị ${jobs.length} vị trí (Tổng số: ${totalCount})`}
        </span>

        {(jobType || workplaceType || debouncedSearch) && (
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
              <div className="h-4 w-24 bg-gray-200 dark:bg-gray-800 rounded-full" />
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
          <h3 className="text-base font-bold text-navy dark:text-white">Không thể tải danh sách việc làm</h3>
          <p className="text-xs text-gray-500">{errorMessage}</p>
          <button
            onClick={() => fetchJobs()}
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
          <Briefcase className="w-8 h-8 text-gray-400 mx-auto" />
          <h3 className="text-base font-bold text-navy dark:text-white">Chưa có vị trí phù hợp</h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không tìm thấy vị trí tuyển dụng khớp với từ khóa "${debouncedSearch}".`
              : "Hiện chưa có vị trí việc làm nào trong bộ lọc đã chọn."}
          </p>
        </div>
      )}

      {/* 4. SUCCESS */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map((item) => (
              <div
                key={item.id}
                className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all border border-surface-border shadow-sm group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                      {item.jobType}
                    </span>
                    <span className="text-[11px] text-gray-500 font-semibold flex items-center gap-1">
                      <MapPin className="w-3 h-3 text-tealAccent" />
                      <span>{item.location} ({item.workplaceType})</span>
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                    {item.title}
                  </h3>

                  <div className="text-xs text-gray-600 dark:text-gray-300 font-medium flex items-center gap-1.5">
                    <Building className="w-3.5 h-3.5 text-visionary" />
                    <span>{item.company}</span>
                  </div>

                  <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                    {item.requirements}
                  </p>

                  {item.englishRequired && (
                    <div className="inline-flex items-center gap-1 text-[11px] text-tealAccent font-semibold">
                      <CheckCircle className="w-3 h-3" />
                      <span>Yêu cầu tiếng Anh chuyên ngành</span>
                    </div>
                  )}
                </div>

                <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between text-xs">
                  <span className="text-gray-400">
                    {item.createdAt ? new Date(item.createdAt).toLocaleDateString("vi-VN") : "Đang tuyển"}
                  </span>

                  {item.applyUrl && (
                    <a
                      href={item.applyUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1"
                    >
                      <span>Ứng tuyển ngay</span>
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
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> vị trí)
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

export default function CareersPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo cổng cơ hội nghề nghiệp...
      </div>
    }>
      <CareersContent />
    </Suspense>
  );
}

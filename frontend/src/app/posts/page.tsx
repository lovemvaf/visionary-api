"use client";

import React, { useState, useEffect, useCallback, useRef, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import {
  BookOpen,
  Calendar,
  User,
  Search,
  ArrowRight,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  RotateCcw,
  Tag,
  FilterX
} from "lucide-react";
import { api } from "../../lib/api";
import { PostItem, PostCategory } from "../../lib/types";

function PostsPageContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  // Read initial state from URL query parameters
  const initialCategory = searchParams.get("category") || "";
  const initialSearch = searchParams.get("search") || "";
  const initialPage = parseInt(searchParams.get("page") || "1", 10);

  const [categories, setCategories] = useState<PostCategory[]>([]);
  const [selectedCat, setSelectedCat] = useState<string>(initialCategory);
  const [search, setSearch] = useState<string>(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState<string>(initialSearch);
  const [pageIndex, setPageIndex] = useState<number>(initialPage > 0 ? initialPage : 1);
  const pageSize = 9; // 3x3 responsive grid

  // Data state
  const [posts, setPosts] = useState<PostItem[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [hasNextPage, setHasNextPage] = useState<boolean>(false);
  const [hasPreviousPage, setHasPreviousPage] = useState<boolean>(false);

  // Status state: "loading" | "success" | "empty" | "error"
  const [status, setStatus] = useState<"loading" | "success" | "empty" | "error">("loading");
  const [errorMessage, setErrorMessage] = useState<string>("");

  // Request sequence guard to avoid race conditions
  const requestSeq = useRef(0);

  // Debounce search input by 300ms
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(timer);
  }, [search]);

  // Sync state to URL without reloading page
  const updateUrl = useCallback((cat: string, s: string, p: number) => {
    const params = new URLSearchParams();
    if (cat) params.set("category", cat);
    if (s.trim()) params.set("search", s.trim());
    if (p > 1) params.set("page", p.toString());
    const qs = params.toString();
    router.replace(`${pathname}${qs ? `?${qs}` : ""}`, { scroll: false });
  }, [pathname, router]);

  // Fetch categories on mount
  useEffect(() => {
    api.getCategories().then((res) => {
      if (res.success && res.data) {
        setCategories(res.data);
      }
    });
  }, []);

  // Fetch posts whenever selectedCat, debouncedSearch, or pageIndex changes
  const fetchPosts = useCallback(async () => {
    const currentSeq = ++requestSeq.current;
    setStatus("loading");
    setErrorMessage("");

    try {
      const res = await api.getPosts({
        categoryId: selectedCat || undefined,
        search: debouncedSearch.trim() || undefined,
        pageIndex,
        pageSize,
      });

      // Ignore stale response if user initiated newer request
      if (currentSeq !== requestSeq.current) return;

      if (res.success && res.data) {
        setPosts(res.data.items || []);
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
        setPosts([]);
        setStatus("error");
        setErrorMessage(res.message || "Không thể tải danh sách bài viết từ máy chủ.");
      }
    } catch (err: any) {
      if (currentSeq !== requestSeq.current) return;
      setPosts([]);
      setStatus("error");
      setErrorMessage(err?.message || "Lỗi kết nối đến máy chủ.");
    }
  }, [selectedCat, debouncedSearch, pageIndex, pageSize]);

  useEffect(() => {
    fetchPosts();
    updateUrl(selectedCat, debouncedSearch, pageIndex);
  }, [fetchPosts, updateUrl, selectedCat, debouncedSearch, pageIndex]);

  // Handlers
  const handleCategorySelect = (catId: string) => {
    if (selectedCat !== catId) {
      setSelectedCat(catId);
      setPageIndex(1);
    }
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setPageIndex(1);
  };

  const handleClearSearch = () => {
    setSearch("");
    setDebouncedSearch("");
    setPageIndex(1);
  };

  const handleResetFilters = () => {
    setSelectedCat("");
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

  // Determine active category name
  const activeCategoryName = categories.find((c) => c.id === selectedCat)?.name;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          VISIONARY News & CMS
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Tin tức Hội nhập & Thông báo Hoạt động
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Cập nhật thông tin công nghệ mới, thông báo từ Ban Chủ Nhiệm và các bài chia sẻ kinh nghiệm kỹ thuật từ nhóm VISIONARY API (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang).
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-surface-border">
        {/* Category Tabs */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <button
            onClick={() => handleCategorySelect("")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              selectedCat === ""
                ? "bg-visionary text-white shadow-sm"
                : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
            }`}
          >
            Tất cả danh mục
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => handleCategorySelect(cat.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                selectedCat === cat.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              <span>{cat.name}</span>
              <span className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                selectedCat === cat.id ? "bg-white/20 text-white" : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
              }`}>
                {cat.postCount}
              </span>
            </button>
          ))}
        </div>

        {/* Search input with clear button */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm theo tiêu đề, tóm tắt..."
            value={search}
            onChange={handleSearchChange}
            className="w-full pl-9 pr-8 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
          />
          {search && (
            <button
              onClick={handleClearSearch}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs font-bold"
              aria-label="Xóa từ khóa"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Results Header / Scope info */}
      <div className="flex items-center justify-between text-xs text-gray-500 border-b border-surface-border pb-3">
        <div>
          {status === "loading" ? (
            <span>Đang tải dữ liệu bài viết...</span>
          ) : activeCategoryName ? (
            <span>
              Danh mục: <strong className="text-navy dark:text-white">{activeCategoryName}</strong> ({totalCount} bài viết)
            </span>
          ) : (
            <span>
              Tất cả bài viết: <strong className="text-navy dark:text-white">{totalCount}</strong> bài đã công bố
              {totalCount > 0 && ` (Hiển thị ${(pageIndex - 1) * pageSize + 1}–${Math.min(pageIndex * pageSize, totalCount)})`}
            </span>
          )}
          {debouncedSearch.trim() && (
            <span className="ml-2">
              với từ khóa &quot;<strong>{debouncedSearch}</strong>&quot;
            </span>
          )}
        </div>

        {(selectedCat || debouncedSearch) && (
          <button
            onClick={handleResetFilters}
            className="inline-flex items-center gap-1 text-visionary dark:text-tealAccent hover:underline font-semibold"
          >
            <FilterX className="w-3.5 h-3.5" />
            <span>Xóa bộ lọc</span>
          </button>
        )}
      </div>

      {/* 1. LOADING STATE: Skeleton Loader Cards */}
      {status === "loading" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="glass-card rounded-2xl p-6 space-y-4 animate-pulse">
              <div className="flex items-center justify-between">
                <div className="h-4 w-24 bg-gray-200 dark:bg-gray-800 rounded-full" />
                <div className="h-3 w-16 bg-gray-200 dark:bg-gray-800 rounded-full" />
              </div>
              <div className="h-5 w-4/5 bg-gray-200 dark:bg-gray-800 rounded" />
              <div className="space-y-2">
                <div className="h-3 w-full bg-gray-200 dark:bg-gray-800 rounded" />
                <div className="h-3 w-5/6 bg-gray-200 dark:bg-gray-800 rounded" />
              </div>
              <div className="pt-4 border-t border-gray-100 dark:border-gray-800 flex justify-between items-center">
                <div className="h-3 w-28 bg-gray-200 dark:bg-gray-800 rounded" />
                <div className="h-3 w-16 bg-gray-200 dark:bg-gray-800 rounded" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 2. ERROR STATE: With Real Retry Action */}
      {status === "error" && (
        <div className="glass-card rounded-2xl p-10 text-center space-y-4 border border-red-200 dark:border-red-900/50 max-w-lg mx-auto">
          <div className="w-12 h-12 rounded-full bg-red-100 dark:bg-red-950/40 text-red-600 flex items-center justify-center mx-auto">
            <AlertCircle className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-navy dark:text-white">
            Không thể tải dữ liệu bài viết
          </h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {errorMessage || "Đã xảy ra lỗi khi kết nối đến máy chủ API. Vui lòng thử lại sau ít phút."}
          </p>
          <button
            onClick={() => fetchPosts()}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-visionary text-white text-xs font-semibold hover:bg-visionary/90 transition-all shadow-sm"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Thử lại</span>
          </button>
        </div>
      )}

      {/* 3. EMPTY STATE: Clear Informative Message */}
      {status === "empty" && (
        <div className="glass-card rounded-2xl p-12 text-center space-y-4 max-w-md mx-auto">
          <div className="w-12 h-12 rounded-full bg-gray-100 dark:bg-navy-light text-gray-400 flex items-center justify-center mx-auto">
            <BookOpen className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-navy dark:text-white">
            {debouncedSearch
              ? "Không tìm thấy bài viết phù hợp"
              : "Chưa có bài viết trong danh mục này"}
          </h3>
          <p className="text-xs text-gray-500">
            {debouncedSearch
              ? `Không có bài viết nào khớp với từ khóa "${debouncedSearch}". Hãy thử với từ khóa khác.`
              : "Chưa có nội dung bài viết nào phù hợp với bộ lọc hiện tại."}
          </p>
          {(selectedCat || debouncedSearch) && (
            <button
              onClick={handleResetFilters}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-navy-light text-xs font-semibold text-navy dark:text-gray-200 hover:bg-gray-200"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Xem tất cả danh mục</span>
            </button>
          )}
        </div>
      )}

      {/* 4. SUCCESS STATE: Posts Grid */}
      {status === "success" && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
              <div
                key={post.id}
                className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary dark:hover:border-tealAccent transition-all group border border-surface-border shadow-sm hover:shadow-md"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                      {post.categoryName}
                    </span>
                    <span className="text-[11px] text-gray-500 flex items-center gap-1">
                      <Calendar className="w-3 h-3 text-tealAccent" />
                      {post.publishedAt ? new Date(post.publishedAt).toLocaleDateString("vi-VN") : "Mới đăng"}
                    </span>
                  </div>

                  <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors line-clamp-2">
                    {post.title}
                  </h3>

                  <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                    {post.summary}
                  </p>
                </div>

                <div className="mt-6 pt-4 border-t border-surface-border flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs text-gray-500">
                    <User className="w-3.5 h-3.5 text-visionary" />
                    <span className="truncate max-w-[120px]">{post.authorName}</span>
                  </div>

                  <Link
                    href={`/posts/${post.slug}`}
                    className="text-xs font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1 group-hover:gap-1.5 transition-all"
                  >
                    <span>Đọc bài</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Unified Pagination Bar */}
          {totalPages > 1 && (
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-surface-border">
              <span className="text-xs text-gray-500">
                Trang <strong>{pageIndex}</strong> / <strong>{totalPages}</strong> (Tổng <strong>{totalCount}</strong> bài viết)
              </span>

              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => handlePageChange(pageIndex - 1)}
                  disabled={!hasPreviousPage}
                  className="px-3 py-1.5 rounded-lg border border-surface-border text-xs font-semibold text-navy dark:text-gray-200 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-navy-light flex items-center gap-1"
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
                          : "border border-surface-border text-navy dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-navy-light"
                      }`}
                    >
                      {pNum}
                    </button>
                  );
                })}

                <button
                  onClick={() => handlePageChange(pageIndex + 1)}
                  disabled={!hasNextPage}
                  className="px-3 py-1.5 rounded-lg border border-surface-border text-xs font-semibold text-navy dark:text-gray-200 disabled:opacity-30 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-navy-light flex items-center gap-1"
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

export default function PostsPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto px-4 py-12 text-center text-xs text-gray-500">
        Đang khởi tạo danh mục bài viết...
      </div>
    }>
      <PostsPageContent />
    </Suspense>
  );
}

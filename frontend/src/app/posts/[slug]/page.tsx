"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Calendar, User, Eye, Tag, AlertCircle, RotateCcw, BookOpen } from "lucide-react";
import { api } from "../../../lib/api";
import { PostItem } from "../../../lib/types";

export default function PostDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [post, setPost] = useState<PostItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>("");

  const fetchPost = () => {
    if (!slug) return;
    setLoading(true);
    setError("");

    api.getPostBySlug(slug)
      .then((res) => {
        setLoading(false);
        if (res.success && res.data) {
          setPost(res.data);
        } else {
          setPost(null);
          setError(res.message || "Không tìm thấy bài viết hoặc bài viết chưa được công bố.");
        }
      })
      .catch((err) => {
        setLoading(false);
        setPost(null);
        setError(err?.message || "Lỗi kết nối khi tải bài viết.");
      });
  };

  useEffect(() => {
    fetchPost();
  }, [slug]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8 animate-pulse">
        <div className="h-4 w-32 bg-gray-200 dark:bg-gray-800 rounded" />
        <div className="space-y-4">
          <div className="h-6 w-24 bg-gray-200 dark:bg-gray-800 rounded-full" />
          <div className="h-8 w-3/4 bg-gray-200 dark:bg-gray-800 rounded" />
          <div className="h-4 w-1/2 bg-gray-200 dark:bg-gray-800 rounded" />
        </div>
        <div className="glass-card rounded-2xl p-8 space-y-4">
          <div className="h-4 w-full bg-gray-200 dark:bg-gray-800 rounded" />
          <div className="h-4 w-5/6 bg-gray-200 dark:bg-gray-800 rounded" />
          <div className="h-4 w-4/6 bg-gray-200 dark:bg-gray-800 rounded" />
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="max-w-lg mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-950/40 text-amber-600 flex items-center justify-center mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-navy dark:text-white">
          {error || "Bài viết không tồn tại"}
        </h2>
        <p className="text-xs text-gray-500 dark:text-gray-400">
          Bài viết có thể đã bị gỡ, chuyển trạng thái bản nháp hoặc đường dẫn không chính xác.
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            onClick={fetchPost}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gray-100 dark:bg-navy-light text-xs font-semibold text-navy dark:text-gray-200 hover:bg-gray-200"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Thử lại</span>
          </button>
          <Link
            href="/posts"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-visionary text-white text-xs font-semibold hover:bg-visionary/90 shadow-sm"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Quay lại Tin tức</span>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      <Link
        href="/posts"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-visionary dark:text-tealAccent hover:underline"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Quay lại trang tin tức</span>
      </Link>

      <div className="space-y-4">
        <span className="badge-teal text-xs px-3 py-1 rounded-full font-bold">
          {post.categoryName}
        </span>

        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-navy dark:text-white leading-tight">
          {post.title}
        </h1>

        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500 pt-2 border-b border-surface-border pb-4">
          <div className="flex items-center gap-1.5">
            <User className="w-4 h-4 text-visionary" />
            <span>Tác giả: <strong>{post.authorName}</strong></span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar className="w-4 h-4 text-tealAccent" />
            <span>{post.publishedAt ? new Date(post.publishedAt).toLocaleDateString("vi-VN") : "Hôm nay"}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Eye className="w-4 h-4 text-gray-400" />
            <span>{post.viewCount} lượt xem</span>
          </div>
        </div>

        <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed italic border-l-4 border-tealAccent pl-4 py-1">
          {post.summary}
        </p>
      </div>

      <article className="prose dark:prose-invert max-w-none glass-card rounded-2xl p-8 space-y-4 text-xs sm:text-sm text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-line border border-surface-border">
        {post.contentMarkdown}
      </article>

      {post.tags && post.tags.length > 0 && (
        <div className="flex items-center gap-2 pt-4 border-t border-surface-border">
          <Tag className="w-4 h-4 text-gray-400" />
          <div className="flex flex-wrap gap-1.5">
            {post.tags.map((t) => (
              <span key={t} className="px-2.5 py-0.5 rounded-md bg-gray-100 dark:bg-navy-light text-xs text-gray-600 dark:text-gray-300">
                #{t}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { BookOpen, Calendar, User, Eye, Search, ArrowRight, Tag } from "lucide-react";
import { api } from "../../lib/api";
import { PostItem, PostCategory } from "../../lib/types";

export default function PostsPage() {
  const [posts, setPosts] = useState<PostItem[]>([]);
  const [categories, setCategories] = useState<PostCategory[]>([]);
  const [selectedCat, setSelectedCat] = useState<string>("");
  const [search, setSearch] = useState<string>("");

  const fallbackPosts: PostItem[] = [
    {
      id: "p1",
      categoryId: "c1",
      categoryName: "Công nghệ & AI",
      authorName: "Quách Khoa Đức",
      title: "Chào mừng đến với Hệ sinh thái VISIONARY DNTU 2026",
      slug: "chao-mung-he-sinh-thai-visionary-2026",
      summary: "VISIONARY là nền tảng tích hợp quản lý CLB Tiếng Anh, trung tâm học tập English for IT, radar công nghệ và cổng cơ hội quốc tế.",
      contentMarkdown: "Nền tảng kết nối toàn diện sinh viên và cơ hội quốc tế.",
      contentHtml: "<p>Nền tảng kết nối toàn diện sinh viên và cơ hội quốc tế.</p>",
      status: "Published",
      publishedAt: new Date().toISOString(),
      viewCount: 128,
      tags: ["DNTU", "Visionary", "Hội nhập"]
    },
    {
      id: "p2",
      categoryId: "c2",
      categoryName: "Tin Hội nhập",
      authorName: "Võ Ngọc Minh Đạt",
      title: "Kế hoạch Hoạt động & Sinh hoạt Định kỳ CLB Tiếng Anh DNTU Năm học 2025 - 2026",
      slug: "ke-hoach-hoat-dong-clb-tieng-anh-2025-2026",
      summary: "Lộ trình các buổi sinh hoạt chuyên ban, rèn luyện speaking hàng tuần và chương trình chuẩn bị cho các cuộc thi hùng biện tiếng Anh.",
      contentMarkdown: "Lịch trình sinh hoạt định kỳ chi tiết cho các bạn thành viên CLB.",
      contentHtml: "<p>Lịch trình sinh hoạt định kỳ chi tiết cho các bạn thành viên CLB.</p>",
      status: "Published",
      publishedAt: new Date().toISOString(),
      viewCount: 95,
      tags: ["CLB", "Sinh hoạt", "Speaking"]
    }
  ];

  useEffect(() => {
    api.getCategories().then((res) => {
      if (res.success && res.data?.length) setCategories(res.data);
    });

    api.getPosts({ categoryId: selectedCat || undefined, search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setPosts(res.data.items);
        } else {
          setPosts(fallbackPosts);
        }
      })
      .catch(() => setPosts(fallbackPosts));
  }, [selectedCat, search]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          VISIONARY News & CMS
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Tin tức Hội nhập & Thông báo Hoạt động
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Cập nhật những chuyển động công nghệ mới, thông báo từ Ban Chủ Nhiệm và các bài chia sẻ kinh nghiệm rèn luyện kỹ năng toàn cầu.
        </p>
      </div>

      {/* Filter and Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <button
            onClick={() => setSelectedCat("")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
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
              onClick={() => setSelectedCat(cat.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                selectedCat === cat.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>

        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm bài viết..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
          />
        </div>
      </div>

      {/* Posts Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div
            key={post.id}
            className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary transition-all group"
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

              <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                {post.title}
              </h3>

              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                {post.summary}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <div className="flex items-center gap-1.5 text-xs text-gray-500">
                <User className="w-3.5 h-3.5 text-visionary" />
                <span>{post.authorName}</span>
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
    </div>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Calendar, User, Eye, Share2, Tag } from "lucide-react";
import { api } from "../../../lib/api";
import { PostItem } from "../../../lib/types";

export default function PostDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [post, setPost] = useState<PostItem | null>(null);

  const defaultPost: PostItem = {
    id: "p1",
    categoryId: "c1",
    categoryName: "Công nghệ & AI",
    authorName: "Quách Khoa Đức",
    title: "Chào mừng đến với Hệ sinh thái VISIONARY DNTU 2026",
    slug: slug || "chao-mung-he-sinh-thai-visionary-2026",
    summary: "VISIONARY là nền tảng tích hợp quản lý CLB Tiếng Anh, trung tâm học tập English for IT, radar công nghệ và cổng cơ hội quốc tế.",
    contentMarkdown: `### 1. Giới thiệu Sứ mệnh VISIONARY
Hệ thống **VISIONARY** được thiết kế và triển khai nhằm giải quyết bài toán cốt lõi: Kết nối năng lực ngoại ngữ chuyên sâu với các công nghệ mũi nhọn trong kỷ nguyên số hóa và trí tuệ nhân tạo.

### 2. Các Trụ cột Hoạt động Chính
- **Quản trị CLB Tiếng Anh DNTU:** Tự động hóa quy trình xét duyệt thành viên, điểm danh số và lập báo cáo hoạt động.
- **English for IT:** Trung tâm học tập tương tác với các chủ đề REST API, AI/ML, Cloud & DevOps và luyện phỏng vấn kỹ thuật quốc tế.
- **Technology Radar:** Radar công nghệ mở cập nhật liên tục từ GitHub REST API và Hugging Face Hub.
- **Cơ hội & Việc làm:** Tổng hợp các sân chơi Hackathon, ICPC, học bổng ASEAN và cơ hội thực tập CNTT đòi hỏi ngoại ngữ.

### 3. Đội ngũ Kỹ thuật & Nghiên cứu
Dự án được thực hiện bởi nhóm **VISIONARY API** gồm 4 thành viên: Quách Khoa Đức (Lead), Võ Ngọc Minh Đạt, Hồ Đoàng Nguyên Khang, và Đào Trí Khang.`,
    contentHtml: "<p>Nội dung chi tiết hệ sinh thái VISIONARY DNTU 2026.</p>",
    status: "Published",
    publishedAt: new Date().toISOString(),
    viewCount: 185,
    tags: ["DNTU", "Visionary", "Hội nhập", "Web API"]
  };

  useEffect(() => {
    if (slug) {
      api.getPostBySlug(slug).then((res) => {
        if (res.success && res.data) {
          setPost(res.data);
        }
      });
    }
  }, [slug]);

  const p = post || defaultPost;

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
          {p.categoryName}
        </span>

        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-navy dark:text-white leading-tight">
          {p.title}
        </h1>

        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500 pt-2 border-b border-surface-border pb-4">
          <div className="flex items-center gap-1.5">
            <User className="w-4 h-4 text-visionary" />
            <span>Tác giả: <strong>{p.authorName}</strong></span>
          </div>
          <div className="flex items-center gap-1.5">
            <Calendar className="w-4 h-4 text-tealAccent" />
            <span>{p.publishedAt ? new Date(p.publishedAt).toLocaleDateString("vi-VN") : "Hôm nay"}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Eye className="w-4 h-4 text-gray-400" />
            <span>{p.viewCount} lượt xem</span>
          </div>
        </div>

        <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed italic border-l-4 border-tealAccent pl-4 py-1">
          {p.summary}
        </p>
      </div>

      <article className="prose dark:prose-invert max-w-none glass-card rounded-2xl p-8 space-y-4 text-xs sm:text-sm text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-line">
        {p.contentMarkdown}
      </article>

      {p.tags.length > 0 && (
        <div className="flex items-center gap-2 pt-4">
          <Tag className="w-4 h-4 text-gray-400" />
          <div className="flex flex-wrap gap-1.5">
            {p.tags.map((t) => (
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

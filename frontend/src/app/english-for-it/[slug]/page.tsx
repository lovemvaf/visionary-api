"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, BookOpen, Volume2, ExternalLink, Calendar, Eye, Share2 } from "lucide-react";
import { api } from "../../../lib/api";
import { LearningResource } from "../../../lib/types";

export default function EnglishForItDetailPage() {
  const params = useParams();
  const slug = params?.slug as string;
  const [resource, setResource] = useState<LearningResource | null>(null);

  useEffect(() => {
    if (slug) {
      api.getEnglishResourceBySlug(slug).then((res) => {
        if (res.success && res.data) {
          setResource(res.data);
        }
      });
    }
  }, [slug]);

  const defaultItem: LearningResource = {
    id: "1",
    title: "Essential REST API Terminology for Backend Engineers",
    slug: slug || "essential-rest-api-terminology",
    level: "Intermediate",
    topic: "REST API & Backend",
    summary: "Bộ thuật ngữ và mẫu câu phỏng vấn chuẩn quốc tế về RESTful API, HTTP Status Codes, Idempotency và JWT Authentication.",
    content: `### 1. Architectural Principles of REST
- **Statelessness (Phi trạng thái):** Mỗi request từ client gửi tới server phải chứa đầy đủ mọi thông tin cần thiết để server hiểu và xử lý. Server không lưu giữ bất kỳ session context nào giữa các request.
- **Client-Server Separation:** Giao diện người dùng và logic xử lý dữ liệu được tách biệt hoàn toàn thông qua giao thức chuẩn HTTP.

### 2. Deep Dive into Key Terminology
- **Idempotency (Tính bất biến):** Một phương thức HTTP được gọi là *idempotent* nếu việc gọi 1 lần hay 100 lần với cùng tham số đều tạo ra trạng thái tài nguyên giống nhau trên server. Các method: GET, PUT, DELETE, HEAD. Ngược lại, POST là *non-idempotent*.
- **Payload:** Khối dữ liệu thực sự được chuyên chở trong thân (body) của HTTP request hoặc response (thường ở định dạng JSON).
- **Rate Limiting & Throttling:** Cơ chế giới hạn số lượng request mà một client có thể gửi trong một khoảng thời gian nhằm ngăn chặn quá tải máy chủ hoặc tấn công DoS.

### 3. Professional Technical Interview Q&A
**Q: How do you explain the difference between PUT and PATCH?**
*A: "A PUT request is used to completely replace an existing resource with a new representation, and it is idempotent. In contrast, a PATCH request is applied to make partial modifications to a resource, updating only the specified fields."*`,
    glossaryJson: JSON.stringify([
      { term: "Idempotency", phonetic: "/ˌaɪ.dɛmˈpoʊ.təns/", meaning: "Tính bất biến khi gọi nhiều lần cùng một request", example: "PUT and DELETE methods must be strictly idempotent." },
      { term: "Payload", phonetic: "/ˈpeɪ.loʊd/", meaning: "Thân dữ liệu chuyên chở trong HTTP", example: "The JSON payload contains user profile attributes." },
      { term: "Statelessness", phonetic: "/ˈsteɪt.ləs.nəs/", meaning: "Đặc tính phi trạng thái của kiến trúc REST", example: "Statelessness enables horizontal scaling of API nodes." },
      { term: "Throttling", phonetic: "/ˈθrɒt.lɪŋ/", meaning: "Cơ chế điều tiết và giới hạn lưu lượng gọi API", example: "We implemented API throttling to protect downstream database queries." }
    ]),
    referenceUrl: "https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design",
    viewCount: 420,
    createdAt: new Date().toISOString()
  };

  const item = resource || defaultItem;
  let glossaries: any[] = [];
  try {
    if (item.glossaryJson) glossaries = JSON.parse(item.glossaryJson);
  } catch {}

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      <Link
        href="/english-for-it"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-visionary dark:text-tealAccent hover:underline"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Quay lại danh mục English for IT</span>
      </Link>

      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="badge-teal text-xs px-3 py-1 rounded-full font-bold">
            {item.level}
          </span>
          <span className="badge-blue text-xs px-3 py-1 rounded-full font-bold">
            {item.topic}
          </span>
        </div>

        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-navy dark:text-white leading-tight">
          {item.title}
        </h1>

        <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed italic border-l-4 border-tealAccent pl-4 py-1">
          {item.summary}
        </p>
      </div>

      {/* Glossary Section */}
      {glossaries.length > 0 && (
        <section className="glass-card rounded-2xl p-6 border-l-4 border-visionary space-y-4">
          <h2 className="text-base font-bold text-navy dark:text-white flex items-center gap-2">
            <Volume2 className="w-5 h-5 text-tealAccent" />
            <span>Thuật ngữ Kỹ thuật Chuyên sâu</span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {glossaries.map((g, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-surface dark:bg-navy-light space-y-1 text-xs">
                <div className="flex items-center justify-between font-bold text-visionary dark:text-tealAccent">
                  <span className="text-sm">{g.term}</span>
                  <span className="text-xs text-gray-400 font-normal italic">{g.phonetic}</span>
                </div>
                <div className="text-gray-700 dark:text-gray-200 font-medium">{g.meaning}</div>
                <div className="text-[11px] text-gray-500 italic mt-1 bg-white/60 dark:bg-navy/60 p-1.5 rounded">
                  &quot;{g.example}&quot;
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Main Content */}
      <article className="prose dark:prose-invert max-w-none glass-card rounded-2xl p-8 space-y-4 text-xs sm:text-sm text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-line">
        {item.content}
      </article>

      {item.referenceUrl && (
        <div className="glass-card p-4 rounded-xl flex items-center justify-between text-xs">
          <span className="text-gray-500">Tài liệu tham khảo chính thức:</span>
          <a
            href={item.referenceUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-visionary dark:text-tealAccent font-semibold hover:underline flex items-center gap-1"
          >
            <span>Microsoft Learn Official Docs</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      )}
    </div>
  );
}

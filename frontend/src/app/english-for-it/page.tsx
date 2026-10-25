"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { BookOpen, Search, Filter, Sparkles, ArrowRight, Volume2, Bookmark, CheckCircle2 } from "lucide-react";
import { api } from "../../lib/api";
import { LearningResource } from "../../lib/types";

export default function EnglishForItPage() {
  const [resources, setResources] = useState<LearningResource[]>([]);
  const [level, setLevel] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [loading, setLoading] = useState(true);

  const fallbackResources: LearningResource[] = [
    {
      id: "1",
      title: "Essential REST API Terminology for Backend Engineers",
      slug: "essential-rest-api-terminology",
      level: "Intermediate",
      topic: "REST API & Backend",
      summary: "Bộ thuật ngữ và mẫu câu phỏng vấn chuẩn quốc tế về RESTful API, HTTP Status Codes, Idempotency và JWT Authentication.",
      content: "Deep dive into statelessness, idempotency, and OAuth 2.0 standards.",
      glossaryJson: JSON.stringify([
        { term: "Idempotency", phonetic: "/ˌaɪ.dɛmˈpoʊ.təns/", meaning: "Tính bất biến khi gọi lại cùng một request", example: "PUT and DELETE are idempotent." },
        { term: "Payload", phonetic: "/ˈpeɪ.loʊd/", meaning: "Dữ liệu thực tế được truyền trong thân request/response", example: "The JSON payload contains user credentials." },
        { term: "Statelessness", phonetic: "/ˈsteɪt.ləs.nəs/", meaning: "Trạng thái không lưu session giữa client và server", example: "REST APIs must remain strictly stateless." }
      ]),
      viewCount: 342,
      createdAt: new Date().toISOString()
    },
    {
      id: "2",
      title: "Demystifying AI & LLM Terminology: RAG, Embeddings, Tokens",
      slug: "demystifying-ai-llm-terminology",
      level: "Advanced",
      topic: "AI & Machine Learning",
      summary: "Hiểu sâu thuật ngữ tiếng Anh trong kỷ nguyên GenAI: Retrieval-Augmented Generation (RAG), Vector Embeddings, và Context Window.",
      content: "Comprehensive breakdown of modern AI terminology.",
      glossaryJson: JSON.stringify([
        { term: "RAG", phonetic: "/ræɡ/", meaning: "Tạo sinh tăng cường truy xuất dữ liệu", example: "RAG grounds the model in enterprise documents." },
        { term: "Embeddings", phonetic: "/ɪmˈbɛd.ɪŋz/", meaning: "Biểu diễn ngữ nghĩa bằng vector số học", example: "High-dimensional embeddings enable semantic similarity search." },
        { term: "Hallucination", phonetic: "/həˌluː.sɪˈneɪ.ʃən/", meaning: "Hiện tượng mô hình AI bịa đặt thông tin sai lệch", example: "Prompt engineering reduces hallucinations." }
      ]),
      viewCount: 512,
      createdAt: new Date().toISOString()
    },
    {
      id: "3",
      title: "Git & GitHub Collaboration Vocabulary for Global Agile Teams",
      slug: "git-github-collaboration-vocabulary",
      level: "Beginner",
      topic: "DevOps & Tools",
      summary: "Nắm vững các thuật ngữ Commit, Rebase, Cherry-pick, Pull Request và cách diễn đạt báo cáo tiến độ bằng tiếng Anh.",
      content: "Agile communication skills for global tech collaboration.",
      glossaryJson: JSON.stringify([
        { term: "Merge Conflict", phonetic: "/mɜːrdʒ ˈkɒn.flɪkt/", meaning: "Xung đột dòng mã nguồn khi gộp nhánh", example: "We resolved the merge conflict before merging to main." },
        { term: "Pull Request (PR)", phonetic: "/pʊl rɪˈkwɛst/", meaning: "Yêu cầu xem xét và gộp mã nguồn", example: "Please review my PR and approve it." }
      ]),
      viewCount: 220,
      createdAt: new Date().toISOString()
    }
  ];

  useEffect(() => {
    setLoading(true);
    api.getEnglishResources({ level: level || undefined, search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setResources(res.data.items);
        } else {
          setResources(fallbackResources);
        }
      })
      .catch(() => setResources(fallbackResources))
      .finally(() => setLoading(false));
  }, [level, search]);

  const levels = ["", "Beginner", "Intermediate", "Advanced", "Professional"];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          VISIONARY Learning Center
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          English for IT – Tiếng Anh Chuyên ngành CNTT
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Chương trình học thuật ngữ thực chiến, rèn luyện kỹ năng phỏng vấn kỹ thuật và viết tài liệu quốc tế dành riêng cho sinh viên DNTU.
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-card p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Level Filters */}
        <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto">
          {levels.map((lvl) => (
            <button
              key={lvl}
              onClick={() => setLevel(lvl)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                level === lvl
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {lvl === "" ? "Tất cả cấp độ" : lvl}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm bài học, thuật ngữ..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
          />
        </div>
      </div>

      {/* Resources Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((item) => {
          let glossaries: any[] = [];
          try {
            if (item.glossaryJson) glossaries = JSON.parse(item.glossaryJson);
          } catch {}

          return (
            <div
              key={item.id}
              className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-tealAccent transition-all group"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="badge-teal text-[10px] px-2.5 py-0.5 rounded-full font-bold">
                    {item.level}
                  </span>
                  <span className="text-[11px] text-gray-500 font-medium">{item.topic}</span>
                </div>

                <h3 className="text-base font-bold text-navy dark:text-white group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors">
                  {item.title}
                </h3>

                <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                  {item.summary}
                </p>

                {/* Vocabulary Preview */}
                {glossaries.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800 space-y-2">
                    <div className="text-[11px] uppercase tracking-wider font-bold text-gray-400">
                      Thuật ngữ trọng tâm:
                    </div>
                    <div className="space-y-1.5">
                      {glossaries.slice(0, 2).map((g, idx) => (
                        <div key={idx} className="p-2 rounded-lg bg-surface dark:bg-navy-light text-xs">
                          <div className="font-bold text-navy dark:text-tealAccent flex items-center justify-between">
                            <span>{g.term}</span>
                            <span className="text-[10px] text-gray-400 font-normal italic">{g.phonetic}</span>
                          </div>
                          <div className="text-[11px] text-gray-600 dark:text-gray-300 mt-0.5">{g.meaning}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <Link
                href={`/english-for-it/${item.slug}`}
                className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-visionary dark:text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
              >
                <span>Học bài giảng chi tiết</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          );
        })}
      </div>
    </div>
  );
}

"use client";

import React, { useState, useEffect } from "react";
import { Radio, Search, Star, GitFork, ExternalLink, RefreshCw, Sparkles, Shield, Cpu } from "lucide-react";
import { api } from "../../lib/api";
import { TechResource } from "../../lib/types";

export default function TechRadarPage() {
  const [resources, setResources] = useState<TechResource[]>([]);
  const [sourceType, setSourceType] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState("");

  const fallbackTech: TechResource[] = [
    {
      id: "1",
      name: "dotnet/aspnetcore",
      sourceType: "GitHubRepository",
      officialUrl: "https://github.com/dotnet/aspnetcore",
      description: "ASP.NET Core is a cross-platform, high-performance, open-source framework for building modern, cloud-enabled, Internet-connected apps.",
      primaryLanguage: "C#",
      license: "MIT",
      metricsJson: JSON.stringify({ stars: 36800, forks: 9600 }),
      learningSuitability: "Advanced / Core Web API",
      lastCheckedAt: new Date().toISOString(),
      isVerified: true
    },
    {
      id: "2",
      name: "vercel/next.js",
      sourceType: "GitHubRepository",
      officialUrl: "https://github.com/vercel/next.js",
      description: "The React Framework for the Web. Used by some of the world's largest companies, Next.js enables you to create full-stack Web applications.",
      primaryLanguage: "TypeScript",
      license: "MIT",
      metricsJson: JSON.stringify({ stars: 127000, forks: 27000 }),
      learningSuitability: "Intermediate / Full-Stack",
      lastCheckedAt: new Date().toISOString(),
      isVerified: true
    },
    {
      id: "3",
      name: "meta-llama/Llama-3-8B",
      sourceType: "HuggingFaceModel",
      officialUrl: "https://huggingface.co/meta-llama/Meta-Llama-3-8B",
      description: "Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models.",
      primaryLanguage: "Python / PyTorch",
      license: "Llama 3 Community",
      metricsJson: JSON.stringify({ downloads: 1450000, likes: 7800 }),
      learningSuitability: "AI / GenAI & RAG",
      lastCheckedAt: new Date().toISOString(),
      isVerified: true
    },
    {
      id: "4",
      name: "microsoft/playwright",
      sourceType: "GitHubRepository",
      officialUrl: "https://github.com/microsoft/playwright",
      description: "Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API.",
      primaryLanguage: "TypeScript",
      license: "Apache-2.0",
      metricsJson: JSON.stringify({ stars: 68500, forks: 3900 }),
      learningSuitability: "QA Automation & Testing",
      lastCheckedAt: new Date().toISOString(),
      isVerified: true
    }
  ];

  useEffect(() => {
    api.getTechResources({ sourceType: sourceType || undefined, search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setResources(res.data.items);
        } else {
          setResources(fallbackTech);
        }
      })
      .catch(() => setResources(fallbackTech));
  }, [sourceType, search]);

  const handleSync = async () => {
    setIsSyncing(true);
    setSyncMessage("");
    const res = await api.syncTechResources("All");
    if (res.success) {
      setSyncMessage("Đã kích hoạt đồng bộ dữ liệu tự động từ GitHub và Hugging Face!");
      // reload
      api.getTechResources().then((r) => {
        if (r.success && r.data?.items) setResources(r.data.items);
      });
    } else {
      setSyncMessage(res.message || "Cần quyền Admin để chạy đồng bộ trực tiếp.");
    }
    setIsSyncing(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-surface-border pb-8">
        <div className="space-y-2">
          <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
            Open-Source & Trends
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
            VISIONARY Technology Radar
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-300 max-w-2xl">
            Cập nhật xu hướng công nghệ, kho mã nguồn mở GitHub chất lượng cao và các mô hình AI/LLM mới nhất từ Hugging Face Hub phục vụ học tập và nghiên cứu.
          </p>
        </div>

        <button
          onClick={handleSync}
          disabled={isSyncing}
          className="self-start md:self-auto px-4 py-2.5 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-semibold shadow-md flex items-center gap-2 hover:scale-[1.02] transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? "animate-spin" : ""}`} />
          <span>{isSyncing ? "Đang đồng bộ..." : "Đồng bộ Nguồn mới"}</span>
        </button>
      </div>

      {syncMessage && (
        <div className="p-3 rounded-xl bg-tealAccent/10 border border-tealAccent/30 text-xs text-tealAccent font-semibold flex items-center gap-2">
          <Sparkles className="w-4 h-4 flex-shrink-0" />
          <span>{syncMessage}</span>
        </div>
      )}

      {/* Filter and Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          {[
            { id: "", label: "Tất cả nguồn" },
            { id: "GitHubRepository", label: "GitHub Repositories" },
            { id: "HuggingFaceModel", label: "Hugging Face Models" }
          ].map((type) => (
            <button
              key={type.id}
              onClick={() => setSourceType(type.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                sourceType === type.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {type.label}
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Tìm theo tên, ngôn ngữ, mô tả..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none focus:border-tealAccent"
          />
        </div>
      </div>

      {/* Radar Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {resources.map((item) => {
          let metrics: any = {};
          try {
            if (item.metricsJson) metrics = JSON.parse(item.metricsJson);
          } catch {}

          const isGitHub = item.sourceType === "GitHubRepository";

          return (
            <div
              key={item.id}
              className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary transition-all group"
            >
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold ${
                    isGitHub ? "badge-blue" : "badge-teal"
                  }`}>
                    {isGitHub ? "GitHub Repo" : "Hugging Face Model"}
                  </span>
                  <span className="text-[11px] px-2 py-0.5 rounded bg-gray-100 dark:bg-navy-light text-gray-600 dark:text-gray-300 font-medium">
                    {item.license || "Open"}
                  </span>
                </div>

                <div>
                  <h3 className="text-base font-bold text-navy dark:text-white flex items-center justify-between">
                    <span className="group-hover:text-visionary dark:group-hover:text-tealAccent transition-colors truncate">
                      {item.name}
                    </span>
                    <a
                      href={item.officialUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-gray-400 hover:text-visionary ml-2 flex-shrink-0"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  </h3>
                  {item.learningSuitability && (
                    <div className="text-[11px] text-tealAccent font-semibold mt-1">
                      Mức phù hợp: {item.learningSuitability}
                    </div>
                  )}
                </div>

                <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed line-clamp-3">
                  {item.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs">
                <span className="font-semibold text-navy dark:text-gray-200">
                  {item.primaryLanguage || "Đa ngôn ngữ"}
                </span>

                <div className="flex items-center gap-3 text-gray-500">
                  {metrics.stars !== undefined && (
                    <span className="flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 text-amber-400" />
                      {metrics.stars.toLocaleString()}
                    </span>
                  )}
                  {metrics.forks !== undefined && (
                    <span className="flex items-center gap-1">
                      <GitFork className="w-3.5 h-3.5" />
                      {metrics.forks.toLocaleString()}
                    </span>
                  )}
                  {metrics.likes !== undefined && (
                    <span className="flex items-center gap-1 text-tealAccent font-semibold">
                      ♥ {metrics.likes.toLocaleString()}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

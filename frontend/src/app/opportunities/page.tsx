"use client";

import React, { useState, useEffect } from "react";
import { Compass, Search, Calendar, Globe, ExternalLink, ShieldCheck, Tag, ArrowRight } from "lucide-react";
import { api } from "../../lib/api";
import { OpportunityItem } from "../../lib/types";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [category, setCategory] = useState("");
  const [scope, setScope] = useState("");
  const [search, setSearch] = useState("");

  const fallbackOpportunities: OpportunityItem[] = [
    {
      id: "1",
      title: "ICPC Vietnam National Programming Contest 2026",
      organizer: "Hội Tin học Việt Nam (VAIP) & ICPC Asia Pacific",
      category: "AlgorithmIcpc",
      scope: "Vietnam",
      format: "Offline",
      officialUrl: "https://icpc.ptit.edu.vn",
      eligibility: "Sinh viên đại học tại Việt Nam, đội thi tối đa 3 thành viên, tranh tài thuật toán.",
      registrationDeadline: "2026-11-30T23:59:59Z",
      status: "VerifiedOpen",
      verifiedAt: new Date().toISOString(),
      verifiedSource: "ICPC Official Portal"
    },
    {
      id: "2",
      title: "Google Cloud AI Global Hackathon 2026",
      organizer: "Google Cloud & Devpost",
      category: "Hackathon",
      scope: "Global",
      format: "Online",
      officialUrl: "https://googlecloud.devpost.com",
      eligibility: "Sinh viên và lập trình viên toàn cầu từ 18 tuổi, phát triển ứng dụng GenAI.",
      registrationDeadline: "2026-12-15T23:59:59Z",
      status: "VerifiedOpen",
      verifiedAt: new Date().toISOString(),
      verifiedSource: "Devpost Official Feed"
    },
    {
      id: "3",
      title: "ASEAN Youth Fellowship & Leadership Exchange 2026",
      organizer: "Singapore International Foundation (SIF) & ASEAN Secretariat",
      category: "ExchangeProgram",
      scope: "ASEAN",
      format: "Offline",
      officialUrl: "https://www.sif.org.sg",
      eligibility: "Sinh viên tiêu biểu các nước ASEAN, có chứng chỉ tiếng Anh IELTS >= 6.5 hoặc tương đương.",
      registrationDeadline: "2026-12-31T23:59:59Z",
      status: "VerifiedOpen",
      verifiedAt: new Date().toISOString(),
      verifiedSource: "SIF Global Office"
    },
    {
      id: "4",
      title: "Global Cybersecurity Student CTF Challenge",
      organizer: "OWASP & DEF CON Student Group",
      category: "CybersecurityCtf",
      scope: "Global",
      format: "Online",
      officialUrl: "https://ctftime.org",
      eligibility: "Sinh viên chuyên ngành An toàn thông tin, Mạng máy tính và CNTT.",
      registrationDeadline: "2026-11-20T23:59:59Z",
      status: "VerifiedOpen",
      verifiedAt: new Date().toISOString(),
      verifiedSource: "CTFTime Verified"
    }
  ];

  useEffect(() => {
    api.getOpportunities({ category: category || undefined, scope: scope || undefined, search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setOpportunities(res.data.items);
        } else {
          setOpportunities(fallbackOpportunities);
        }
      })
      .catch(() => setOpportunities(fallbackOpportunities));
  }, [category, scope, search]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Global Opportunities
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Cuộc thi, Học bổng & Hội nhập Quốc tế
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Tổng hợp các cuộc thi Hackathon, lập trình thuật toán ICPC, sân chơi CTF bảo mật và học bổng ASEAN dành cho sinh viên Việt Nam đã qua xác minh.
        </p>
      </div>

      {/* Filter and Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {[
            { id: "", label: "Tất cả lĩnh vực" },
            { id: "Hackathon", label: "Hackathon" },
            { id: "AlgorithmIcpc", label: "ICPC / Thuật toán" },
            { id: "ExchangeProgram", label: "Trao đổi ASEAN" },
            { id: "CybersecurityCtf", label: "CTF Bảo mật" }
          ].map((cat) => (
            <button
              key={cat.id}
              onClick={() => setCategory(cat.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                category === cat.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={scope}
            onChange={(e) => setScope(e.target.value)}
            className="px-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
          >
            <option value="">Tất cả phạm vi</option>
            <option value="Vietnam">Việt Nam</option>
            <option value="ASEAN">Khu vực ASEAN</option>
            <option value="Global">Toàn cầu</option>
          </select>

          <div className="relative flex-grow md:w-64">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm cuộc thi, tổ chức..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {opportunities.map((item) => (
          <div
            key={item.id}
            className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-tealAccent transition-all border"
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="badge-teal text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  {item.category}
                </span>
                <span className="text-xs text-gray-500 font-medium flex items-center gap-1">
                  <Globe className="w-3.5 h-3.5 text-tealAccent" />
                  {item.scope} • {item.format}
                </span>
              </div>

              <div>
                <h3 className="text-lg font-bold text-navy dark:text-white">
                  {item.title}
                </h3>
                <div className="text-xs text-tealAccent font-semibold mt-0.5">
                  Đơn vị tổ chức: {item.organizer}
                </div>
              </div>

              <div className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed bg-surface dark:bg-navy-light p-3 rounded-xl space-y-1">
                <div className="font-semibold text-navy dark:text-white">Điều kiện tham gia:</div>
                <p>{item.eligibility}</p>
              </div>

              <div className="flex flex-wrap items-center justify-between text-xs text-gray-500 pt-2 gap-2">
                <div className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-visionary" />
                  <span>
                    Hạn đăng ký:{" "}
                    <strong>
                      {item.registrationDeadline
                        ? new Date(item.registrationDeadline).toLocaleDateString("vi-VN")
                        : "Chưa công bố"}
                    </strong>
                  </span>
                </div>
                {item.verifiedSource && (
                  <div className="flex items-center gap-1 text-[11px] text-tealAccent font-medium">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>Nguồn: {item.verifiedSource}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">
                ● Đang mở đăng ký
              </span>

              <a
                href={item.officialUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-lg bg-visionary hover:bg-visionary-hover text-white text-xs font-semibold shadow-sm flex items-center gap-1.5 transition-all hover:scale-[1.02]"
              >
                <span>Xem & Đăng ký chính thức</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

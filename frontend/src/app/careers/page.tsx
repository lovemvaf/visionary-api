"use client";

import React, { useState, useEffect } from "react";
import { Briefcase, MapPin, Building, ExternalLink, Search, CheckCircle, Sparkles } from "lucide-react";
import { api } from "../../lib/api";
import { JobItem } from "../../lib/types";

export default function CareersPage() {
  const [jobs, setJobs] = useState<JobItem[]>([]);
  const [jobType, setJobType] = useState("");
  const [workplaceType, setWorkplaceType] = useState("");
  const [search, setSearch] = useState("");

  const fallbackJobs: JobItem[] = [
    {
      id: "1",
      title: "Software Engineering Intern (.NET / C#)",
      company: "FPT Software Global Delivery",
      jobType: "Internship",
      workplaceType: "Hybrid",
      location: "Dong Nai / HCM",
      applyUrl: "https://career.fpt-software.com",
      requirements: "Nắm vững C#, OOP, ASP.NET Core Web API cơ bản. Tiếng Anh giao tiếp hoặc đọc hiểu tài liệu chuyên ngành tốt.",
      englishRequired: true,
      isVerified: true,
      createdAt: new Date().toISOString()
    },
    {
      id: "2",
      title: "Frontend Engineer Fresher (Next.js / TypeScript)",
      company: "VNG Corporation",
      jobType: "Fresher",
      workplaceType: "Onsite",
      location: "Ho Chi Minh City",
      applyUrl: "https://careers.vng.com.vn",
      requirements: "Kinh nghiệm với React, Next.js App Router, Tailwind CSS. Năng động, tư duy hội nhập và khả năng làm việc nhóm tốt.",
      englishRequired: true,
      isVerified: true,
      createdAt: new Date().toISOString()
    },
    {
      id: "3",
      title: "AI & Data Engineer Intern",
      company: "NashTech Global Vietnam",
      jobType: "Internship",
      workplaceType: "Hybrid",
      location: "Ho Chi Minh City",
      applyUrl: "https://nashtechglobal.com/careers",
      requirements: "Hiểu biết về Python, SQL, REST API, kiến thức cơ bản về Machine Learning hoặc GenAI. Tiếng Anh đạt yêu cầu giao tiếp với khách hàng quốc tế.",
      englishRequired: true,
      isVerified: true,
      createdAt: new Date().toISOString()
    },
    {
      id: "4",
      title: "QA Automation Engineer Junior",
      company: "KMS Technology Vietnam",
      jobType: "Junior",
      workplaceType: "Remote",
      location: "Vietnam (Remote)",
      applyUrl: "https://kms-technology.com/careers",
      requirements: "Kiến thức về Playwright, Selenium, C# hoặc Java. Viết test case bằng tiếng Anh thành thạo.",
      englishRequired: true,
      isVerified: true,
      createdAt: new Date().toISOString()
    }
  ];

  useEffect(() => {
    api.getJobs({ jobType: jobType || undefined, workplaceType: workplaceType || undefined, search: search || undefined })
      .then((res) => {
        if (res.success && res.data?.items?.length) {
          setJobs(res.data.items);
        } else {
          setJobs(fallbackJobs);
        }
      })
      .catch(() => setJobs(fallbackJobs));
  }, [jobType, workplaceType, search]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Title */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          VISIONARY Career Gateway
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-navy dark:text-white tracking-tight">
          Cổng Việc làm & Thực tập Quốc tế
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Kết nối các vị trí Thực tập sinh, Fresher và Junior CNTT đòi hỏi năng lực tiếng Anh chuyên ngành; ứng tuyển trực tiếp tại cổng tuyển dụng chính thức của doanh nghiệp.
        </p>
      </div>

      {/* Filter and Search */}
      <div className="glass-card p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {[
            { id: "", label: "Tất cả vị trí" },
            { id: "Internship", label: "Thực tập (Internship)" },
            { id: "Fresher", label: "Fresher" },
            { id: "Junior", label: "Junior" }
          ].map((type) => (
            <button
              key={type.id}
              onClick={() => setJobType(type.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                jobType === type.id
                  ? "bg-visionary text-white shadow-sm"
                  : "bg-gray-100 dark:bg-navy-light text-navy dark:text-gray-200 hover:bg-gray-200"
              }`}
            >
              {type.label}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 w-full md:w-auto">
          <select
            value={workplaceType}
            onChange={(e) => setWorkplaceType(e.target.value)}
            className="px-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
          >
            <option value="">Tất cả hình thức</option>
            <option value="Remote">Remote (Từ xa)</option>
            <option value="Hybrid">Hybrid (Linh hoạt)</option>
            <option value="Onsite">Onsite (Tại văn phòng)</option>
          </select>

          <div className="relative flex-grow md:w-64">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm theo vị trí, công ty..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-surface-border bg-white dark:bg-navy text-navy dark:text-white focus:outline-none"
            />
          </div>
        </div>
      </div>

      {/* Jobs Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-visionary transition-all"
          >
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="badge-blue text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  {job.jobType}
                </span>
                <span className="text-xs text-gray-500 font-medium">
                  {job.workplaceType}
                </span>
              </div>

              <div>
                <h3 className="text-lg font-bold text-navy dark:text-white">
                  {job.title}
                </h3>
                <div className="flex items-center gap-2 text-xs text-gray-600 dark:text-gray-300 mt-1">
                  <Building className="w-3.5 h-3.5 text-visionary" />
                  <span className="font-semibold">{job.company}</span>
                  <span>•</span>
                  <MapPin className="w-3.5 h-3.5 text-tealAccent" />
                  <span>{job.location}</span>
                </div>
              </div>

              <div className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed bg-surface dark:bg-navy-light p-3 rounded-xl space-y-1">
                <div className="font-semibold text-navy dark:text-white">Yêu cầu cốt lõi:</div>
                <p>{job.requirements}</p>
              </div>

              {job.englishRequired && (
                <div className="flex items-center gap-1.5 text-xs text-tealAccent font-semibold">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Yêu cầu Tiếng Anh chuyên ngành hoặc giao tiếp</span>
                </div>
              )}
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <span className="text-xs text-emerald-600 dark:text-emerald-400 font-semibold">
                ● Đang tuyển dụng
              </span>

              <a
                href={job.applyUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-lg bg-visionary hover:bg-visionary-hover text-white text-xs font-semibold shadow-sm flex items-center gap-1.5 transition-all hover:scale-[1.02]"
              >
                <span>Nộp đơn tại Website Doanh nghiệp</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

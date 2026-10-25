import React from "react";
import Link from "next/link";
import {
  Globe,
  BookOpen,
  Radio,
  Compass,
  Briefcase,
  Award,
  Calendar,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Users,
  ShieldCheck,
  Star,
  GitFork,
  ExternalLink,
  ChevronRight
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="space-y-16 pb-20">
      {/* 1. Hero Section */}
      <section className="relative overflow-hidden hero-gradient pt-16 pb-20 lg:pt-24 lg:pb-32 border-b border-surface-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full badge-teal text-xs font-semibold uppercase tracking-wider animate-pulse">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Hệ sinh thái Hội nhập Quốc tế DNTU 2026</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-navy dark:text-white leading-[1.15]">
              Connecting Students,{" "}
              <span className="bg-gradient-to-r from-visionary to-tealAccent bg-clip-text text-transparent">
                Technology
              </span>{" "}
              & Global Opportunities
            </h1>

            <p className="text-base sm:text-lg text-gray-600 dark:text-gray-300 leading-relaxed">
              VISIONARY là nền tảng số hóa quản lý hoạt động Câu lạc bộ Tiếng Anh DNTU, trung tâm học tập English for IT, Radar công nghệ mở và cổng kết nối việc làm, học bổng toàn cầu.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <Link
                href="/english-for-it"
                className="px-6 py-3 rounded-xl bg-visionary hover:bg-visionary-hover text-white font-semibold text-sm shadow-lg shadow-visionary/25 hover:shadow-xl transition-all flex items-center gap-2 hover:scale-[1.02]"
              >
                <BookOpen className="w-4 h-4 text-tealAccent" />
                <span>Học English for IT</span>
              </Link>

              <Link
                href="/about"
                className="px-6 py-3 rounded-xl bg-white dark:bg-navy-light text-navy dark:text-white border border-surface-border font-semibold text-sm hover:bg-gray-50 dark:hover:bg-navy transition-all flex items-center gap-2 hover:scale-[1.02]"
              >
                <Users className="w-4 h-4 text-tealAccent" />
                <span>Gia nhập CLB DNTU</span>
              </Link>

              <Link
                href="/tech-radar"
                className="px-6 py-3 rounded-xl glass-card text-navy dark:text-white font-semibold text-sm hover:border-tealAccent transition-all flex items-center gap-2 hover:scale-[1.02]"
              >
                <Radio className="w-4 h-4 text-tealAccent" />
                <span>Khám phá Tech Radar</span>
              </Link>
            </div>
          </div>

          {/* Quick Metrics Strip */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            <div className="glass-card p-5 rounded-2xl text-center shadow-sm hover:shadow-md transition-shadow border-t-2 border-tealAccent">
              <div className="text-3xl font-extrabold text-navy dark:text-white">100%</div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-medium">Một API Ba Nền tảng</div>
            </div>
            <div className="glass-card p-5 rounded-2xl text-center shadow-sm hover:shadow-md transition-shadow border-t-2 border-visionary">
              <div className="text-3xl font-extrabold text-navy dark:text-white">4</div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-medium">Trụ cột Chuyên môn CLB</div>
            </div>
            <div className="glass-card p-5 rounded-2xl text-center shadow-sm hover:shadow-md transition-shadow border-t-2 border-tealAccent">
              <div className="text-3xl font-extrabold text-navy dark:text-white">100+</div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-medium">Thuật ngữ & Bài học IT</div>
            </div>
            <div className="glass-card p-5 rounded-2xl text-center shadow-sm hover:shadow-md transition-shadow border-t-2 border-visionary">
              <div className="text-3xl font-extrabold text-navy dark:text-white">24/7</div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 font-medium">Tự động Cập nhật Nguồn</div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Core Pillars Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h2 className="text-xs uppercase tracking-widest font-bold text-tealAccent mb-2">
            Hệ sinh thái Toàn diện
          </h2>
          <h3 className="text-2xl sm:text-3xl font-bold text-navy dark:text-white">
            6 Trụ cột Đột phá Dành cho Sinh viên DNTU
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Pillar 1: Visionary Club */}
          <div className="glass-card p-6 rounded-2xl hover:border-visionary transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-visionary/10 text-visionary flex items-center justify-center group-hover:scale-110 transition-transform">
                <Users className="w-6 h-6 text-visionary" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Cổng Quản trị CLB Tiếng Anh</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Số hóa toàn diện: nộp đơn gia nhập trực tuyến, xét duyệt minh bạch, điểm danh mã QR động và quản lý lịch hoạt động nội bộ.
              </p>
            </div>
            <Link
              href="/about"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-visionary dark:text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Xem thông tin CLB</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Pillar 2: English for IT */}
          <div className="glass-card p-6 rounded-2xl hover:border-tealAccent transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-tealAccent/10 text-tealAccent flex items-center justify-center group-hover:scale-110 transition-transform">
                <BookOpen className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Trung tâm English for IT</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Học tiếng Anh gắn liền thực tế: thuật ngữ REST API, AI/ML, Cloud DevOps, văn phong viết tài liệu và luyện phỏng vấn kỹ thuật quốc tế.
              </p>
            </div>
            <Link
              href="/english-for-it"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Vào chuyên mục bài học</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Pillar 3: Technology Radar */}
          <div className="glass-card p-6 rounded-2xl hover:border-visionary transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Radio className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Technology Radar</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Theo dõi xu hướng công nghệ nóng, khám phá kho GitHub repos hàng đầu và các mô hình AI/LLM mới nhất từ Hugging Face Hub.
              </p>
            </div>
            <Link
              href="/tech-radar"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-visionary dark:text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Xem Technology Radar</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Pillar 4: Opportunities */}
          <div className="glass-card p-6 rounded-2xl hover:border-tealAccent transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Compass className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Cuộc thi & Hội nhập</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Tổng hợp Hackathon, AI Challenge, ICPC, học bổng quốc tế và các chương trình giao lưu thanh niên ASEAN có kiểm chứng.
              </p>
            </div>
            <Link
              href="/opportunities"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Tìm kiếm cuộc thi</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Pillar 5: Career Gateway */}
          <div className="glass-card p-6 rounded-2xl hover:border-visionary transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Briefcase className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Career Gateway</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Cổng cơ hội thực tập, Fresher CNTT và các vị trí đòi hỏi tiếng Anh; dẫn link nộp đơn trực tiếp tại cổng tuyển dụng chính thức.
              </p>
            </div>
            <Link
              href="/careers"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-visionary dark:text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Khám phá việc làm</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Pillar 6: Hall of Achievement */}
          <div className="glass-card p-6 rounded-2xl hover:border-tealAccent transition-all group flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Award className="w-6 h-6" />
              </div>
              <h4 className="text-lg font-bold text-navy dark:text-white">Bảng vàng Thành tích</h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Tôn vinh và lưu danh những thành tích xuất sắc trong học thuật, giải thưởng công nghệ, chứng chỉ ngoại ngữ và đóng góp cộng đồng.
              </p>
            </div>
            <Link
              href="/achievements"
              className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 text-xs font-semibold text-tealAccent flex items-center gap-1 group-hover:gap-2 transition-all"
            >
              <span>Xem bảng vinh danh</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </section>

      {/* 3. Upcoming Events & Activities Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <span className="text-xs uppercase tracking-widest font-bold text-tealAccent">
              Sự kiện Nổi bật
            </span>
            <h3 className="text-2xl font-bold text-navy dark:text-white mt-1">
              Hoạt động CLB & Tọa đàm Quốc tế
            </h3>
          </div>
          <Link
            href="/events"
            className="text-xs font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Xem tất cả sự kiện</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-card rounded-2xl p-6 border-l-4 border-visionary flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="badge-teal text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  Sắp diễn ra
                </span>
                <span className="text-xs text-gray-500 flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-tealAccent" />
                  Chủ nhật tới • 08:30
                </span>
              </div>
              <h4 className="text-base font-bold text-navy dark:text-white">
                VISIONARY Tech & English Talk 2026: Lộ trình làm chủ AI và Hội nhập Toàn cầu
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Tọa đàm chuyên sâu về phương pháp kết hợp tiếng Anh chuyên ngành với công nghệ Web API và GenAI để mở rộng cơ hội việc làm quốc tế.
              </p>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Địa điểm: <strong>Hội trường Edison, DNTU & Online MS Teams</strong>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <span className="text-xs text-gray-500 font-medium">Giới hạn: 150 chỗ</span>
              <Link
                href="/events"
                className="px-4 py-2 rounded-lg bg-visionary hover:bg-visionary-hover text-white text-xs font-semibold shadow-sm"
              >
                Đăng ký ngay
              </Link>
            </div>
          </div>

          <div className="glass-card rounded-2xl p-6 border-l-4 border-tealAccent flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="badge-blue text-[11px] px-2.5 py-0.5 rounded-full font-bold">
                  Workshop Chuyên đề
                </span>
                <span className="text-xs text-gray-500 flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-tealAccent" />
                  Tháng sau
                </span>
              </div>
              <h4 className="text-base font-bold text-navy dark:text-white">
                Workshop: Làm chủ thuật ngữ REST API & Clean Architecture trong phỏng vấn quốc tế
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                Thực hành mô phỏng phỏng vấn kỹ thuật bằng tiếng Anh cho các vị trí Backend .NET, Frontend Next.js và Mobile Developer.
              </p>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Địa điểm: <strong>Phòng Lab CNTT, Trường ĐH Công nghệ Đồng Nai</strong>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between">
              <span className="text-xs text-gray-500 font-medium">Giới hạn: 60 chỗ</span>
              <Link
                href="/events"
                className="px-4 py-2 rounded-lg bg-navy hover:bg-navy-light text-white text-xs font-semibold shadow-sm"
              >
                Xem chi tiết
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Tech Radar & Open Source Preview */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <span className="text-xs uppercase tracking-widest font-bold text-tealAccent">
              Technology Radar
            </span>
            <h3 className="text-2xl font-bold text-navy dark:text-white mt-1">
              Kho Công nghệ Mở & Xu hướng Toàn cầu
            </h3>
          </div>
          <Link
            href="/tech-radar"
            className="text-xs font-semibold text-visionary dark:text-tealAccent hover:underline flex items-center gap-1 self-start sm:self-auto"
          >
            <span>Vào kho Tech Radar</span>
            <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-visionary transition-all">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-visionary">GitHub Repository</span>
                <span className="text-[11px] px-2 py-0.5 rounded bg-gray-100 dark:bg-navy-light text-gray-600 dark:text-gray-300 font-medium">MIT</span>
              </div>
              <h4 className="text-base font-bold text-navy dark:text-white flex items-center gap-1.5">
                <span>dotnet/aspnetcore</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 line-clamp-2">
                ASP.NET Core is a cross-platform, high-performance, open-source framework for building modern Web APIs and cloud apps.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold text-tealAccent">C#</span>
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 text-amber-400" /> 36.8k
                </span>
                <span className="flex items-center gap-1">
                  <GitFork className="w-3.5 h-3.5" /> 9.6k
                </span>
              </div>
            </div>
          </div>

          <div className="glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-visionary transition-all">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-visionary">GitHub Repository</span>
                <span className="text-[11px] px-2 py-0.5 rounded bg-gray-100 dark:bg-navy-light text-gray-600 dark:text-gray-300 font-medium">MIT</span>
              </div>
              <h4 className="text-base font-bold text-navy dark:text-white flex items-center gap-1.5">
                <span>vercel/next.js</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 line-clamp-2">
                The React Framework for the Web. Used by top global tech companies to create full-stack Web applications.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold text-tealAccent">TypeScript</span>
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 text-amber-400" /> 127k
                </span>
                <span className="flex items-center gap-1">
                  <GitFork className="w-3.5 h-3.5" /> 27k
                </span>
              </div>
            </div>
          </div>

          <div className="glass-card p-5 rounded-2xl flex flex-col justify-between hover:border-visionary transition-all">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-tealAccent">Hugging Face Model</span>
                <span className="text-[11px] px-2 py-0.5 rounded bg-gray-100 dark:bg-navy-light text-gray-600 dark:text-gray-300 font-medium">Open Weights</span>
              </div>
              <h4 className="text-base font-bold text-navy dark:text-white flex items-center gap-1.5">
                <span>meta-llama/Llama-3-8B</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-300 line-clamp-2">
                State-of-the-art open large language model by Meta, optimized for research, reasoning, code generation and RAG.
              </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center justify-between text-xs text-gray-500">
              <span className="font-semibold text-tealAccent">Python / PyTorch</span>
              <div className="flex items-center gap-3">
                <span className="flex items-center gap-1 text-tealAccent font-semibold">
                  NLP / LLM
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Team Recognition Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-card rounded-3xl p-8 lg:p-10 border border-tealAccent/30 relative overflow-hidden bg-gradient-to-r from-navy/5 via-tealAccent/5 to-visionary/5">
          <div className="relative z-10 flex flex-col lg:flex-row items-center justify-between gap-6">
            <div className="space-y-3 text-center lg:text-left max-w-2xl">
              <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold">
                VISIONARY API Engineering Group
              </div>
              <h3 className="text-2xl sm:text-3xl font-extrabold text-navy dark:text-white">
                Dự án Quản lý Hoạt động Hội nhập CLB Tiếng Anh DNTU
              </h3>
              <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                Được nghiên cứu, thiết kế kiến trúc và phát triển đồng bộ bởi 4 thành viên:{" "}
                <strong className="text-navy dark:text-white">Quách Khoa Đức</strong>,{" "}
                <strong className="text-navy dark:text-white">Võ Ngọc Minh Đạt</strong>,{" "}
                <strong className="text-navy dark:text-white">Hồ Đoàng Nguyên Khang</strong>, và{" "}
                <strong className="text-navy dark:text-white">Đào Trí Khang</strong>.
              </p>
            </div>

            <Link
              href="/about"
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-visionary to-tealAccent text-white text-xs font-bold shadow-lg shadow-tealAccent/20 hover:scale-105 transition-all flex items-center gap-2 flex-shrink-0"
            >
              <span>Tìm hiểu về Đội ngũ</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

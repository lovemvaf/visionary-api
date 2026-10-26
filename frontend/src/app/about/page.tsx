import React from "react";
import Link from "next/link";
import {
  Globe,
  Users,
  ShieldCheck,
  BookOpen,
  Award,
  Sparkles,
  Mail,
  MapPin,
  Calendar,
  CheckCircle,
  ArrowRight
} from "lucide-react";

export default function AboutPage() {
  const teamMembers = [
    {
      name: "Quách Khoa Đức",
      role: "Principal Software Architect & Lead Full-Stack Engineer",
      studentId: "1923040025",
      department: "Khoa Công nghệ Thông tin",
      responsibilities: "Kiến trúc tổng thể, ASP.NET Core 8 Web API, PostgreSQL/Supabase, Frontend Web Next.js, CI/CD, Tự động hóa và Tích hợp hệ thống.",
      isLead: true
    },
    {
      name: "Võ Ngọc Minh Đạt",
      role: "Club Operations & Desktop Software Engineer",
      department: "Khoa Công nghệ Thông tin",
      responsibilities: "Nghiệp vụ Câu lạc bộ Tiếng Anh, Quản lý Thành viên, Quản lý Sự kiện & Điểm danh, Ứng dụng Quản trị Windows Forms C#.",
      isLead: false
    },
    {
      name: "Hồ Đoàn Nguyên Khang",
      role: "Data Pipeline & Opportunities Specialist",
      department: "Khoa Công nghệ Thông tin",
      responsibilities: "Cổng thông tin Cuộc thi quốc tế, Hackathon, Học bổng, Career Gateway, Pipeline thu thập và làm sạch dữ liệu tự động.",
      isLead: false
    },
    {
      name: "Đào Trí Khang",
      role: "Mobile Software Engineer & Tech Lead",
      department: "Khoa Công nghệ Thông tin",
      responsibilities: "Phát triển ứng dụng di động Android Native Java, Chuyên trang English for IT, Technology Radar và Kiểm thử chất lượng.",
      isLead: false
    }
  ];

  const departments = [
    {
      name: "Ban Chuyên môn & Học thuật",
      desc: "Phụ trách tổ chức các workshop English for IT, rèn luyện kỹ năng phỏng vấn kỹ thuật quốc tế và tổ chức câu lạc bộ nói tiếng Anh.",
      color: "border-tealAccent"
    },
    {
      name: "Ban Truyền thông & Sự kiện",
      desc: "Quản trị nội dung tin tức hội nhập, sản xuất ấn phẩm truyền thông, tổ chức các buổi tọa đàm công nghệ và quản lý album ảnh hoạt động.",
      color: "border-visionary"
    },
    {
      name: "Ban Đối ngoại & Hợp tác",
      desc: "Kết nối các cơ hội học bổng quốc tế, cuộc thi hackathon toàn cầu và kết nối các chương trình thực tập CNTT dành cho sinh viên.",
      color: "border-indigo-500"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
      {/* 1. Header Title */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="badge-teal inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
          Giới thiệu Hệ thống & Đội ngũ
        </div>
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-navy dark:text-white tracking-tight">
          Về VISIONARY & Nhóm VISIONARY API
        </h1>
        <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
          VISIONARY ra đời từ sự thấu hiểu sâu sắc về nhu cầu kết hợp ngoại ngữ chuyên môn với công nghệ cao trong kỷ nguyên hội nhập toàn cầu của sinh viên Đại học Công nghệ Đồng Nai (DNTU).
        </p>
      </div>

      {/* 2. Club Mission & Pillars */}
      <section className="glass-card rounded-3xl p-8 lg:p-12 border border-surface-border space-y-8">
        <div className="max-w-3xl space-y-4">
          <span className="text-xs uppercase font-bold text-tealAccent tracking-wider">
            Sứ mệnh CLB Tiếng Anh DNTU
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-navy dark:text-white">
            Connecting Students, Technology and Global Opportunities
          </h2>
          <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
            Chúng tôi định hướng hoạt động CLB không chỉ dừng lại ở các buổi giao tiếp tiếng Anh cơ bản, mà phải liên kết chặt chẽ vào hành trình nghề nghiệp: <strong>Khám phá → Học tập → Kết nối → Tham gia → Phát triển kỹ năng → Ghi nhận thành tích → Tiếp cận cơ hội quốc tế</strong>.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
          {departments.map((d) => (
            <div key={d.name} className={`glass-card p-6 rounded-2xl border-l-4 ${d.color} space-y-3`}>
              <h3 className="text-base font-bold text-navy dark:text-white">{d.name}</h3>
              <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">{d.desc}</p>
            </div>
          ))}
        </div>

        <div className="pt-6 border-t border-gray-100 dark:border-gray-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-gray-500">
            Bạn muốn tham gia vào Ban Chủ Nhiệm hoặc trở thành Thành viên chính thức?
          </div>
          <Link
            href="/auth/register"
            className="px-5 py-2.5 rounded-xl bg-visionary hover:bg-visionary-hover text-white text-xs font-bold shadow-md shadow-visionary/25 flex items-center gap-1.5"
          >
            <span>Nộp đơn gia nhập CLB</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </section>

      {/* 3. Official Development Team: VISIONARY API */}
      <section className="space-y-8">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs uppercase font-bold text-tealAccent tracking-wider">
            Đội ngũ Phát triển
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-navy dark:text-white">
            Nhóm Kỹ thuật VISIONARY API
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Gồm 4 thành viên chính thức đảm nhiệm toàn diện các phân hệ của hệ sinh thái:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {teamMembers.map((m) => (
            <div
              key={m.name}
              className={`glass-card p-6 rounded-2xl flex flex-col justify-between space-y-4 border ${
                m.isLead ? "border-tealAccent shadow-md" : "border-surface-border"
              }`}
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-navy to-visionary flex items-center justify-center text-white font-bold text-sm">
                      {m.name.split(" ").slice(-1)[0][0]}
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-navy dark:text-white flex items-center gap-2">
                        {m.name}
                        {m.isLead && (
                          <span className="badge-teal text-[10px] px-2 py-0.5 rounded-full font-bold">
                            Lead
                          </span>
                        )}
                      </h3>
                      <div className="text-xs text-gray-500">{m.department}</div>
                    </div>
                  </div>
                </div>

                <div className="text-xs font-semibold text-visionary dark:text-tealAccent">
                  {m.role}
                </div>

                <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
                  {m.responsibilities}
                </p>
              </div>

              {m.studentId && (
                <div className="pt-3 border-t border-gray-100 dark:border-gray-800 text-[11px] text-gray-500 flex items-center justify-between">
                  <span>MSSV: <strong>{m.studentId}</strong></span>
                  <span className="text-tealAccent font-medium">Verified Contributor</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 4. Academic Integrity Notice */}
      <section className="glass-card rounded-2xl p-6 border-l-4 border-amber-500 bg-amber-50/30 dark:bg-amber-950/10 space-y-2">
        <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400 font-bold text-xs uppercase tracking-wide">
          <ShieldCheck className="w-4 h-4" />
          <span>Thông cáo Minh bạch Học thuật & Sở hữu Trí tuệ</span>
        </div>
        <p className="text-xs text-gray-600 dark:text-gray-300 leading-relaxed">
          VISIONARY là hệ thống giải pháp công nghệ do nhóm sinh viên <strong>VISIONARY API</strong> nghiên cứu và thực hiện phục vụ bài toán số hóa hoạt động CLB Tiếng Anh và môn học TH71108 Web API. Trang web thể hiện sản phẩm đồ án của nhóm, không tự nhận là cổng thông tin điện tử hành chính chính thức của Trường Đại học Công nghệ Đồng Nai khi chưa có quyết định phê duyệt bằng văn bản từ nhà trường. Mọi dữ liệu thu thập từ các nguồn công khai quốc tế đều giữ nguyên tính liêm chính và chỉ dẫn nguồn gốc xuất xứ.
        </p>
      </section>
    </div>
  );
}

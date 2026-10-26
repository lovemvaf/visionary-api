import React from "react";
import Link from "next/link";
import { Globe, Heart, ShieldCheck, Mail, MapPin, ExternalLink } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-navy-dark text-gray-300 border-t border-navy-light/40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand & Slogan */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-visionary to-tealAccent flex items-center justify-center text-white shadow-md">
                <Globe className="w-5 h-5" />
              </div>
              <span className="text-xl font-bold tracking-tight text-white">VISIONARY</span>
            </div>
            <p className="text-sm text-gray-400 max-w-sm leading-relaxed">
              Hệ thống Quản lý Hoạt động Hội nhập – Nền tảng kết nối Câu lạc bộ Tiếng Anh, trung tâm tri thức English for IT, Radar công nghệ và cơ hội quốc tế.
            </p>
            <div className="text-xs text-tealAccent font-semibold tracking-wide uppercase">
              Connecting Students, Technology and Global Opportunities
            </div>
            <div className="pt-2 text-xs text-gray-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-tealAccent flex-shrink-0" />
              <span>Dự án học thuật TH71108 Web API do nhóm VISIONARY API nghiên cứu & phát triển.</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
              Khám phá
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/about" className="hover:text-tealAccent transition-colors">
                  Giới thiệu CLB & Nhóm
                </Link>
              </li>
              <li>
                <Link href="/english-for-it" className="hover:text-tealAccent transition-colors">
                  English for IT
                </Link>
              </li>
              <li>
                <Link href="/tech-radar" className="hover:text-tealAccent transition-colors">
                  Technology Radar
                </Link>
              </li>
              <li>
                <Link href="/opportunities" className="hover:text-tealAccent transition-colors">
                  Cuộc thi & Học bổng
                </Link>
              </li>
              <li>
                <Link href="/careers" className="hover:text-tealAccent transition-colors">
                  Career Gateway
                </Link>
              </li>
              <li>
                <Link href="/achievements" className="hover:text-tealAccent transition-colors">
                  Bảng vàng Thành tích
                </Link>
              </li>
            </ul>
          </div>

          {/* Platform & Resources */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
              Hệ sinh thái
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <Link href="/events" className="hover:text-tealAccent transition-colors">
                  Sự kiện & Hoạt động
                </Link>
              </li>
              <li>
                <Link href="/posts" className="hover:text-tealAccent transition-colors">
                  Tin tức & Thông báo
                </Link>
              </li>
              <li>
                <a
                  href="http://localhost:5000/swagger"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-tealAccent transition-colors flex items-center gap-1"
                >
                  <span>ASP.NET Core OpenAPI</span>
                  <ExternalLink className="w-3 h-3 text-gray-400" />
                </a>
              </li>
              <li>
                <span className="text-gray-400">Windows Forms C# Client</span>
              </li>
              <li>
                <span className="text-gray-400">Android Native Java App</span>
              </li>
            </ul>
          </div>

          {/* Development Team */}
          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-4">
              Nhóm VISIONARY API
            </h4>
            <ul className="space-y-1.5 text-xs text-gray-300">
              <li className="font-medium text-white flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-tealAccent"></span>
                <a
                  href="https://github.com/lovemvaf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-tealAccent transition-colors flex items-center gap-1"
                >
                  <span>Quách Khoa Đức (Lead)</span>
                  <ExternalLink className="w-2.5 h-2.5 text-gray-500" />
                </a>
              </li>
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-gray-500"></span>
                <a
                  href="https://github.com/vongocminhdat"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-tealAccent transition-colors flex items-center gap-1"
                >
                  <span>Võ Ngọc Minh Đạt</span>
                  <ExternalLink className="w-2.5 h-2.5 text-gray-500" />
                </a>
              </li>
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-gray-500"></span>
                <a
                  href="https://github.com/HoKhangIT"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-tealAccent transition-colors flex items-center gap-1"
                >
                  <span>Hồ Đoàn Nguyên Khang</span>
                  <ExternalLink className="w-2.5 h-2.5 text-gray-500" />
                </a>
              </li>
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-gray-500"></span>
                <a
                  href="https://github.com/TS13lover1989"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-tealAccent transition-colors flex items-center gap-1"
                >
                  <span>Đào Trí Khang</span>
                  <ExternalLink className="w-2.5 h-2.5 text-gray-500" />
                </a>
              </li>
            </ul>
            <div className="mt-4 pt-3 border-t border-gray-800 text-[11px] text-gray-400 space-y-1">
              <div className="flex items-center gap-1.5">
                <MapPin className="w-3 h-3 text-tealAccent" />
                <span>Trường ĐH Công nghệ Đồng Nai</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Mail className="w-3 h-3 text-tealAccent" />
                <span>visionary.dntu@gmail.com</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-navy-light/40 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-400 gap-4">
          <p>© 2026 VISIONARY — Developed by VISIONARY API. All rights reserved.</p>
          <div className="flex items-center gap-2">
            <span>Built with ASP.NET Core 8 & Next.js App Router</span>
            <span>•</span>
            <span className="text-tealAccent">One API, Three Platforms</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

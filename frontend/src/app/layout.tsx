import type { Metadata } from "next";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import "../styles/globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://visionary-platform.vercel.app"),
  title: "VISIONARY – English, Technology & Global Integration Platform | DNTU",
  description:
    "Hệ thống Quản lý Hoạt động Hội nhập – Kết nối Sinh viên, Công nghệ và Cơ hội Quốc tế. Phát triển bởi nhóm VISIONARY API (Quách Khoa Đức, Võ Ngọc Minh Đạt, Hồ Đoàn Nguyên Khang, Đào Trí Khang).",
  keywords: [
    "VISIONARY",
    "DNTU",
    "Câu lạc bộ Tiếng Anh DNTU",
    "English for IT",
    "Technology Radar",
    "Global Opportunities",
    "Hackathon",
    "Career Gateway"
  ],
  authors: [{ name: "VISIONARY API" }],
  openGraph: {
    title: "VISIONARY – English, Technology & Global Integration Platform",
    description: "Hệ thống Quản lý Hoạt động Hội nhập – CLB Tiếng Anh DNTU",
    url: "https://visionary-platform.vercel.app",
    siteName: "VISIONARY Platform",
    locale: "vi_VN",
    type: "website",
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col bg-surface dark:bg-navy-dark text-navy dark:text-gray-100 antialiased selection:bg-tealAccent/20 selection:text-tealAccent">
        <Navbar />
        <main className="flex-grow">{children}</main>
        <Footer />
      </body>
    </html>
  );
}

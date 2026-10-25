import { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/dashboard/admin", "/api/"],
    },
    sitemap: "https://visionary-platform.vercel.app/sitemap.xml",
  };
}

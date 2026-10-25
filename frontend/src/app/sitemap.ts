import { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://visionary-platform.vercel.app";
  const routes = [
    "",
    "/about",
    "/english-for-it",
    "/tech-radar",
    "/opportunities",
    "/careers",
    "/events",
    "/achievements",
    "/posts",
    "/auth/login",
    "/auth/register",
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: route === "" ? "daily" : "weekly",
    priority: route === "" ? 1.0 : 0.8,
  }));
}

import { NextRequest, NextResponse } from "next/server";

function cleanUrl(url?: string): string {
  if (!url) return "http://localhost:5000";
  // Remove BOM (\uFEFF), zero-width characters, control characters, and trailing slashes
  const sanitized = url.replace(/[\uFEFF\u200B-\u200D\u0000-\u001F]/g, "").trim();
  return sanitized.replace(/\/+$/, "");
}

// Determine backend upstream URL
const BACKEND_BASE_URL = cleanUrl(
  process.env.API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_URL
);

async function handleProxy(req: NextRequest, { params }: { params: { path: string[] } }) {
  const path = params.path ? params.path.join("/") : "";
  const correlationId = `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
  const searchParams = req.nextUrl.searchParams.toString();
  const targetUrl = `${BACKEND_BASE_URL}/api/${path}${searchParams ? `?${searchParams}` : ""}`;

  // Forward incoming headers
  const headers = new Headers();
  const authHeader = req.headers.get("authorization");
  if (authHeader) headers.set("authorization", authHeader);

  const contentType = req.headers.get("content-type");
  if (contentType) headers.set("content-type", contentType);

  headers.set("accept", "application/json");
  headers.set("x-correlation-id", correlationId);

  // Read request body if present
  let body: BodyInit | null = null;
  if (["POST", "PUT", "PATCH"].includes(req.method)) {
    try {
      body = await req.text();
    } catch {
      body = null;
    }
  }

  // Abort controller for 15s timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000);

  try {
    const upstreamRes = await fetch(targetUrl, {
      method: req.method,
      headers,
      body,
      signal: controller.signal,
      cache: "no-store",
    });

    clearTimeout(timeoutId);

    const resContentType = upstreamRes.headers.get("content-type") || "";
    let responseData: any;

    if (resContentType.includes("application/json")) {
      responseData = await upstreamRes.json();
    } else {
      const text = await upstreamRes.text();
      responseData = {
        success: upstreamRes.ok,
        message: text || (upstreamRes.ok ? "Success" : "Lỗi xử lý từ máy chủ"),
        data: null,
      };
    }

    const response = NextResponse.json(responseData, {
      status: upstreamRes.status,
    });
    response.headers.set("x-correlation-id", correlationId);
    return response;
  } catch (error: any) {
    clearTimeout(timeoutId);
    const isTimeout = error?.name === "AbortError";
    const errorMessage = isTimeout
      ? "Yêu cầu tới máy chủ Visionary đã quá thời gian chờ (15s). Vui lòng thử lại sau."
      : "Không thể kết nối đến máy chủ Visionary. Dịch vụ máy chủ đang khởi động hoặc chưa sẵn sàng.";

    return NextResponse.json(
      {
        success: false,
        message: errorMessage,
        data: null,
        errors: [error?.message || "Upstream backend unreachable"],
        correlationId,
        timestamp: new Date().toISOString(),
      },
      { status: 503, headers: { "x-correlation-id": correlationId } }
    );
  }
}

export async function GET(req: NextRequest, ctx: { params: { path: string[] } }) {
  return handleProxy(req, ctx);
}

export async function POST(req: NextRequest, ctx: { params: { path: string[] } }) {
  return handleProxy(req, ctx);
}

export async function PUT(req: NextRequest, ctx: { params: { path: string[] } }) {
  return handleProxy(req, ctx);
}

export async function DELETE(req: NextRequest, ctx: { params: { path: string[] } }) {
  return handleProxy(req, ctx);
}

export async function PATCH(req: NextRequest, ctx: { params: { path: string[] } }) {
  return handleProxy(req, ctx);
}

export async function OPTIONS() {
  return new NextResponse(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, x-correlation-id",
    },
  });
}

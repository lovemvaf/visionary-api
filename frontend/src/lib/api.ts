import {
  ApiResponse,
  PagedResponse,
  AuthResponse,
  UserProfile,
  ClubOverview,
  Department,
  Member,
  CommitteeMember,
  EventItem,
  PostItem,
  PostCategory,
  LearningResource,
  TechResource,
  OpportunityItem,
  JobItem,
  AchievementItem,
  DashboardStats,
  MembershipApplicationItem,
  AuditLogItem,
  UserListItem,
  ContentSourceItem
} from "./types";

const getBaseUrl = (): string => {
  // In the browser, always use same-origin relative calls ("") so requests go to Next.js BFF (/api/...)
  if (typeof window !== "undefined") {
    return "";
  }
  // Server-side calls use API_BASE_URL or NEXT_PUBLIC_API_URL or localhost
  return process.env.API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";
};

function getToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("visionary_token");
  }
  return null;
}

export function setToken(token: string) {
  if (typeof window !== "undefined") {
    localStorage.setItem("visionary_token", token);
  }
}

export function clearToken() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("visionary_token");
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const baseUrl = getBaseUrl();
  const url = `${baseUrl}${endpoint}`;

  try {
    const res = await fetch(url, { ...options, headers });
    const contentType = res.headers.get("content-type") || "";
    let data: any;

    if (contentType.includes("application/json")) {
      data = await res.json();
    } else {
      const text = await res.text();
      data = {
        success: res.ok,
        message: text,
        data: null
      };
    }

    if (!res.ok) {
      let friendlyMessage = data?.message;
      if (res.status === 401) {
        friendlyMessage = "Email hoặc mật khẩu không chính xác.";
      } else if (res.status === 403) {
        friendlyMessage = "Bạn không có quyền thực hiện thao tác này.";
      } else if (res.status === 409) {
        friendlyMessage = "Email này đã được đăng ký. Bạn có thể đăng nhập hoặc đặt lại mật khẩu.";
      } else if (res.status === 502 || res.status === 503 || res.status === 504) {
        friendlyMessage = "Dịch vụ máy chủ Visionary đang khởi động hoặc chưa sẵn sàng. Vui lòng thử lại sau ít phút.";
      } else if (!friendlyMessage) {
        friendlyMessage = `Yêu cầu không thành công (Mã lỗi: ${res.status}). Vui lòng thử lại.`;
      }

      return {
        success: false,
        message: friendlyMessage,
        data: null as any,
        errors: data?.errors || [friendlyMessage],
        timestamp: new Date().toISOString()
      };
    }

    return data as ApiResponse<T>;
  } catch (error: any) {
    return {
      success: false,
      message: "Không thể kết nối đến máy chủ Visionary. Vui lòng kiểm tra kết nối mạng và thử lại.",
      data: null as any,
      errors: [error?.message || "Connection failed"],
      timestamp: new Date().toISOString()
    };
  }
}

export const api = {
  // Auth
  async login(email: string, password: string): Promise<ApiResponse<AuthResponse>> {
    const res = await request<AuthResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    if (res.success && res.data?.token) {
      setToken(res.data.token);
    }
    return res;
  },

  async register(data: { email: string; password: string; fullName: string; studentId?: string; department?: string }): Promise<ApiResponse<AuthResponse>> {
    const res = await request<AuthResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    if (res.success && res.data?.token) {
      setToken(res.data.token);
    }
    return res;
  },

  async googleLogin(idToken: string): Promise<ApiResponse<AuthResponse>> {
    const res = await request<AuthResponse>("/api/auth/google", {
      method: "POST",
      body: JSON.stringify({ idToken }),
    });
    if (res.success && res.data?.token) {
      setToken(res.data.token);
    }
    return res;
  },

  async getMe(): Promise<ApiResponse<UserProfile>> {
    return request<UserProfile>("/api/auth/me");
  },

  async updateProfile(data: { fullName: string; studentId?: string; department?: string; bio?: string }): Promise<ApiResponse<UserProfile>> {
    return request<UserProfile>("/api/auth/profile", {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  logout() {
    clearToken();
  },

  // Club
  async getClubOverview(): Promise<ApiResponse<ClubOverview>> {
    return request<ClubOverview>("/api/club/overview");
  },

  async getDepartments(): Promise<ApiResponse<Department[]>> {
    return request<Department[]>("/api/club/departments");
  },

  async getMembers(params?: { departmentId?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<Member>>> {
    const qs = new URLSearchParams();
    if (params?.departmentId) qs.append("departmentId", params.departmentId);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<Member>>(`/api/club/members?${qs.toString()}`);
  },

  async getCommittee(): Promise<ApiResponse<CommitteeMember[]>> {
    return request<CommitteeMember[]>("/api/club/committee");
  },

  async applyMembership(data: { preferredDepartmentId?: string; selfIntroduction: string; motivation: string; englishProficiency?: string }): Promise<ApiResponse<any>> {
    return request<any>("/api/club/applications", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async getApplications(status?: string): Promise<ApiResponse<MembershipApplicationItem[]>> {
    const qs = status ? `?status=${status}` : "";
    return request<MembershipApplicationItem[]>(`/api/club/applications${qs}`);
  },

  async reviewApplication(id: string, isApproved: boolean, clubRole?: string, departmentId?: string, reviewNotes?: string): Promise<ApiResponse<string>> {
    return request<string>(`/api/club/applications/${id}/review`, {
      method: "PUT",
      body: JSON.stringify({ isApproved, clubRole, departmentId, reviewNotes }),
    });
  },

  // Events
  async getEvents(params?: { status?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<EventItem>>> {
    const qs = new URLSearchParams();
    if (params?.status) qs.append("status", params.status);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<EventItem>>(`/api/events?${qs.toString()}`);
  },

  async getEventBySlug(slug: string): Promise<ApiResponse<EventItem>> {
    return request<EventItem>(`/api/events/${slug}`);
  },

  async registerEvent(id: string): Promise<ApiResponse<string>> {
    return request<string>(`/api/events/${id}/register`, { method: "POST" });
  },

  async cancelEventRegistration(id: string): Promise<ApiResponse<string>> {
    return request<string>(`/api/events/${id}/cancel`, { method: "POST" });
  },

  async getMyEvents(): Promise<ApiResponse<EventItem[]>> {
    return request<EventItem[]>("/api/events/my-events");
  },

  async createEvent(data: { title: string; description: string; location: string; startTime: string; endTime: string; registrationDeadline: string; maxCapacity: number }): Promise<ApiResponse<EventItem>> {
    return request<EventItem>("/api/events", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  // Posts / CMS
  async getPosts(params?: { categoryId?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<PostItem>>> {
    const qs = new URLSearchParams();
    if (params?.categoryId) qs.append("categoryId", params.categoryId);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<PostItem>>(`/api/posts?${qs.toString()}`);
  },

  async getPostBySlug(slug: string): Promise<ApiResponse<PostItem>> {
    return request<PostItem>(`/api/posts/${slug}`);
  },

  async getCategories(): Promise<ApiResponse<PostCategory[]>> {
    return request<PostCategory[]>("/api/posts/categories");
  },

  // English for IT
  async getEnglishResources(params?: { level?: string; topic?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<LearningResource>>> {
    const qs = new URLSearchParams();
    if (params?.level) qs.append("level", params.level);
    if (params?.topic) qs.append("topic", params.topic);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<LearningResource>>(`/api/english-for-it?${qs.toString()}`);
  },

  async getEnglishResourceBySlug(slug: string): Promise<ApiResponse<LearningResource>> {
    return request<LearningResource>(`/api/english-for-it/${slug}`);
  },

  // Tech Radar
  async getTechResources(params?: { sourceType?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<TechResource>>> {
    const qs = new URLSearchParams();
    if (params?.sourceType) qs.append("sourceType", params.sourceType);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<TechResource>>(`/api/tech-radar?${qs.toString()}`);
  },

  async syncTechResources(source: string = "All"): Promise<ApiResponse<string>> {
    return request<string>("/api/tech-radar/sync", {
      method: "POST",
      body: JSON.stringify({ source }),
    });
  },

  // Opportunities
  async getOpportunities(params?: { category?: string; scope?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<OpportunityItem>>> {
    const qs = new URLSearchParams();
    if (params?.category) qs.append("category", params.category);
    if (params?.scope) qs.append("scope", params.scope);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<OpportunityItem>>(`/api/opportunities?${qs.toString()}`);
  },

  // Jobs
  async getJobs(params?: { jobType?: string; workplaceType?: string; search?: string; pageIndex?: number; pageSize?: number }): Promise<ApiResponse<PagedResponse<JobItem>>> {
    const qs = new URLSearchParams();
    if (params?.jobType) qs.append("jobType", params.jobType);
    if (params?.workplaceType) qs.append("workplaceType", params.workplaceType);
    if (params?.search) qs.append("search", params.search);
    if (params?.pageIndex) qs.append("pageIndex", params.pageIndex.toString());
    if (params?.pageSize) qs.append("pageSize", params.pageSize.toString());
    return request<PagedResponse<JobItem>>(`/api/jobs?${qs.toString()}`);
  },

  // Achievements
  async getAchievements(categoryId?: string): Promise<ApiResponse<AchievementItem[]>> {
    const qs = categoryId ? `?categoryId=${categoryId}` : "";
    return request<AchievementItem[]>(`/api/achievements${qs}`);
  },

  // Admin Dashboard
  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    return request<DashboardStats>("/api/admin/dashboard");
  },

  async getSources(): Promise<ApiResponse<ContentSourceItem[]>> {
    return request<ContentSourceItem[]>("/api/admin/sources");
  },

  async triggerSource(id: string): Promise<ApiResponse<string>> {
    return request<string>(`/api/admin/sources/trigger/${id}`, { method: "POST" });
  },

  async getAuditLogs(): Promise<ApiResponse<AuditLogItem[]>> {
    return request<AuditLogItem[]>("/api/admin/audit-logs");
  },

  async getUsers(search?: string): Promise<ApiResponse<UserListItem[]>> {
    const qs = search ? `?search=${encodeURIComponent(search)}` : "";
    return request<UserListItem[]>(`/api/admin/users${qs}`);
  },

  async updateUserRoles(id: string, roles: string[]): Promise<ApiResponse<string>> {
    return request<string>(`/api/admin/users/${id}/roles`, {
      method: "PUT",
      body: JSON.stringify({ roles })
    });
  }
};

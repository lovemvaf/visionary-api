export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  errors: string[];
  timestamp: string;
}

export interface PagedResponse<T> {
  items: T[];
  pageIndex: number;
  pageSize: number;
  totalCount: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

export interface UserProfile {
  id: string;
  email: string;
  fullName: string;
  studentId?: string;
  department?: string;
  avatarUrl?: string;
  bio?: string;
  roles: string[];
  isMember: boolean;
  clubRole?: string;
}

export interface AuthResponse {
  token: string;
  expiresAt: string;
  user: UserProfile;
}

export interface Department {
  id: string;
  name: string;
  description?: string;
  memberCount: number;
}

export interface CommitteeMember {
  userId: string;
  fullName: string;
  position: string;
  avatarUrl?: string;
  department?: string;
}

export interface ClubOverview {
  name: string;
  description: string;
  mission: string;
  totalMembers: number;
  totalEvents: number;
  departments: Department[];
  currentCommittee: CommitteeMember[];
  contactEmail: string;
}

export interface Member {
  id: string;
  userId: string;
  fullName: string;
  email: string;
  studentId?: string;
  departmentName?: string;
  clubRole: string;
  status: string;
  joinedDate: string;
  englishLevel?: string;
  avatarUrl?: string;
}

export interface EventItem {
  id: string;
  title: string;
  slug: string;
  description: string;
  location: string;
  startTime: string;
  endTime: string;
  registrationDeadline: string;
  maxCapacity: number;
  currentRegistrationsCount: number;
  bannerUrl?: string;
  status: string;
  isRegisteredByCurrentUser: boolean;
  isCheckedInByCurrentUser: boolean;
  qrCheckInCode?: string;
}

export interface PostItem {
  id: string;
  categoryId: string;
  categoryName: string;
  authorName: string;
  title: string;
  slug: string;
  summary: string;
  contentMarkdown: string;
  contentHtml: string;
  thumbnailUrl?: string;
  status: string;
  publishedAt?: string;
  viewCount: number;
  tags: string[];
}

export interface PostCategory {
  id: string;
  name: string;
  slug: string;
  description?: string;
  postCount: number;
}

export interface LearningResource {
  id: string;
  title: string;
  slug: string;
  level: string;
  topic: string;
  summary: string;
  content: string;
  glossaryJson?: string;
  referenceUrl?: string;
  viewCount: number;
  createdAt: string;
}

export interface TechResource {
  id: string;
  name: string;
  sourceType: string;
  externalId?: string;
  officialUrl: string;
  description: string;
  primaryLanguage?: string;
  license?: string;
  metricsJson?: string;
  learningSuitability?: string;
  lastCheckedAt: string;
  isVerified: boolean;
}

export interface OpportunityItem {
  id: string;
  title: string;
  organizer: string;
  category: string;
  scope: string;
  format: string;
  officialUrl: string;
  eligibility: string;
  registrationDeadline?: string;
  status: string;
  verifiedAt?: string;
  verifiedSource?: string;
}

export interface JobItem {
  id: string;
  title: string;
  company: string;
  jobType: string;
  workplaceType: string;
  location: string;
  applyUrl: string;
  requirements: string;
  englishRequired: boolean;
  isVerified: boolean;
  createdAt: string;
}

export interface AchievementItem {
  id: string;
  categoryId: string;
  categoryName: string;
  recipientUserId: string;
  recipientName: string;
  studentId?: string;
  department?: string;
  title: string;
  description: string;
  awardedDate: string;
  evidenceUrl?: string;
  isVerified: boolean;
}

export interface DashboardStats {
  totalUsers: number;
  totalMembers: number;
  pendingApplications: number;
  totalEvents: number;
  totalPosts: number;
  totalAchievements: number;
  totalOpportunities: number;
  totalJobs: number;
  totalTechResources: number;
  recentActivities: {
    action: string;
    description: string;
    timestamp: string;
    userName?: string;
  }[];
}

export interface MembershipApplicationItem {
  id: string;
  userId: string;
  applicantName: string;
  applicantEmail: string;
  studentId?: string;
  preferredDepartmentName?: string;
  selfIntroduction: string;
  motivation: string;
  englishProficiency?: string;
  status: string;
  reviewNotes?: string;
  submittedAt: string;
}

export interface AuditLogItem {
  id: string;
  action: string;
  resource: string;
  resourceId?: string;
  userName?: string;
  ipAddress?: string;
  timestamp: string;
  details?: string;
}

export interface UserListItem {
  id: string;
  email: string;
  fullName: string;
  studentId?: string;
  department?: string;
  isActive: boolean;
  roles: string[];
  isMember: boolean;
  clubRole?: string;
  createdAt: string;
}

export interface ContentSourceItem {
  id: string;
  name: string;
  type: string;
  endpointUrl: string;
  intervalMinutes: number;
  isEnabled: boolean;
  lastRunAt?: string;
  lastStatus?: string;
}

using System;
using Visionary.Core.Enums;

namespace Visionary.Core.DTOs
{
    public class EventDto
    {
        public Guid Id { get; set; }
        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Location { get; set; } = string.Empty;
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public DateTime RegistrationDeadline { get; set; }
        public int MaxCapacity { get; set; }
        public int CurrentRegistrationsCount { get; set; }
        public string? BannerUrl { get; set; }
        public string Status { get; set; } = string.Empty;
        public bool IsRegisteredByCurrentUser { get; set; }
        public bool IsCheckedInByCurrentUser { get; set; }
        public string? QrCheckInCode { get; set; }
    }

    public class CreateEventRequest
    {
        public string Title { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Location { get; set; } = string.Empty;
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public DateTime RegistrationDeadline { get; set; }
        public int MaxCapacity { get; set; } = 100;
        public string? BannerUrl { get; set; }
    }

    public class UpdateEventRequest : CreateEventRequest
    {
        public EventStatus Status { get; set; }
    }

    public class EventRegistrationDto
    {
        public Guid Id { get; set; }
        public Guid EventId { get; set; }
        public Guid UserId { get; set; }
        public string FullName { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string? StudentId { get; set; }
        public DateTime RegisteredAt { get; set; }
        public string Status { get; set; } = string.Empty;
        public bool IsAttended { get; set; }
        public DateTime? CheckInTime { get; set; }
    }

    public class CheckInRequest
    {
        public Guid UserId { get; set; }
        public string? QrCode { get; set; }
        public AttendanceMethod Method { get; set; } = AttendanceMethod.ManualCheckIn;
    }
}

using System;
using System.Collections.Generic;
using Visionary.Core.Common;
using Visionary.Core.Enums;

namespace Visionary.Core.Entities
{
    public class Event : BaseEntity
    {
        public string Title { get; set; } = string.Empty;
        public string Slug { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;
        public string Location { get; set; } = string.Empty;
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public DateTime RegistrationDeadline { get; set; }
        public int MaxCapacity { get; set; } = 100;
        public string? BannerUrl { get; set; }
        public EventStatus Status { get; set; } = EventStatus.Published;

        public Guid CreatedByUserId { get; set; }
        public User CreatedByUser { get; set; } = null!;

        public string? QrCheckInCode { get; set; }

        public ICollection<EventRegistration> Registrations { get; set; } = new List<EventRegistration>();
        public ICollection<EventAttendance> Attendances { get; set; } = new List<EventAttendance>();
    }

    public class EventRegistration : BaseEntity
    {
        public Guid EventId { get; set; }
        public Event Event { get; set; } = null!;

        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;
        public RegistrationStatus Status { get; set; } = RegistrationStatus.Registered;
        public string? Notes { get; set; }
    }

    public class EventAttendance : BaseEntity
    {
        public Guid EventId { get; set; }
        public Event Event { get; set; } = null!;

        public Guid UserId { get; set; }
        public User User { get; set; } = null!;

        public DateTime CheckInTime { get; set; } = DateTime.UtcNow;
        public AttendanceMethod Method { get; set; } = AttendanceMethod.ManualCheckIn;

        public Guid? VerifiedByUserId { get; set; }
        public User? VerifiedByUser { get; set; }
    }
}

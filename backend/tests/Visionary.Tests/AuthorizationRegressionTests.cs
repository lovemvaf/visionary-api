using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Xunit;

namespace Visionary.Tests
{
    [Collection("IntegrationTests")]
    public class AuthorizationRegressionTests
    {
        private readonly HttpClient _client;

        public AuthorizationRegressionTests(CustomWebApplicationFactory factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task AdminUsers_AnonymousRequest_ReturnsUnauthorized()
        {
            var response = await _client.GetAsync("/api/admin/users");

            Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
        }

        [Fact]
        public async Task Student_CannotAccessAdminOrGrantSelfAdminRole()
        {
            var email = $"authorization-test-{Guid.NewGuid():N}@visionary.test";
            var registration = new RegisterRequest
            {
                Email = email,
                Password = "TestPassword@123",
                FullName = "Authorization Test Student"
            };

            var registrationResponse = await _client.PostAsJsonAsync("/api/auth/register", registration);
            Assert.Equal(HttpStatusCode.OK, registrationResponse.StatusCode);

            var registrationResult = await registrationResponse.Content.ReadFromJsonAsync<ApiResponse<AuthResponse>>();
            Assert.NotNull(registrationResult?.Data);
            Assert.Contains("Student", registrationResult.Data.User.Roles);
            Assert.DoesNotContain("Admin", registrationResult.Data.User.Roles);

            _client.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("Bearer", registrationResult.Data.Token);

            var adminUsersResponse = await _client.GetAsync("/api/admin/users");
            Assert.Equal(HttpStatusCode.Forbidden, adminUsersResponse.StatusCode);

            var roleChangeResponse = await _client.PutAsJsonAsync(
                $"/api/admin/users/{registrationResult.Data.User.Id}/roles",
                new UpdateUserRoleRequest { Roles = new List<string> { "Admin" } });
            Assert.Equal(HttpStatusCode.Forbidden, roleChangeResponse.StatusCode);

            var profileResponse = await _client.GetAsync("/api/auth/me");
            Assert.Equal(HttpStatusCode.OK, profileResponse.StatusCode);

            var profile = await profileResponse.Content.ReadFromJsonAsync<ApiResponse<UserProfileDto>>();
            Assert.NotNull(profile?.Data);
            Assert.Contains("Student", profile.Data.Roles);
            Assert.DoesNotContain("Admin", profile.Data.Roles);
        }
    }
}

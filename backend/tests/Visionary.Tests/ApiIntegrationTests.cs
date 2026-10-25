using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Testing;
using Visionary.Core.Common;
using Visionary.Core.DTOs;
using Xunit;

namespace Visionary.Tests
{
    [Collection("IntegrationTests")]
    public class ApiIntegrationTests
    {
        private readonly HttpClient _client;

        public ApiIntegrationTests(CustomWebApplicationFactory factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task RootEndpoint_ReturnsHealthyStatus()
        {
            var response = await _client.GetAsync("/");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var content = await response.Content.ReadAsStringAsync();
            Assert.Contains("VISIONARY API", content);
            Assert.Contains("Healthy", content);
        }

        [Fact]
        public async Task ClubOverview_ReturnsSuccessData()
        {
            var response = await _client.GetAsync("/api/club/overview");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<ClubOverviewDto>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.True(apiRes.Data.Departments.Count > 0);
        }

        [Fact]
        public async Task EventsEndpoint_ReturnsSeededEvents()
        {
            var response = await _client.GetAsync("/api/events");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResponse<EventDto>>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.True(apiRes.Data.Items.Count > 0);
        }

        [Fact]
        public async Task EnglishForItEndpoint_ReturnsResources()
        {
            var response = await _client.GetAsync("/api/english-for-it");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResponse<LearningResourceDto>>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.True(apiRes.Data.Items.Count > 0);
        }

        [Fact]
        public async Task OpportunitiesEndpoint_ReturnsOpportunities()
        {
            var response = await _client.GetAsync("/api/opportunities");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResponse<OpportunityDto>>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.True(apiRes.Data.Items.Count > 0);
        }

        [Fact]
        public async Task JobsEndpoint_ReturnsJobs()
        {
            var response = await _client.GetAsync("/api/jobs");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<PagedResponse<JobDto>>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.True(apiRes.Data.Items.Count > 0);
        }

        [Fact]
        public async Task Login_WithSeededAdminCredentials_ReturnsJwtToken()
        {
            var loginRequest = new LoginRequest
            {
                Email = "quachkhoaduc@visionary.dntu.edu.vn",
                Password = "Visionary@2026"
            };

            var response = await _client.PostAsJsonAsync("/api/auth/login", loginRequest);
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var apiRes = await response.Content.ReadFromJsonAsync<ApiResponse<AuthResponse>>();
            Assert.NotNull(apiRes);
            Assert.True(apiRes.Success);
            Assert.NotNull(apiRes.Data);
            Assert.False(string.IsNullOrEmpty(apiRes.Data.Token));
            Assert.Equal("Quách Khoa Đức", apiRes.Data.User.FullName);
            Assert.Contains("Admin", apiRes.Data.User.Roles);
        }
    }
}

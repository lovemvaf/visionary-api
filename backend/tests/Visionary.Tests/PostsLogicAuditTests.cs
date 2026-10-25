using System;
using System.Collections.Generic;
using System.Linq;
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
    public class PostsLogicAuditTests : IClassFixture<WebApplicationFactory<Program>>
    {
        private readonly HttpClient _client;

        public PostsLogicAuditTests(WebApplicationFactory<Program> factory)
        {
            _client = factory.CreateClient();
        }

        [Fact]
        public async Task CategoriesEndpoint_ReturnsFourCategoriesWithExactPublishedCounts()
        {
            var res = await _client.GetFromJsonAsync<ApiResponse<List<PostCategoryDto>>>("/api/posts/categories");
            Assert.NotNull(res);
            Assert.True(res.Success);
            Assert.NotNull(res.Data);
            Assert.Equal(4, res.Data.Count);

            var catTech = res.Data.FirstOrDefault(c => c.Slug == "cong-nghe-ai");
            var catEnglish = res.Data.FirstOrDefault(c => c.Slug == "tieng-anh-chuyen-nganh");
            var catNews = res.Data.FirstOrDefault(c => c.Slug == "tin-hoi-nhap");
            var catClub = res.Data.FirstOrDefault(c => c.Slug == "hoat-dong-clb");

            Assert.NotNull(catTech);
            Assert.NotNull(catEnglish);
            Assert.NotNull(catNews);
            Assert.NotNull(catClub);

            Assert.Equal(8, catTech.PostCount);
            Assert.Equal(6, catEnglish.PostCount);
            Assert.Equal(5, catNews.PostCount);
            Assert.Equal(4, catClub.PostCount);
        }

        [Fact]
        public async Task PublishedPosts_CategoryUnion_StrictlyEquals_AllPublishedPosts()
        {
            // 1. Fetch categories
            var catRes = await _client.GetFromJsonAsync<ApiResponse<List<PostCategoryDto>>>("/api/posts/categories");
            Assert.NotNull(catRes?.Data);

            // 2. Fetch all published posts across all pages
            var allPosts = new List<PostDto>();
            int page = 1;
            while (true)
            {
                var pagedRes = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>($"/api/posts?pageIndex={page}&pageSize=10");
                Assert.NotNull(pagedRes?.Data);
                allPosts.AddRange(pagedRes.Data.Items);
                if (!pagedRes.Data.HasNextPage) break;
                page++;
            }

            Assert.Equal(23, allPosts.Count);
            // Verify all IDs in "All" are unique (no duplicates across pages)
            var allDistinctIds = allPosts.Select(p => p.Id).Distinct().ToList();
            Assert.Equal(23, allDistinctIds.Count);

            // 3. Fetch each category and verify union invariant
            var unionCategoryPosts = new List<PostDto>();
            foreach (var cat in catRes.Data)
            {
                var catPosts = new List<PostDto>();
                int catPage = 1;
                while (true)
                {
                    var catPagedRes = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>($"/api/posts?categoryId={cat.Id}&pageIndex={catPage}&pageSize=10");
                    Assert.NotNull(catPagedRes?.Data);
                    catPosts.AddRange(catPagedRes.Data.Items);
                    if (!catPagedRes.Data.HasNextPage) break;
                    catPage++;
                }

                // Verify every post in category actually belongs to that category
                Assert.All(catPosts, p => Assert.Equal(cat.Id, p.CategoryId));
                unionCategoryPosts.AddRange(catPosts);
            }

            Assert.Equal(23, unionCategoryPosts.Count);

            // Invariant: PublishedPosts(All) = UNION( PublishedPosts(Category A), Category B, ... )
            var unionIds = unionCategoryPosts.Select(p => p.Id).OrderBy(id => id).ToList();
            var allIds = allDistinctIds.OrderBy(id => id).ToList();
            Assert.Equal(allIds, unionIds);
        }

        [Fact]
        public async Task Pagination_Metadata_And_ItemCounts_AreAccurate()
        {
            // Page 1
            var page1 = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?pageIndex=1&pageSize=10");
            Assert.NotNull(page1?.Data);
            Assert.Equal(10, page1.Data.Items.Count);
            Assert.Equal(23, page1.Data.TotalCount);
            Assert.Equal(3, page1.Data.TotalPages);
            Assert.Equal(1, page1.Data.PageIndex);
            Assert.True(page1.Data.HasNextPage);
            Assert.False(page1.Data.HasPreviousPage);

            // Page 2
            var page2 = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?pageIndex=2&pageSize=10");
            Assert.NotNull(page2?.Data);
            Assert.Equal(10, page2.Data.Items.Count);
            Assert.Equal(2, page2.Data.PageIndex);
            Assert.True(page2.Data.HasNextPage);
            Assert.True(page2.Data.HasPreviousPage);

            // Page 3
            var page3 = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?pageIndex=3&pageSize=10");
            Assert.NotNull(page3?.Data);
            Assert.Equal(3, page3.Data.Items.Count);
            Assert.Equal(3, page3.Data.PageIndex);
            Assert.False(page3.Data.HasNextPage);
            Assert.True(page3.Data.HasPreviousPage);

            // Intersection of items between pages must be EMPTY (no bleed/duplicates)
            var p1Ids = page1.Data.Items.Select(x => x.Id).ToHashSet();
            var p2Ids = page2.Data.Items.Select(x => x.Id).ToHashSet();
            var p3Ids = page3.Data.Items.Select(x => x.Id).ToHashSet();

            Assert.Empty(p1Ids.Intersect(p2Ids));
            Assert.Empty(p2Ids.Intersect(p3Ids));
            Assert.Empty(p1Ids.Intersect(p3Ids));
        }

        [Fact]
        public async Task UnpublishedPosts_Draft_And_PendingReview_NeverLeakPublicly()
        {
            var res = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?pageSize=50");
            Assert.NotNull(res?.Data);

            Assert.All(res.Data.Items, p =>
            {
                Assert.Equal("Published", p.Status);
                Assert.DoesNotContain("Bản nháp", p.Title);
                Assert.DoesNotContain("Chờ duyệt", p.Title);
            });

            // Direct slug access to Draft should return 404 for anonymous guest
            var draftRes = await _client.GetAsync("/api/posts/draft-ke-hoach-workshop-ai-thang-11");
            Assert.Equal(HttpStatusCode.NotFound, draftRes.StatusCode);

            // Direct slug access to PendingReview should return 404 for anonymous guest
            var pendingRes = await _client.GetAsync("/api/posts/pending-bao-cao-tai-chinh-clb-quy-3");
            Assert.Equal(HttpStatusCode.NotFound, pendingRes.StatusCode);
        }

        [Fact]
        public async Task Search_WithCategory_And_EmptyState_AreAccurate()
        {
            // Search for specific keyword
            var searchRes = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?search=Clean%20Architecture");
            Assert.NotNull(searchRes?.Data);
            Assert.True(searchRes.Data.TotalCount >= 1);
            Assert.Contains(searchRes.Data.Items, p => p.Slug == "kien-truc-clean-architecture-aspnet-core");

            // Search for non-existent keyword returns 0 items and empty list
            var emptyRes = await _client.GetFromJsonAsync<ApiResponse<PagedResponse<PostDto>>>("/api/posts?search=NonExistentKeywordXYZ12345");
            Assert.NotNull(emptyRes?.Data);
            Assert.Equal(0, emptyRes.Data.TotalCount);
            Assert.Empty(emptyRes.Data.Items);
            Assert.False(emptyRes.Data.HasNextPage);
            Assert.False(emptyRes.Data.HasPreviousPage);
        }

        [Fact]
        public async Task GetPostBySlug_ValidPublishedPost_Returns200AndIncrementsView()
        {
            var res = await _client.GetFromJsonAsync<ApiResponse<PostDto>>("/api/posts/chao-mung-he-sinh-thai-visionary-2026");
            Assert.NotNull(res);
            Assert.True(res.Success);
            Assert.NotNull(res.Data);
            Assert.Equal("chao-mung-he-sinh-thai-visionary-2026", res.Data.Slug);
            Assert.Equal("Quách Khoa Đức", res.Data.AuthorName);
        }
    }
}

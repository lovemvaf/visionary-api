using System;
using System.Net;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Visionary.Core.Common;

namespace Visionary.Api.Middleware
{
    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlingMiddleware> _logger;
        private readonly IHostEnvironment _env;

        public ExceptionHandlingMiddleware(
            RequestDelegate next,
            ILogger<ExceptionHandlingMiddleware> logger,
            IHostEnvironment env)
        {
            _next = next;
            _logger = logger;
            _env = env;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                var correlationId = context.TraceIdentifier;
                _logger.LogError(ex, "Unhandled exception occurred [CorrelationId: {CorrelationId}]: {Message}", correlationId, ex.Message);
                await HandleExceptionAsync(context, ex, correlationId);
            }
        }

        private Task HandleExceptionAsync(HttpContext context, Exception exception, string correlationId)
        {
            context.Response.ContentType = "application/json";
            context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;

            var errorDetail = _env.IsDevelopment()
                ? exception.Message
                : $"Internal server error. Trace Identifier: {correlationId}";

            var response = ApiResponse<object>.Fail("An unexpected error occurred. Please try again later.", new() { errorDetail });
            var json = JsonSerializer.Serialize(response, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase });

            return context.Response.WriteAsync(json);
        }
    }
}

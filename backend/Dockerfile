# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

# Copy all source files (excluding bin and obj via .dockerignore)
COPY . .

# Publish directly without solution file (restores and compiles Visionary.Api cleanly)
WORKDIR /source/src/Visionary.Api
RUN dotnet publish Visionary.Api.csproj -c Release -o /app/publish

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

ENTRYPOINT ["dotnet", "Visionary.Api.dll"]

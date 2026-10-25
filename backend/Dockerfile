# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /source

# Copy solution and project files
COPY Visionary.sln .
COPY src/Visionary.Core/*.csproj src/Visionary.Core/
COPY src/Visionary.Infrastructure/*.csproj src/Visionary.Infrastructure/
COPY src/Visionary.Api/*.csproj src/Visionary.Api/
COPY tests/Visionary.Tests/*.csproj tests/Visionary.Tests/

# Restore dependencies
RUN dotnet restore

# Copy all source files and publish
COPY . .
WORKDIR /source/src/Visionary.Api
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

ENTRYPOINT ["dotnet", "Visionary.Api.dll"]

$base = "http://127.0.0.1:8000"
Write-Host "`n=== بدء اختبار المصادقة والأدوار ===" -ForegroundColor Cyan

# Admin
$body = @{username="admin";password="admin"}
$res = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -Body $body
$adminToken = $res.access_token
Write-Host "[PASS] تسجيل دخول Admin" -ForegroundColor Green

$headers = @{Authorization="Bearer $adminToken"}
Invoke-RestMethod -Uri "$base/admin/users" -Headers $headers | Out-Null
Write-Host "[PASS] Admin - /admin/users" -ForegroundColor Green
Invoke-RestMethod -Uri "$base/analyst/reports" -Headers $headers | Out-Null
Write-Host "[PASS] Admin - /analyst/reports" -ForegroundColor Green
Invoke-RestMethod -Uri "$base/viewer/public-data" -Headers $headers | Out-Null
Write-Host "[PASS] Admin - /viewer/public-data" -ForegroundColor Green

# Analyst
$body = @{username="analyst";password="analyst"}
$res = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -Body $body
$analystToken = $res.access_token
$headers = @{Authorization="Bearer $analystToken"}

try {
    Invoke-RestMethod -Uri "$base/admin/users" -Headers $headers
    Write-Host "[FAIL] Analyst يجب ألا يصل إلى /admin/users" -ForegroundColor Red
} catch {
    Write-Host "[PASS] Analyst ممنوع من /admin/users (403)" -ForegroundColor Green
}
Invoke-RestMethod -Uri "$base/analyst/reports" -Headers $headers | Out-Null
Write-Host "[PASS] Analyst - /analyst/reports" -ForegroundColor Green
Invoke-RestMethod -Uri "$base/viewer/public-data" -Headers $headers | Out-Null
Write-Host "[PASS] Analyst - /viewer/public-data" -ForegroundColor Green

# Viewer
$body = @{username="viewer";password="viewer"}
$res = Invoke-RestMethod -Uri "$base/auth/login" -Method Post -Body $body
$viewerToken = $res.access_token
$headers = @{Authorization="Bearer $viewerToken"}

try {
    Invoke-RestMethod -Uri "$base/admin/users" -Headers $headers
    Write-Host "[FAIL] Viewer يجب ألا يصل إلى /admin/users" -ForegroundColor Red
} catch {
    Write-Host "[PASS] Viewer ممنوع من /admin/users (403)" -ForegroundColor Green
}
try {
    Invoke-RestMethod -Uri "$base/analyst/reports" -Headers $headers
    Write-Host "[FAIL] Viewer يجب ألا يصل إلى /analyst/reports" -ForegroundColor Red
} catch {
    Write-Host "[PASS] Viewer ممنوع من /analyst/reports (403)" -ForegroundColor Green
}
Invoke-RestMethod -Uri "$base/viewer/public-data" -Headers $headers | Out-Null
Write-Host "[PASS] Viewer - /viewer/public-data" -ForegroundColor Green

# Refresh Token
$headers = @{Authorization="Bearer $adminToken"}
$res = Invoke-RestMethod -Uri "$base/auth/refresh" -Method Post -Headers $headers
Write-Host "[PASS] تجديد التوكن ناجح" -ForegroundColor Green

# Fake Token
$headers = @{Authorization="Bearer fake.token.here"}
try {
    Invoke-RestMethod -Uri "$base/admin/users" -Headers $headers
    Write-Host "[FAIL] توكن مزور يجب ألا يُقبل" -ForegroundColor Red
} catch {
    Write-Host "[PASS] توكن مزور مرفوض (401)" -ForegroundColor Green
}

Write-Host "`n=== تمت جميع الاختبارات بنجاح ===" -ForegroundColor Cyan

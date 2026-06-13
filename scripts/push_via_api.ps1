# Push commit lên GitHub qua REST API — dùng khi git push bị proxy công ty chặn (Connection reset).
# Chạy: powershell -File scripts\push_via_api.ps1
# Sau khi chạy xong: git fetch origin; git status (local sẽ lệch 1 commit cùng nội dung —
# chạy: git reset --hard origin/master để đồng bộ).
$ErrorActionPreference = 'Stop'
$gh = "$env:LOCALAPPDATA\gh-cli\bin\gh.exe"
$repo = "repos/Tuon-Tun/kcn-review"
$root = Split-Path -Parent $PSScriptRoot
$tmp = Join-Path $env:TEMP "ghapi"
New-Item -ItemType Directory -Force $tmp | Out-Null

# 1. Xác định commit gốc trên remote và các file local khác biệt so với nó
$base = & $gh api "$repo/branches/master" --jq .commit.sha
$baseTree = & $gh api "$repo/git/commits/$base" --jq .tree.sha
# --no-renames: ép rename thành xóa+thêm để đường dẫn CŨ cũng được xử lý (xóa trên remote)
$files = @(git -C $root diff --name-only --no-renames $base HEAD) | Where-Object { $_ }
if (-not $files) { Write-Output "Khong co gi de push."; exit 0 }
Write-Output "Base: $base | files: $($files.Count)"

# 2. Tạo blob cho từng file — lấy bytes từ HEAD (đã qua chuẩn hóa autocrlf của git),
#    KHÔNG đọc thẳng từ đĩa (file đĩa có thể là CRLF -> lệch với quy ước LF của repo)
#    File bị XÓA/DI CHUYỂN trong HEAD -> entry sha=null để GitHub xóa khỏi tree
#    (thiếu bước này thì file xóa local vẫn sống mãi trên remote!)
$entries = @()
foreach ($f in $files) {
    cmd /c "git -C `"$root`" cat-file -e `"HEAD:$f`" 2>nul"
    if ($LASTEXITCODE -ne 0) {
        $entries += @{ path = $f; mode = "100644"; type = "blob"; sha = $null }
        Write-Output "  xoa  $f"
        continue
    }
    $tmpBlob = Join-Path $tmp "raw.bin"
    cmd /c "git -C `"$root`" cat-file blob `"HEAD:$f`" > `"$tmpBlob`""
    $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($tmpBlob))
    $payload = Join-Path $tmp "blob.json"
    [IO.File]::WriteAllText($payload, ('{"encoding":"base64","content":"' + $b64 + '"}'))
    $sha = & $gh api "$repo/git/blobs" --method POST --input $payload --jq .sha
    $entries += @{ path = $f; mode = "100644"; type = "blob"; sha = $sha }
    Write-Output "  blob $f -> $($sha.Substring(0,8))"
}

# 3. Tạo tree + commit + cập nhật ref
$treePayload = Join-Path $tmp "tree.json"
[IO.File]::WriteAllText($treePayload, (@{ base_tree = $baseTree; tree = $entries } | ConvertTo-Json -Depth 5))
$treeSha = & $gh api "$repo/git/trees" --method POST --input $treePayload --jq .sha
$msg = (git -C $root log -1 --pretty=%B) -join "`n"
$commitPayload = Join-Path $tmp "commit.json"
[IO.File]::WriteAllText($commitPayload, (@{ message = $msg; tree = $treeSha; parents = @($base) } | ConvertTo-Json -Depth 5))
$commitSha = & $gh api "$repo/git/commits" --method POST --input $commitPayload --jq .sha
$refPayload = Join-Path $tmp "ref.json"
[IO.File]::WriteAllText($refPayload, ('{"sha":"' + $commitSha + '"}'))
& $gh api "$repo/git/refs/heads/master" --method PATCH --input $refPayload --jq .object.sha
Write-Output "DA PUSH QUA API: $commitSha"
Remove-Item $tmp -Recurse -Force

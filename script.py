<?php
// Baca URL stream dari file
$source = trim(@file_get_contents("latest.txt"));
if (!$source || strpos($source, "#ERROR") !== false) {
    header("HTTP/1.1 503 Service Unavailable");
    echo "Stream tidak tersedia.";
    exit;
}

// Ambil parameter segmen atau manifest
$path = isset($_GET['path']) ? $_GET['path'] : '';
$target = $source;

// Jika segmen, ubah URL dasar
if ($path && preg_match('/\.m4s$|\.mp4$/', $path)) {
    $base = preg_replace('/manifest\.mpd.*/', '', $source);
    $target = $base . $path;
} elseif ($path && preg_match('/\.mpd$/', $path)) {
    $target = $source;
}

// Ambil konten dari sumber
$opts = [
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: Mozilla/5.0\r\n"
    ]
];
$context = stream_context_create($opts);
$content = @file_get_contents($target, false, $context);

if (!$content) {
    header("HTTP/1.1 502 Bad Gateway");
    echo "Gagal mengambil stream.";
    exit;
}

// Jika manifest, rewrite URL segmen
if (preg_match('/\.mpd$/', $target)) {
    $domain = $_SERVER['HTTP_HOST'];
    $proxy_base = "https://$domain/proxy.php?path=";
    $content = str_replace("https://", $proxy_base);
}

// Set header sesuai tipe
if (preg_match('/\.mpd$/', $target)) {
    header("Content-Type: application/dash+xml");
} elseif (preg_match('/\.m4s$/', $target)) {
    header("Content-Type: video/iso.segment");
} else {
    header("Content-Type: application/octet-stream");
}

echo $content;

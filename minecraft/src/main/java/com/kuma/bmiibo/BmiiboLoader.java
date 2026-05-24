package com.kuma.bmiibo;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class BmiiboLoader {
    private static final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB 安全防線

    public static class BmiiboResult {
        public String name;
        public String id;
        public String author;
        public byte[] iconBytes;
    }

    public static BmiiboResult loadBmiibo(File file) throws Exception {
        if (file.length() > MAX_FILE_SIZE) {
            throw new SecurityException("檔案大小超過 5MB 安全限制！");
        }

        BmiiboResult result = new BmiiboResult();
        boolean hasJson = false;
        boolean hasIcon = false;

        try (ZipInputStream zis = new ZipInputStream(new FileInputStream(file))) {
            ZipEntry entry;
            while ((entry = zis.getNextEntry()) != null) {
                if (entry.getName().equals("bmiibo.json")) {
                    // 讀取 JSON 數據
                    BufferedReader reader = new BufferedReader(new InputStreamReader(zis, StandardCharsets.UTF_8));
                    JsonObject json = JsonParser.parseReader(reader).getAsJsonObject();
                    result.name = json.get("name").getAsString();
                    result.id = json.get("id").getAsString();
                    result.author = json.get("author").getAsString();
                    hasJson = true;
                } else if (entry.getName().equals("icon.png")) {
                    // 讀取圖片位元組
                    ByteArrayOutputStream baos = new ByteArrayOutputStream();
                    byte[] buffer = new byte[1024];
                    int len;
                    while ((len = zis.read(buffer)) > 0) {
                        baos.write(buffer, 0, len);
                    }
                    result.iconBytes = baos.toByteArray();
                    hasIcon = true;
                }
                zis.closeEntry();
            }
        }

        if (!hasJson || !hasIcon) {
            throw new FormatFlagsConversionMismatchException("`.bmiibo` 結構毀損，缺少關鍵檔案！");
        }

        return result;
    }
}

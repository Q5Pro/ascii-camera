# 📷 ASCII Camera

Webcam görüntünüzü (veya herhangi bir resmi) gerçek zamanlı olarak
terminal ASCII art'a çeviren araç. Renkli veya siyah-beyaz modda çalışır.

## Özellikler

- 🎥 Webcam'den gerçek zamanlı ASCII dönüşümü
- 🖼️ Statik resim dosyalarını da dönüştürebilir
- 🌈 Renkli (ANSI true-color) veya klasik siyah-beyaz mod
- 💾 Sonucu .txt dosyası olarak kaydedebilir
- 📐 Ayarlanabilir genişlik/detay seviyesi

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
# Webcam ile canlı ASCII (Ctrl+C ile çıkış)
python3 ascii_cam.py

# Renkli mod
python3 ascii_cam.py --color

# Bir resmi dönüştür
python3 ascii_cam.py --image foto.jpg --width 120

# Sonucu dosyaya kaydet
python3 ascii_cam.py --image foto.jpg --save cikti.txt

# İkinci kamerayı kullan (birden fazla kamera varsa)
python3 ascii_cam.py --camera 1
```

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| `--image` | Webcam yerine resim dosyası kullan | yok |
| `--width` | Çıktı karakter genişliği | 100 |
| `--color` | Renkli ASCII çıktısı | kapalı |
| `--camera` | Kamera index numarası | 0 |
| `--save` | Çıktıyı dosyaya kaydet (resim modunda) | yok |

## Nasıl çalışır?

Her piksel gri tonlamaya çevrilir, parlaklık değeri 0-255 aralığında
`" .:-=+*#%@"` karakter setine eşlenir (boşluk en karanlık, `@` en parlak).
Renkli modda her karakter, orijinal pikselin RGB değeriyle ANSI true-color
kodu kullanılarak boyanır.

## Lisans

MIT

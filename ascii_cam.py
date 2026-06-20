"""
ASCII Camera
============
Bilgisayarınızın kamerasından (veya bir resim/video dosyasından) görüntü alıp
gerçek zamanlı olarak ASCII art'a çeviren terminal aracı.

Kullanım:
    python ascii_cam.py                      # Webcam ile canlı ASCII
    python ascii_cam.py --image foto.jpg     # Tek bir resmi dönüştür
    python ascii_cam.py --width 120 --color  # Renkli, daha geniş çıktı

Gereksinimler:
    pip install opencv-python numpy
"""

import argparse
import sys
import time

import cv2 as cv2
import numpy as np

# Karanlıktan aydınlığa doğru karakter seti (yoğunluk eşlemesi için)
ASCII_CHARS = " .:-=+*#%@"


def pixel_to_char(value: int, charset: str = ASCII_CHARS) -> str:
    """0-255 arası parlaklık değerini bir ASCII karaktere eşler."""
    scale = len(charset) - 1
    index = int((value / 255) * scale)
    return charset[index]


def frame_to_ascii(frame, width: int = 100, color: bool = False) -> str:
    """Bir OpenCV görüntü karesini ASCII art string'ine çevirir."""
    height, orig_width = frame.shape[:2]
    aspect_ratio = height / orig_width
    # Karakterler genellikle piksellerden daha "yüksek" görünür, bu yüzden 0.55 ile düzeltiyoruz
    new_height = int(width * aspect_ratio * 0.55)
    resized = cv2.resize(frame, (width, max(new_height, 1)))

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    lines = []
    for y in range(resized.shape[0]):
        row_chars = []
        for x in range(resized.shape[1]):
            char = pixel_to_char(gray[y, x])
            if color:
                b, g, r = resized[y, x]
                row_chars.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
            else:
                row_chars.append(char)
        lines.append("".join(row_chars))
    return "\n".join(lines)


def run_webcam(width: int, color: bool, camera_index: int = 0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Kamera açılamadı. --image ile bir dosya deneyebilirsiniz.")
        sys.exit(1)

    print("ASCII kamera başlatıldı. Çıkmak için Ctrl+C.\n")
    time.sleep(1)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)  # Ayna efekti
            ascii_frame = frame_to_ascii(frame, width=width, color=color)
            sys.stdout.write("\033[H\033[J")  # Ekranı temizle
            sys.stdout.write(ascii_frame + "\n")
            sys.stdout.flush()
            time.sleep(0.04)  # ~25 FPS hedefi
    except KeyboardInterrupt:
        print("\nKapatılıyor...")
    finally:
        cap.release()


def run_image(path: str, width: int, color: bool, output: str = None):
    frame = cv2.imread(path)
    if frame is None:
        print(f"Resim okunamadı: {path}")
        sys.exit(1)

    ascii_art = frame_to_ascii(frame, width=width, color=color)
    print(ascii_art)

    if output:
        # Renk kodlarını çıkarmadan düz metin olarak kaydet
        plain = frame_to_ascii(frame, width=width, color=False)
        with open(output, "w", encoding="utf-8") as f:
            f.write(plain)
        print(f"\nASCII art şuraya kaydedildi: {output}")


def main():
    parser = argparse.ArgumentParser(description="Webcam veya resmi ASCII art'a çevirir")
    parser.add_argument("--image", type=str, help="Webcam yerine bir resim dosyası kullan")
    parser.add_argument("--width", type=int, default=100, help="Çıktı karakter genişliği")
    parser.add_argument("--color", action="store_true", help="Renkli ASCII çıktısı")
    parser.add_argument("--camera", type=int, default=0, help="Kamera index numarası")
    parser.add_argument("--save", type=str, help="Resim modunda çıktıyı dosyaya kaydet (.txt)")
    args = parser.parse_args()

    if args.image:
        run_image(args.image, args.width, args.color, args.save)
    else:
        run_webcam(args.width, args.color, args.camera)


if __name__ == "__main__":
    main()

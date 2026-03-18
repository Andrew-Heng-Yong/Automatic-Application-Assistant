from pathlib import Path
import cv2


def load_image(path: Path, grayscale: bool):
    flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
    img = cv2.imread(str(path), flag)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img


def compare_images(template_path: Path, image_path: Path, grayscale: bool = True):
    template = load_image(template_path, grayscale)
    image = load_image(image_path, grayscale)

    if image.shape[0] < template.shape[0] or image.shape[1] < template.shape[1]:
        raise ValueError("Second image must be at least as large as the first image.")

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return float(max_val), max_loc, template.shape[:2], image.shape[:2]


def find_two_images(script_dir: Path):
    exts = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
    images = sorted(
        [p for p in script_dir.iterdir() if p.is_file() and p.suffix.lower() in exts]
    )

    if len(images) < 2:
        raise FileNotFoundError("Need at least 2 image files in the same folder as this script.")

    return images[0], images[1]


def main():
    script_dir = Path(__file__).resolve().parent
    template_path, image_path = find_two_images(script_dir)

    score, loc, template_shape, image_shape = compare_images(
        template_path,
        image_path,
        grayscale=True,
    )

    print(f"template: {template_path.name}")
    print(f"image:    {image_path.name}")
    print("mode:     grayscale")
    print("method:   cv2.TM_CCOEFF_NORMED")
    print(f"score:    {score:.6f}")
    print(f"found at: {loc}")
    print(f"template size: {template_shape[1]}x{template_shape[0]}")
    print(f"image size:    {image_shape[1]}x{image_shape[0]}")


if __name__ == "__main__":
    main()
from gradio_client import Client
import shutil
import cv2
from pathlib import Path

clean_prompt = "Wide theatrical establishing shot of a grand royal rose garden courtyard in Alice in Wonderland, Disney Pixar 3D animated fantasy movie art style, cinematic theatrical lighting, 16:9 widescreen. An empty grand symmetrical royal courtyard with polished red-and-white checkered marble stone tiles leading toward towering gilded golden palace gates with ornate heart motifs in the distance. Towering manicured dark green hedge walls with heart-shaped arches, overflowing with blooming velvet red roses and white roses. Warm glowing golden palace lanterns, soft volumetric god-rays through gentle evening mist. Dramatic twilight crimson and purple evening sky. Beautiful theatrical stage set backdrop, completely empty scenery, no people, no characters, no actors, no text."

print("Connecting to FLUX.1-schnell...")
client = Client("black-forest-labs/FLUX.1-schnell")

print("Generating image with clean prompt...")
result = client.predict(
    prompt=clean_prompt,
    seed=42,
    randomize_seed=True,
    width=1024,
    height=576,
    num_inference_steps=4,
    api_name="/infer"
)

print("Result received:", result)
image_dict = result[0]
image_path = image_dict["path"] if isinstance(image_dict, dict) else image_dict
print("Generated image temporary path:", image_path)

# Destination paths
dest_img = Path("assets/images/scene4_rosegarden.png")
dest_jpg = Path("assets/images/scene4_rosegarden.jpg")

# Upscale/resize to exact 1920x1080 16:9
img = cv2.imread(str(image_path))
h, w, _ = img.shape
print(f"Original generated size: {w}x{h}")

img_1080p = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite(str(dest_img), img_1080p)
cv2.imwrite(str(dest_jpg), img_1080p)

# Also copy to brain artifact directory for inspection
brain_dest = Path(r"C:\Users\hyder\.gemini\antigravity\brain\599b619f-5b6a-462d-b713-4a8976f07de9\scene4_rosegarden_flux.png")
shutil.copy(dest_img, brain_dest)

print("Saved to assets/images/scene4_rosegarden.png (1920x1080)")
print("Saved to brain directory:", brain_dest)

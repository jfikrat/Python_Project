import base64
import os
from io import BytesIO
from PIL import Image
from config import settings


class ImageService:
    """Service for image processing and conversion."""

    @staticmethod
    def validate_image(file_content: bytes, filename: str) -> tuple[bool, str | None]:
        """
        Validate uploaded image file.

        Args:
            file_content: Raw file bytes
            filename: Original filename

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check file size
        if len(file_content) > settings.max_upload_size:
            max_mb = settings.max_upload_size / (1024 * 1024)
            return False, f"File size exceeds {max_mb}MB limit"

        # Check file extension
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.allowed_image_types:
            allowed = ", ".join(settings.allowed_image_types)
            return False, f"Invalid file type. Allowed: {allowed}"

        # Validate it's actually an image
        try:
            image = Image.open(BytesIO(file_content))
            image.verify()
        except Exception:
            return False, "Invalid or corrupted image file"

        return True, None

    @staticmethod
    def to_base64_data_url(file_content: bytes, filename: str) -> str:
        """
        Convert image bytes to base64 data URL for OpenAI API.

        Args:
            file_content: Raw image bytes
            filename: Original filename (for MIME type detection)

        Returns:
            Data URL string (data:image/jpeg;base64,...)
        """
        ext = os.path.splitext(filename)[1].lower()

        # Determine MIME type
        mime_mapping = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        mime_type = mime_mapping.get(ext, "image/jpeg")

        # Encode to base64
        b64_string = base64.b64encode(file_content).decode("utf-8")

        return f"data:{mime_type};base64,{b64_string}"

    @staticmethod
    def optimize_for_api(file_content: bytes, max_dimension: int = 2048) -> bytes:
        """
        Optimize image for OpenAI API (resize if too large).

        Args:
            file_content: Raw image bytes
            max_dimension: Maximum width or height

        Returns:
            Optimized image bytes
        """
        image = Image.open(BytesIO(file_content))

        # Check if resizing needed
        if max(image.size) > max_dimension:
            # Calculate new size maintaining aspect ratio
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # Convert to RGB if necessary
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")

        # Save to bytes
        output = BytesIO()
        image.save(output, format="JPEG", quality=85, optimize=True)
        return output.getvalue()

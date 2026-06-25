import fitz
import hashlib
import os


def generate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def check_pdf_metadata(file_path):
    result = {
        "sha256": generate_sha256(file_path),
        "metadata": {},
        "warnings": []
    }

    ext = os.path.splitext(file_path)[1].lower()

    if ext != ".pdf":
        result["warnings"].append(
            "Metadata check currently supports PDF files only."
        )
        return result

    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        result["metadata"] = metadata

        suspicious_keywords = [
            "word",
            "canva",
            "photoshop",
            "editor",
            "scanner"
        ]

        for key, value in metadata.items():
            if value:
                value_lower = str(value).lower()

                for keyword in suspicious_keywords:
                    if keyword in value_lower:
                        result["warnings"].append(
                            f"Suspicious metadata: {key} contains {value}"
                        )

        creation_date = metadata.get("creationDate")
        modified_date = metadata.get("modDate")

        if not creation_date:
            result["warnings"].append(
                "Missing PDF creation date."
            )

        if creation_date and modified_date:
            if creation_date != modified_date:
                result["warnings"].append(
                    "PDF was modified after creation."
                )

    except Exception as e:
        result["warnings"].append(
            f"Could not read metadata: {e}"
        )

    return result
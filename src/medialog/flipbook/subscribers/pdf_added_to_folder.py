# -*- coding: utf-8 -*-
import os
import tempfile
from pdf2image import convert_from_path

from plone import api
from zope.component.hooks import getSite


def handler(obj, event):
    """ Event handler -  a PDF file is added, convert each page to an image."""
    
    # Only run for PDF files
    if not hasattr(obj, 'file'):
        return
    if not obj.file:
        return

    filename = obj.file.filename.lower()
    if not filename.endswith(".pdf"):
        return

    # Create a temporary file for Poppler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(obj.file.data)
        tmp.flush()
        pdf_path = tmp.name

    # Convert PDF -> list of PIL images
    try:
        images = convert_from_path(pdf_path, dpi=200)
    except Exception as e:
        import logging
        logger = logging.getLogger("your.package")
        logger.error("PDF conversion failed: %s", e)
        return
    finally:
        # Clean up the temp PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    # Add each page as a Plone Image object
    parent = obj.aq_parent
    base_id = os.path.splitext(obj.getId())[0]

    for index, pil_image in enumerate(images, start=1):
        image_id = f"{base_id}-page-{index}.png"

        # Convert PIL image to raw bytes
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp:
            pil_image.save(img_tmp, format="PNG")
            img_tmp.flush()
            image_data = img_tmp.read()

        # Create the Image item in the same folder
        api.content.create(
            container=parent,
            type="Image",
            id=image_id,
            title=f"{obj.Title()} — Page {index}",
            image=image_data,
        )

        os.remove(img_tmp.name)

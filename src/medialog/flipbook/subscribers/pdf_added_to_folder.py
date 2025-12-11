# -*- coding: utf-8 -*-
import os
import tempfile
from pdf2image import convert_from_path

from plone import api
# from zope.component.hooks import getSite
# from zope.globalrequest import getRequest
# from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from io import BytesIO




def handler(obj, event):
    """ Event handler -  a PDF file is added, convert each page to an image."""
    
        
    # Only run for PDF files
    if not hasattr(obj, 'file'):
        return
    if not obj.file:
        return
    
    if obj.aq_parent.layout is None:
        return

    # Only run if URL contains flipbook-view
    if "flipbook-view" not in obj.aq_parent.layout:
        return


    filename = obj.file.filename.lower()
    # TO DO, maybe check for mime type instead of extension
    if not filename.endswith(".pdf"):
        return

    # Create a temporary file for Poppler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(obj.file.data)
        tmp.flush()
        pdf_path = tmp.name

    # Convert PDF -> list of PIL images
    try:
        images = convert_from_path(pdf_path, dpi=250)
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
        image_id = f"{base_id}-page-{index}.jpg"

        # Convert PIL Image → JPG bytes
        buf = BytesIO()
        pil_image.save(buf, format="JPEG")
        image_bytes = buf.getvalue()

        api.content.create(
            container=parent,
            type="Image",
            id=image_id,
            title=f"{obj.Title()} — Page {index}",
            image=NamedBlobImage(
                data=image_bytes,
                filename=f"{base_id}-page-{index}.jpg"
            ),
        )

import os
import uuid

from django.core.files.storage import Storage
from django.core.files.base import ContentFile

from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


class SupabaseStorage(Storage):

    def _save(self, name, content):

        # Preserve Django's upload_to folder
        folder = os.path.dirname(name)

        extension = os.path.splitext(name)[1]

        filename = f"{uuid.uuid4()}{extension}"

        if folder:
            path = f"{folder}/{filename}"
        else:
            path = filename

        supabase.storage.from_(SUPABASE_BUCKET).upload(
            path,
            content.read(),
            file_options={
                "content-type": getattr(content, "content_type", "application/octet-stream")
            },
        )

        return path


    def url(self, name):

        return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(name)


    def exists(self, name):
        return False


    def delete(self, name):

        supabase.storage.from_(SUPABASE_BUCKET).remove([name])


    def open(self, name, mode="rb"):

        data = supabase.storage.from_(SUPABASE_BUCKET).download(name)

        return ContentFile(data)
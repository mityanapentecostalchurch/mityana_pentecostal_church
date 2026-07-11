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

        extension = os.path.splitext(name)[1]
        filename = f"{uuid.uuid4()}{extension}"

        print("=" * 60)
        print("Uploading to Supabase...")
        print("Bucket:", SUPABASE_BUCKET)
        print("Filename:", filename)
        print("Content-Type:", getattr(content, "content_type", None))

        try:

            response = (
                supabase.storage
                .from_(SUPABASE_BUCKET)
                .upload(
                    path=filename,
                    file=content.read(),
                    file_options={
                        "content-type": getattr(
                            content,
                            "content_type",
                            "application/octet-stream"
                        )
                    }
                )
            )

            print("Upload response:")
            print(response)

        except Exception as e:

            print("SUPABASE ERROR:")
            print(type(e))
            print(e)

            raise

        return filename


    def url(self, name):

        return supabase.storage.from_(SUPABASE_BUCKET).get_public_url(name)


    def exists(self, name):
        return False


    def delete(self, name):

        supabase.storage.from_(SUPABASE_BUCKET).remove([name])


    def open(self, name, mode="rb"):

        data = supabase.storage.from_(SUPABASE_BUCKET).download(name)

        return ContentFile(data)
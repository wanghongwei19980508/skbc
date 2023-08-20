from utils.api import APIView

from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementAPI(APIView):
    def get(self, request):
        announcement_id = request.GET.get("announcement_id")
        if announcement_id:
            try:
                announcement = Announcement.objects.get(id=announcement_id, visible=True)
                return self.success(AnnouncementSerializer(announcement).data)
            except Announcement.DoesNotExist:
                return self.error("Announcement does not exist")
        announcements = Announcement.objects.filter(visible=True)
        return self.success(self.paginate_data(request, announcements, AnnouncementSerializer))

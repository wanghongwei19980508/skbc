from utils.api import APIView, validate_serializer
from record.models import FollowUpRecord, OperationRecord, RollCallRecord
from record.serializer import CreateFollowUpRecordSerializer, EditFollowUpRecordSerializer, FollowUpRecordSerializer
from account.models import User, Clue
from django.utils.timezone import now

class FollowUpRecordAPI(APIView):
    @validate_serializer(CreateFollowUpRecordSerializer)
    def post(self, request):
        data = request.data
        clue = Clue.objects.get(id=data["student"])
        follow_up_person = User.objects.get(id=request.user.id)
        FollowUpRecord.objects.create(
            follow_up_person=follow_up_person,
            plan_follow_up_time=now(),
            follow_up_stage=data["follow_up_stage"],
            follow_up_content=data["follow_up_content"],
            actual_follow_up_time=now(),
            follow_up_method=data["follow_up_method"],
            student=clue,
            create_time=now(),
        )
        if data["next_follow_up_time"] != None:
            FollowUpRecord.objects.create(
                follow_up_person=follow_up_person,
                plan_follow_up_time=data["next_follow_up_time"],
                follow_up_content=data["next_follow_up_task"],
                student=clue,
                create_time=now(),
            )
        return self.success()
    
    @validate_serializer(EditFollowUpRecordSerializer)
    def put(self, request):
        data = request.data
        clue = Clue.objects.get(id=data["student"])
        follow_up_person = User.objects.get(id=request.user.id)
        id = data["id"]
        FollowUpRecord.objects.filter(id=id).update(
            follow_up_person=follow_up_person,
            follow_up_stage=data["follow_up_stage"],
            follow_up_content=data["follow_up_content"],
            actual_follow_up_time=data["actual_follow_up_time"],
            follow_up_method=data["follow_up_method"],
            student=clue
        )
        if data["next_follow_up_time"] != None:
            FollowUpRecord.objects.create(
                follow_up_person=follow_up_person,
                plan_follow_up_time=data["next_follow_up_time"],
                follow_up_content=data["next_follow_up_task"],
                student=clue,
                create_time=now(),
            )
        return self.success()
    
    def get(self, request):
        data = request.GET
        if data.get('id'):
            id = data.get('id')
            follow_up_record = FollowUpRecord.objects.get(id=id)
            return self.success(FollowUpRecordSerializer(follow_up_record).data)
        follow_up_records = FollowUpRecord.objects.all().order_by('-create_time')
        if data.get('student'):
            student = Clue.objects.get(id=data.get('student'))
            follow_up_records = follow_up_records.filter(student=student)
        if data.get('follow_up_person'):
            follow_up_person = User.objects.get(id=data.get('follow_up_person'))
            follow_up_records = follow_up_records.filter(follow_up_person=follow_up_person)
        if data.get('follow_up_stage'):
            follow_up_stage = data.get('follow_up_stage')
            follow_up_records = follow_up_records.filter(follow_up_stage=follow_up_stage)
        if data.get('follow_up_method'):
            follow_up_method = data.get('follow_up_method')
            follow_up_records = follow_up_records.filter(follow_up_method=follow_up_method)
        if data.get('start_time'):
            start_time = data.get('start_time')
            follow_up_records = follow_up_records.filter(create_time__gte=start_time)
        if data.get('end_time'):
            end_time = data.get('end_time')
            follow_up_records = follow_up_records.filter(create_time__lte=end_time)
        return self.success(self.paginate_data(request, follow_up_records, FollowUpRecordSerializer))
        
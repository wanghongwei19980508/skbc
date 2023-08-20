import os
import re
import xlsxwriter

from django.conf import settings
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from options.options import SysOptions
from submission.models import Submission
from utils.api import APIView, validate_serializer
from utils.shortcuts import rand_str
from utils.constants import TMP_PATH

from ..decorators import super_admin_required
from ..models import AdminType, Permission, User, UserProfile, Clue, FollowStatus, StudentStatus
from ..serializers import EditUserSerializer, UserAdminSerializer, GenerateUserSerializer, ClueSerializer
from ..serializers import ImportUserSeralizer, PicUploadForm

class UserAdminAPI(APIView):
    @validate_serializer(ImportUserSeralizer)
    @super_admin_required
    def post(self, request):
        """
        Import User
        """
        data = request.data["users"]

        user_list = []
        for user_data in data:
            if len(user_data) != 4 or len(user_data[0]) > 32:
                return self.error(f"Error occurred while processing data '{user_data}'")
            user_list.append(User(username=user_data[0], password=make_password(user_data[1]), email=user_data[2]))

        try:
            with transaction.atomic():
                ret = User.objects.bulk_create(user_list)
                UserProfile.objects.bulk_create([UserProfile(user=ret[i], real_name=data[i][3]) for i in range(len(ret))])
            return self.success()
        except IntegrityError as e:
            # Extract detail from exception message
            #    duplicate key value violates unique constraint "user_username_key"
            #    DETAIL:  Key (username)=(root11) already exists.
            return self.error(str(e).split("\n")[1])

    @validate_serializer(EditUserSerializer)
    @super_admin_required
    def put(self, request):
        """
        Edit user api
        """
        data = request.data
        try:
            user = User.objects.get(id=data["id"])
        except User.DoesNotExist:
            return self.error("User does not exist")
        if User.objects.filter(username=data["username"].lower()).exclude(id=user.id).exists():
            return self.error("Username already exists")
        if User.objects.filter(email=data["email"].lower()).exclude(id=user.id).exists():
            return self.error("Email already exists")
        if User.objects.filter(phone=data["phone"]).exclude(id=user.id).exists():
            return self.error("Phone already exists")

        pre_username = user.username
        user.username = data["username"].lower()
        user.email = data["email"].lower()
        user.phone = data['phone']
        user.admin_type = data["admin_type"]
        user.is_disabled = data["is_disabled"]

        if data["admin_type"] == AdminType.ADMIN:
            user.problem_permission = data["problem_permission"]
        elif data["admin_type"] == AdminType.SUPER_ADMIN:
            user.problem_permission = Permission.ALL
        else:
            user.problem_permission = Permission.NONE
        
        if data["admin_type"] == AdminType.ADMIN:
            user.course_permission = data["course_permission"]
        elif data["admin_type"] == AdminType.SUPER_ADMIN:
            user.course_permission = Permission.ALL
        else:
            user.course_permission = Permission.NONE

        if data["password"]:
            user.set_password(data["password"])

        if data["open_api"]:
            # Avoid reset user appkey after saving changes
            if not user.open_api:
                user.open_api_appkey = rand_str()
        else:
            user.open_api_appkey = None
        user.open_api = data["open_api"]

        if data["two_factor_auth"]:
            # Avoid reset user tfa_token after saving changes
            if not user.two_factor_auth:
                user.tfa_token = rand_str()
        else:
            user.tfa_token = None

        user.two_factor_auth = data["two_factor_auth"]

        user.save()
        if pre_username != user.username:
            Submission.objects.filter(username=pre_username).update(username=user.username)

        UserProfile.objects.filter(user=user).update(real_name=data["real_name"])
        return self.success(UserAdminSerializer(user).data)

    @super_admin_required
    def get(self, request):
        """
        User list api / Get user by id
        """
        user_id = request.GET.get("id")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return self.error("User does not exist")
            return self.success(UserAdminSerializer(user).data)

        user = User.objects.all().order_by("-create_time")

        keyword = request.GET.get("keyword", None)
        if keyword:
            user = user.filter(Q(username__icontains=keyword) |
                               Q(userprofile__real_name__icontains=keyword) |
                               Q(email__icontains=keyword) | Q(phone__icontains=keyword))
        return self.success(self.paginate_data(request, user, UserAdminSerializer))

    @super_admin_required
    def delete(self, request):
        id = request.GET.get("id")
        if not id:
            return self.error("Invalid Parameter, id is required")
        ids = id.split(",")
        if str(request.user.id) in ids:
            return self.error("Current user can not be deleted")
        User.objects.filter(id__in=ids).delete()
        return self.success()

'''
图片上传接口
'''
class PicUploadAPI(APIView):
    request_parsers = ()
    @super_admin_required
    def post(self, request):
        """
        upload pic
        """
        form = PicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data["image"]
            itemId = form.cleaned_data["itemId"]
            subject = form.cleaned_data['subject']
        else:
            return self.error("Invalid file content")
        if pic.size > 2 * 1024 * 1024:
            return self.error("Picture is too large")
        suffix = os.path.splitext(pic.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")

        name = rand_str(10) + suffix
        
        if subject == 'softwares':
            with open(os.path.join(settings.SOFTWARE_UPLOAD_DIR, name), "wb") as img:
                for chunk in pic:
                    img.write(chunk)
            softwares = SysOptions.softwares
            if len(softwares) == itemId:
                return self.success(f"{settings.SOFTWARE_URI_PREFIX}/{name}")
            origin_path = os.path.join(settings.DATA_DIR, softwares[itemId]['pic'])
            if os.path.exists(origin_path):
                os.remove(origin_path)
            softwares[itemId]['pic'] = f"{settings.SOFTWARE_URI_PREFIX}/{name}"
            setattr(SysOptions, "softwares", softwares)
        elif subject == 'slideshows':
            with open(os.path.join(settings.SLIDESHOW_UPLOAD_DIR, name), "wb") as img:
                for chunk in pic:
                    img.write(chunk)
            slideshows = SysOptions.slideshows
            if len(slideshows) == itemId:
                return self.success(f"{settings.SLIDESHOW_URI_PREFIX}/{name}")
            origin_path = os.path.join(settings.DATA_DIR, slideshows[itemId]['pic'])
            if os.path.exists(origin_path):
                os.remove(origin_path)
            slideshows[itemId]['pic'] = f"{settings.SLIDESHOW_URI_PREFIX}/{name}"
            setattr(SysOptions, "slideshows", slideshows)
        return self.success("Succeeded")


class GenerateUserAPI(APIView):
    @super_admin_required
    def get(self, request):
        """
        download users excel
        """
        file_id = request.GET.get("file_id")
        if not file_id:
            return self.error("Invalid Parameter, file_id is required")
        if not re.match(r"^[a-zA-Z0-9]+$", file_id):
            return self.error("Illegal file_id")
        file_path = TMP_PATH + f"{file_id}.xlsx"
        if not os.path.isfile(file_path):
            return self.error("File does not exist")
        with open(file_path, "rb") as f:
            raw_data = f.read()
        os.remove(file_path)
        response = HttpResponse(raw_data)
        response["Content-Disposition"] = "attachment; filename=users.xlsx"
        response["Content-Type"] = "application/xlsx"
        return response

    @validate_serializer(GenerateUserSerializer)
    @super_admin_required
    def post(self, request):
        """
        Generate User
        """
        data = request.data
        number_max_length = max(len(str(data["number_from"])), len(str(data["number_to"])))
        if number_max_length + len(data["prefix"]) + len(data["suffix"]) > 32:
            return self.error("Username should not more than 32 characters")
        if data["number_from"] > data["number_to"]:
            return self.error("Start number must be lower than end number")

        file_id = rand_str(8)
        filename = TMP_PATH + f"{file_id}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column("A:B", 20)
        worksheet.write("A1", "Username")
        worksheet.write("B1", "Password")
        i = 1

        user_list = []
        for number in range(data["number_from"], data["number_to"] + 1):
            raw_password = rand_str(data["password_length"])
            user = User(username=f"{data['prefix']}{number}{data['suffix']}", password=make_password(raw_password))
            user.raw_password = raw_password
            user_list.append(user)

        try:
            with transaction.atomic():

                ret = User.objects.bulk_create(user_list)
                UserProfile.objects.bulk_create([UserProfile(user=user) for user in ret])
                for item in user_list:
                    worksheet.write_string(i, 0, item.username)
                    worksheet.write_string(i, 1, item.raw_password)
                    i += 1
                workbook.close()
                return self.success({"file_id": file_id})
        except IntegrityError as e:
            # Extract detail from exception message
            #    duplicate key value violates unique constraint "user_username_key"
            #    DETAIL:  Key (username)=(root11) already exists.
            return self.error(str(e).split("\n")[1])


class ClueAPI(APIView):
    @validate_serializer(ClueSerializer)
    def post(self, request):
        """
        add a clue
        """
        data = request.data
        if Clue.objects.filter(phone=data['phone']).exists():
            return self.error("The phone number already exists")
        clue = Clue.objects.create(student_name=data['student_name'], phone=data['phone'])
        fields = ['phone_owner', 'gender', 'age', 'spare_phone_owner', 'spare_phone', 'avatar', 'address', 'intention_level', 'remark', 'xiaoe_phone']
        for field in fields:
            if field in data:
                setattr(clue, field, data[field])
        if data['follow_up']:
            clue.follow_up = User.objects.get(id=data['follow_up'])
            clue.follow_status = FollowStatus.TO_BE_FOLLOWED
        else:
            clue.follow_status = FollowStatus.UNALLOCATED
        clue.student_status = StudentStatus.POTENTIAL_STUDENT
        if User.objects.filter(phone=data['phone']).exists():
            clue.oj_account = User.objects.get(phone=data['phone'])
        else:
            clue.oj_account = User.objects.create(username=data['phone'], password=make_password(data['phone']))
        clue.oj_account.admin_type = AdminType.STUDENT
        clue.oj_account.problem_permission = Permission.NONE
        clue.oj_account.contest_permission = Permission.NONE
        clue.oj_account.save()
        clue.create_time = now()
        clue.save()
        return self.success(ClueSerializer(clue).data)

    @super_admin_required
    def get(self, request):
        """
        get clues
        """
        data = request.GET
        if data.get('id'):
            clues = Clue.objects.filter(id=data.get('id'))
            if not clues.exists():
                return self.error("Clue does not exist")
            return self.success(ClueSerializer(clues[0]).data)
        clues = Clue.objects.all().order_by('-create_time')
        if data.get('student_name'):
            clues = clues.filter(student_name__contains=data.get('student_name'))
        if data.get('phone'):
            clues = clues.filter(phone__contains=data.get('phone'))
        if data.get('follow_status'):
            clues = clues.filter(follow_status=data.get('follow_status'))
        if data.get('address'):
            clues = clues.filter(address__contains=data.get('address'))
        if data.get('intention_level'):
            clues = clues.filter(intention_level=data.get('intention_level'))
        if data.get('follow_up'):
            clues = clues.filter(follow_up_id=data.get('follow_up'))
        return self.success(self.paginate_data(request, clues, ClueSerializer))

    @validate_serializer(ClueSerializer)
    def put(self, request):
        data = request.data
        if not Clue.objects.filter(id=data['id']).exists():
            return self.error("Clue does not exist")
        clue = Clue.objects.get(id=data['id'])
        if data['phone'] and data['phone'] != clue.phone and Clue.objects.filter(phone=data['phone']).exists():
            return self.error("The phone number already exists")
        if data['follow_up'] and data['follow_up'] != clue.follow_up_id:
            if not User.objects.filter(id=data['follow_up']).exists():
                return self.error("The follow up does not exist")
            clue.follow_up = User.objects.get(id=data['follow_up'])
            clue.follow_status = FollowStatus.TO_BE_FOLLOWED
        else:
            clue.follow_up = None
            clue.follow_status = FollowStatus.UNALLOCATED
        data.pop('follow_up')
        if data['oj_account']:
            data.pop('oj_account')
        for key, value in data.items():
            setattr(clue, key, value)
        clue.save()
        return self.success(ClueSerializer(clue).data)
"""This File will contain all the Response and Controller Code"""
import pandas as pd
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, RedirectView, View
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
# from .csv_worker import get_analysis
from django.core.files import File
from .helper import *
from .models import *


class LogIn(TemplateView):
    """User Login view"""
    template_name = "login.html"

    def post(self, request):
        """get request data for the login"""
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        email = email.strip()
        password = password.strip()
        # authenticate user in the Databse
        user = authenticate(username=email, password=password)
        # if credentials are not matched than redirect to login page
        if user is None:
            messages.add_message(request, messages.ERROR, "Invalid username/password")
            return render(request, "login.html")
        # if all good then render index.html page
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "Login successfull")
        return redirect("/")


class LogOut(RedirectView):
    """Logout View"""
    url = "/login/"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOut, self).get(request, *args, **kwargs)


class AnalysisPage(TemplateView):
    """Analysis Page for CSV"""
    template_name = "analysis.html"

    def dispatch(self, request, *args, **kwargs):
        ip_address = request.META.get("REMOTE_ADDR")
        if not self.request.user.is_authenticated:
            # if user is not authenticated then authenticate with ip address
            user = authenticate(username=ip_address, password=None)
            if user is None:
                # if no user found then redirect to the login page
                return redirect("Sentiment:login")
            # login user
            login(self.request, user)
        return super(AnalysisPage, self).dispatch(request, *args, **kwargs)


class HomePage(TemplateView):
    """Home page Dashboard for User"""
    template_name = "index1.html"

    def dispatch(self, request, *args, **kwargs):
        ip_address = request.META.get("REMOTE_ADDR")
        if not self.request.user.is_authenticated:
            # if user is not authenticated then authenticate with ip address
            user = authenticate(username=ip_address, password=None)
            if user is None:
                # if no user found then redirect to the login page
                return redirect("Sentiment:login")
            # login user
            login(self.request, user)
        return render(request, "index1.html", context={
            'table_content': Document.objects.exclude(document_analyzed="").order_by('-uploaded_at')})
        # return super(HomePage, self).dispatch(request, *args, **kwargs)


def analysis(request):
    """
    Get Result of Uploaded CSV
    """
    if request.method == 'POST' and request.FILES['file']:  # Test is containts files and Method is Post

        # Block to check is it contains file
        try:
            csv_file_data = request.FILES['file']
        except:
            return JsonResponse({'status': 400, 'msg': 'No File Found '})

        # Create Model Object of Document
        document_model = Document()
        file_name = csv_file_data.name
        # print(file_name)

        # save uploaded PDF
        document_model.save_uploaded_doc(csv_file_data)

        # Check is uploaded file CSV
        try:
            # print(document_model.document_uploaded.path)
            df = pd.read_csv(document_model.document_uploaded.path, error_bad_lines=False)
        except Exception as e:
            document_model.delete()
            # print(e)
            return JsonResponse({'status': 400, 'msg': 'Uploaded File is not CSV '})

        # Check is Uploaded File contains text
        try:
            text_Column = df['text']
        except:
            document_model.delete()
            return JsonResponse({'status': 400, 'msg': 'Uploaded CSV must need a field named as "text"'})
        try:
            data_analysis = get_analysis(df)

            # Save Analysed File
            new_file = file_name
            data_analysis.to_csv(new_file, index=False)
            with open(new_file) as f:
                document_model.document_analyzed.save(new_file, File(f))
            delete_file(new_file)

            # Pass Path of Analysis file
            object_id = document_model.id
            context = {'loaded_data': data_analysis.to_json(), 'file_id': object_id,
                       "name": document_model.document_analyzed.name.split("/")[-1]}
            return JsonResponse({'csv_id': document_model.id, 'status': 200, 'context': context})
        except Exception as e:
            print(e)
            document_model.delete()
            return JsonResponse({'status': 400, 'msg': 'Internal Server Error Contact Admin '})
        finally:
            delete_file(file_name)
    else:
        return JsonResponse({'status': 400, 'msg': 'No File Uploaded '})


class CSV_API(APIView):
    """
    Get result of CSV File From an API call
    Postman collection: https://www.getpostman.com/collections/9bf76896d023f39b242a
    Post API Documentation: https://documenter.getpostman.com/view/8895684/TzRX9RR1
    """
    parser_class = (FileUploadParser,)

    def __init__(self):
        self.labels = ["positive score", "negative score", "neutral score", "sentiment result", "entity result",
                       "adjective result"]

    def post(self, request, *args, **kwargs):
        """
        Get Result of CSV API
        file : xxxx.csv
        rows : 1-50
        label : sentiment score
        Response
        ----------------
        data : {row1: 0.0076, row2: 0.0076, ...}
        """
        if request.method == 'POST' and request.FILES['file']:  # Test is containts files and Method is Post
            try:
                # Block to check is it contains file
                try:
                    csv_file_data = request.FILES['file']
                except:
                    return JsonResponse({'status': 400, 'msg': 'No File Found '})

                # Block to check file is CSV
                try:
                    df = pd.read_csv(csv_file_data)
                except:
                    return JsonResponse({'status': 400, 'msg': 'Uploaded File is not CSV '})

                # Check is Uploaded File contains colum named as "text"
                try:
                    text_Column = df['text']
                except:
                    return JsonResponse({'status': 400, 'msg': 'Uploaded CSV must need a field named as "text"'})

                # Extract Start Index and check it is integer
                try:
                    start_index = int(request.POST["rows"].split("-")[0]) - 1
                except:
                    return JsonResponse({'status': 400,
                                         'msg': 'Start Index is not Integer or not in format of 1-50(start_index-end_index)'})

                # Extract End Index and check it is integer
                try:
                    end_index = int(request.POST["rows"].split("-")[1])
                except:
                    return JsonResponse({'status': 400,
                                         'msg': 'End Index is not Integer or not in format of 1-50(start_index-end_index)'})

                try:
                    print(start_index, end_index)
                    length = len(text_Column)
                    if not start_index >= 0 and end_index >= 0:
                        return JsonResponse({'status': 400,
                                             'msg': 'Start Index and End Index must be between 1 and' + str(
                                                 length - 1) + ' or not in format of 1-50(start_index-end_index)'})
                    elif start_index >= end_index:
                        return JsonResponse({'status': 400,
                                             'msg': 'Start Index must be less then End Index'})
                    elif start_index > length or end_index > length:
                        return JsonResponse({'status': 400,
                                             'msg': 'Start Index and End Index must be between 1 and' + str(
                                                 length - 1) + ' or not in format of 1-50(start_index-end_index)'})
                except:
                    return JsonResponse({'status': 400,
                                         'msg': 'Start Index and End Index must not be empty and "rows" must be in format of 1-50(start_index-end_index)'})
                current_label = ""
                try:
                    if request.POST["label"].lower() in self.labels:
                        current_label = request.POST["label"].lower()
                    else:
                        return JsonResponse({'status': 400, 'msg': 'label must be inside ' + str(self.labels)})
                except:
                    return JsonResponse({'status': 400, 'msg': 'label must be inside ' + str(self.labels)})

                text_Column = text_Column[start_index:end_index]
                data_analysis = get_analysis_api(text_Column, current_label.lower())

                data = convert_to_dict(data_analysis, start_index, end_index)
                return JsonResponse({'data': data, 'status': 200, 'msg': "Success"})

            except Exception as e:
                print(e)
                return JsonResponse({'status': 400, 'msg': 'Internal Server Error Contact Admin '})
        else:
            return JsonResponse({'status': 400, 'msg': 'No File Uploaded '})


def download(request):
    """
    Download file from given request which contains "public_file_id"
    """
    if request.method == 'POST':
        if request.POST["public_file_id"]:
            this_id = request.POST["public_file_id"]
            print(this_id)
            obj = Document.objects.get(id=this_id)
            return JsonResponse({"name": str(obj.document_analyzed.name.split("/")[-1])})

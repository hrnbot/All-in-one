from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import Video
# Importing all necessary libraries
import cv2
import os


def index(request):
    return render(request, 'index.html')


def uploading(request):
    if request.method == 'POST':
        if len(request.FILES) > 0:
            uploaded_file = request.FILES['video']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            reg = Video(video_file=uploaded_file)
            reg.save()
            return render(request, 'positive_response.html')
        else:
            return render(request, 'negative_response.html')


'''
- Open the video file
- Capture the first frame
- save to local 
- save to DB (optional)
- Distroy the file
'''

# to get frames from video
def video_frame(request):
    # Read the video from specified path
    # cam = cv2.VideoCapture("C:\\Users\\Admin\\PycharmProjects\\project_1\\openCV.mp4")
    # cam = cv2.VideoCapture("E:\Pycharm_project\video_project\upload_video\high4_0_00035_20210803-152146_7.mp4")
    if request.method == 'POST':
        if len(request.FILES) > 0:
            uploaded_file = request.FILES['video']
            print(uploaded_file)
            try:
                # creating a folder named data
                if not os.path.exists('data'):
                    os.makedirs('data')

            # if not created then raise error
            except OSError:
                print('Error: Creating directory of data')

            # frame
            currentframe = 0

            while (True):
                # reading from frame
                frame = uploaded_file.read()

                if frame:
                    # if video is still left continue creating images
                    name = './data/frame' + str(currentframe) + '.jpg'
                    print('Creating...' + name)

                    # writing the extracted images
                    print(name)
                    # cv2.imwrite(name, frame[-1])
                    print(currentframe)
                    # increasing counter so that it will
                    # show how many frames are created
                    currentframe += 1
                else:
                    break

            # Release all space and windows once done
        # uploaded_file.release()
        # cv2.destroyAllWindows()

        return render(request, 'video_frame.html')

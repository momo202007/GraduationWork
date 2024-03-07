from django.shortcuts import render
import datetime,os
from . import models
from . import forms
# import boto3
from datetime import datetime as dt
# comprehend = boto3.client('comprehend')
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)

d = now.strftime('%Y%m%d')
d2 = now.strftime('%Y年%m月%d日')
calendar_params = {'year_month':'','day':'','text':'','date':'','now_month':1,}

def top(request):

    # comprehend = boto3.client('comprehend', 'us-east-1')
    # print(comprehend.detect_dominant_language(Text="aaaaa"))

    # sessionがなければ作成
    if not 'userID' in request.session:
        request.session['userID'] = ''
    if request.method == 'POST':

        if "login" in request.POST:
            uid = request.POST['user_id_textbox']
            u_pass = request.POST['user_pw_textbox']
            request.session['now_month'+request.session['userID']] = 1
            if models.PatientUsers.objects.filter(pk=uid,patient_password=u_pass,is_delete=False).exists():
                col = models.PatientUsers.objects.get(pk = uid)
                request.session['userID'] = col.__str__()
                # 送る画像の指定
                user_training = models.Training.objects.get(patient_id=request.session['userID'])
                img_pass = {'training_img':'images/training/'+ user_training.training_id + '_' + str(user_training.training_stage) + '.png','happyday':next_happyday(request)}
                return render(request, next_top(request),img_pass)
            elif models.SupporterUsers.objects.filter(pk=uid,supporter_password=u_pass,is_delete=False).exists():
                col = models.SupporterUsers.objects.get(pk = uid)
                request.session['userID'] = col.__str__()
                return render(request, next_top(request),{'ID':request.session['userID']})
            else:
                messages.success(request, "test")
                return HttpResponseRedirect('allauth/login/')

        elif 'first_password_set' in request.POST:
            uid = request.POST['first_pw_id_textbox']
            u_pass = request.POST['first_pw_textbox']
            check_pass = request.POST['first_pw_check_textbox']
            if models.PatientUsers.objects.filter(pk=uid).exists():
                if u_pass == check_pass:
                    product = models.PatientUsers.objects.get(pk=uid) # 条件を設定してから
                    product.patient_password = u_pass          # 書き換えて
                    product.save()              # 保存
                    request.session['userID']=uid
                    params = {'images':[],}
                    # trainingのファイル名一覧取得
                    files = os.listdir(path="static/images/training")
                    for img in files:
                        if img[-5:-4] == '4':
                            params['images'].append([img[:-6],'images/training/'+img])
                    return render(request, 'training/training_select.html',params)
                else:
                    messages.success(request, "test")
                    return HttpResponseRedirect('allauth/first_password_set/')
            else:
                messages.success(request, "test")
                return HttpResponseRedirect('allauth/first_password_set/')

        elif 'reset_pass' in request.POST:
            u_pass = request.POST['Pw_reset_textbox']
            check_pass= request.POST['Pw_reset_check_textbox']
            if u_pass == check_pass:
                if list(request.session['userID'])[0]=='k':
                    product = models.PatientUsers.objects.get(pk=request.session['userID']) # 条件を設定してから
                    product.patient_password = u_pass          # 書き換えて
                    product.save()              # 保存
                    return render(request,'allauth/login.html',{'form':forms.LoginForm})
                else:
                    product = models.SupporterUsers.objects.get(pk=request.session['userID']) # 条件を設定してから
                    product.supporter_password = u_pass         # 書き換えて
                    product.save()              # 保存
                    return render(request,next_top(request),{'ID':request.session['userID']})
        elif 'training_view' in request.POST:
            training_img = request.POST['training_view']
            messages.success(request, training_img)
            return HttpResponseRedirect('collection_list')
        elif 'training' in request.POST:
            training_img = request.POST['training']
            if not models.Training.objects.filter(patient_id=request.session['userID']).exists():
                models.Training.objects.create(patient_id=request.session['userID'],collection_id_list=[],training_id=training_img,training_stage=1)
            else:
                training = models.Training.objects.get(patient_id=request.session['userID'])
                training.training_id = training_img
                training.training_stage=1
                training.save()
            # 送る画像の指定
            user_training = models.Training.objects.get(patient_id=request.session['userID'])
            img_pass = {'training_img':'images/training/'+ user_training.training_id + '_' + str(user_training.training_stage) + '.png','happyday':next_happyday(request)}
            return render(request, next_top(request),img_pass)
        elif 'ToDO_done' in request.POST:
            reference_list = request.POST.getlist("done")
            original = models.Todo.objects.filter(patient_id=request.session['userID'],todo_deletion = False)
            for i in reference_list:
                # 成果に登録
                ref_todo = original.get(pk=i)
                ref_todo.todo_references = True
                today=datetime.date.today()
                ref_todo.achievement_list.append(today.__str__())
                ref_todo.save()
                # sessionがなければ作成
                if not 'last_rehab_day'+request.session['userID'] in request.session:
                    request.session['last_rehab_day'+request.session['userID']] = ''
                # 最後にtodoを完了した日が今日でなければ、育成
                # if request.session['last_rehab_day'+request.session['userID']] != today.__str__():
                if True:
                    request.session['last_rehab_day'+request.session['userID']] = today.__str__()
                    training_data = models.Training.objects.get(pk=request.session['userID'])
                    training_data.training_stage+=1
                    # 成長が終わった場合の処理
                    if training_data.training_stage>=4:
                        params = {'images':[]}
                        messages.success(request, 'images/training/'+training_data.training_id+'_4.png')
                        training_data.collection_id_list.append(training_data.training_id)
                        training_data.save()
                        trainings = training_data.collection_id_list
                        # trainingのファイル名一覧取得
                        files = os.listdir(path="static/images/training")
                        for img in files:
                            if img[-5:-4] == '4' and not img[:-6] in trainings:
                                params['images'].append([img[:-6],'images/training/'+img])
                        return render(request,'training/training_select.html',params)
                    training_data.save()
        else:
            return render(request,'allauth/login.html',{'form':forms.LoginForm})
    if request.session['userID'] == '':
        return render(request, 'allauth/login.html',{'form':forms.LoginForm})
    if list(request.session['userID'])[0]=='s':
        return render(request, next_top(request),{'ID':request.session['userID']})
    # 送る画像の指定
    user_training = models.Training.objects.get(patient_id=request.session['userID'])
    img_pass = {'training_img':'images/training/'+ user_training.training_id + '_' + str(user_training.training_stage) + '.png','happyday':next_happyday(request)}
    return render(request, next_top(request),img_pass)

def next_happyday(request):
    # 次のハッピーデーを検索
    happy_days = models.Calender.objects.filter(patient_id = request.session['userID']).order_by("-calendar_date")
    today=datetime.date.today()
    back_day=datetime.date(1000, 1, 1)
    for day in happy_days:
        if day.calendar_date >= today:
            back_day = day.calendar_date
        else:
            break
    if today == back_day:
        val = '今日はハッピーデーです！'
    elif back_day<today:
        val = 'カレンダーからハッピーデーを登録出来ます！'
    else:
        happyday = back_day-today
        val = 'あと'+str(happyday.days)+'日でハッピーデーです！'
    return val

def supporter_top(request):
    context = {
                    'k':"",
                    's':"",
                    }


    if request.method == "POST":
        if "signup" in request.POST:
            if not 'back_date' in request.session:
                request.session['back_date'] = datetime.datetime.now().__str__()
                test = request.session['back_date'][:19]
                test2 = (test.replace('-', '/'))
                global date_value
                date_value = dt.strptime(test2, '%Y/%m/%d %H:%M:%S')
            if date_value>=datetime.datetime.now():
                return HttpResponse('<script>history.back();</script>')
 
  
            if request.POST['pw_textbox'] == request.POST['pw_check_textbox']:
                # ID作成
                last_id = models.PatientUsers.objects.order_by("patient_id").last()
                val = last_id.__str__()
                t_delta = datetime.timedelta(hours=9)
                JST = datetime.timezone(t_delta, 'JST')
                now = datetime.datetime.now(JST)
                d = now.strftime('%Y%m%d')
                if val.startswith('k'+d[2:]):
                    val = list(val)
                    val[0] = '1'
                    val = list(str(int(''.join(val))+1))
                    val[0] = 'k'
                    new_patient_id = ''.join(val) 
                else:
                    new_patient_id = 'k' + d[2:] + '000'
                    val=list(new_patient_id)
                    context["k"]="患者様のID："+new_patient_id
                    
                val[0] = 's'
                new_supporter_id = ''.join(val)
                context["k"]="患者様のID："+new_patient_id
                context["s"]="あなたのID："+new_supporter_id
                # ここまで

                # 登録用データのセット
                new_patient_birthday = request.POST['birth_date']
                new_patient_symptoms = request.POST['symptoms']
                new_supporter_email = request.POST['email_box']
                new_gender = request.POST['gender']
                new_supporter_password = request.POST['pw_textbox']
                if request.POST['relation']=='家族':
                    new_connections = True
                else:
                    new_connections = False

                # 患者登録
                models.PatientUsers.objects.create(patient_id = new_patient_id ,patient_password = '',patient_birthday = new_patient_birthday,patient_symptoms = new_patient_symptoms,patient_completed = False,gender = new_gender)
                # 外部キーを使用するため新しく登録下データを取り出し。
                new_patient_id = models.PatientUsers.objects.get(patient_id = new_patient_id)
                # サポーター登録
                models.SupporterUsers.objects.create(supporter_id = new_supporter_id,supporter_password = new_supporter_password,patient_id = new_patient_id ,connections = new_connections ,supporter_email = new_supporter_email)
                messages.success(request, context['k'])
                messages.success(request, context['s'])
                return HttpResponseRedirect("allauth/signup")
            else:
                val = {'e':'同じパスワードを入力してください','form':forms.Sign_upForm}
                return render(request,'allauth/signup.html',val)
        elif "test" in request.POST:
            request.session['back_date'] = str(datetime.datetime.now() + datetime.timedelta(seconds=100))
            sup_id = request.POST['hidden_data'][7:]
            request.session['userID']=sup_id
            return render(request, next_top(request),{'ID':request.session['userID']})
        elif "rehab_complete" in request.POST:
            p_id = models.SupporterUsers.objects.get(pk=request.session['userID']).patient_id
            p_data = models.PatientUsers.objects.get(pk=p_id)
            p_data.patient_completed = True
            p_data.save()

    return render(request,next_top(request),{'ID':request.session['userID']})


# allauth
def login(request):
    if request.method == "POST":
        if "logout" in request.POST:
            request.session['userID']=''
            list(messages.get_messages(request))
        elif "withdrawal" in request.POST:
            product = models.SupporterUsers.objects.get(pk=request.session['userID']) # 条件を設定してから
            product.is_delete = True          # 書き換えて
            product.save()                    # 更新

            uid = list(request.session['userID'])
            uid[0]='k'
            product = models.PatientUsers.objects.get(pk=''.join(uid)) # 条件を設定してから
            product.is_delete = True          # 書き換えて
            product.save()                    # 更新
            request.session['userID']=''
    # 全てのセッションをリセット
    request.session['last_rehab_day'+request.session['userID']] = ''
    request.session['now_month'+request.session['userID']] = 1
    request.session['userID'] = ''

    return render(request, 'allauth/login.html', {'form':forms.LoginForm})

def signup(request):
    params = {'form':forms.Sign_upForm}

    return render(request, 'allauth/signup.html',params)

def first_password_set(request):
    params = {'form':forms.First_pw_settingForm}
    return render(request, 'allauth/first_password_set.html',params)

def password_reset(request):
    params = {'form':forms.Pw_resetForm}
    return render(request, 'allauth/password_reset.html',params)

def withdrawal(request):
    return render(request, 'allauth/withdrawal.html')

# diary
def diary_menu(request):
    return render(request, 'diary/diary_menu.html')

def diary_post(request):
    diary_list = models.Diary.objects.filter(patient_id=request.session['userID'])
    form = forms.Diary_newpostForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # create()の場合
        d_text=request.POST['diary_inputbox']

        uid = models.PatientUsers.objects.get(patient_id=request.session['userID'])
        if 'diary_image' in request.FILES:
            d_image=request.FILES['diary_image']
            models.Diary.objects.create(patient_id=uid,diary_date=d,diary_text=d_text,diary_images=d_image)
        else:
            models.Diary.objects.create(patient_id=uid,diary_date=d,diary_text=d_text,diary_images="")
        return HttpResponseRedirect("../list")
    context = {
        'diary_list':diary_list,
        'form':form,
        'date':d2,
    }
    return render(request, 'diary/diary_post.html', context)

def diary_list(request):
    if list(request.session['userID'])[0]=="s":
        u_or_sid = request.session['userID'][0]
        uid = list(request.session['userID'])
        uid[0]='k'
        uid = ''.join(uid)
    else :
        uid=request.session['userID']
        u_or_sid = request.session['userID'][0]

    diary_list = models.Diary.objects.filter(patient_id=uid).order_by('diary_id')
    form = forms.Diary_newpostForm(request.POST or None)
    context = {
        'diary_list':diary_list,
        'form':form,
        'date':d2,
        'ID':u_or_sid,
    }
    if request.method == 'POST':
        global diary_id
        diary_id = request.POST['diary_id']
        context = {
        'diary_list':diary_list,
        'form':form,
    }
        return HttpResponseRedirect("../reference")
    return render(request, 'diary/diary_list.html',context)

def diary_reference(request):
    if list(request.session['userID'])[0]=="s":
        u_or_sid = request.session['userID'][0]
        uid = list(request.session['userID'])
        uid[0]='k'
        uid = ''.join(uid)
    else :
        uid=request.session['userID']
        u_or_sid = request.session['userID'][0]
 
    diary_list = models.Diary.objects.filter(diary_id=diary_id).values()
    form = forms.Diary_newpostForm(request.POST or None)
    context = {
        'diary_list':diary_list,
        'form':form,
        'date':d2,
        'ID':u_or_sid,
        'image':diary_list[0]['diary_images'],
    }
    if request.method == 'POST':
        if "edit" in request.POST:
            return HttpResponseRedirect("../editing")
        elif "delete" in request.POST:
            result = models.Diary.objects.get(diary_id=diary_id)
            result.delete()
            return HttpResponseRedirect("../list")
    return render(request, 'diary/diary_reference.html',context)

def diary_editing(request):
    diary_list = models.Diary.objects.filter(diary_id=diary_id)
    form = forms.Diary_newpostForm(request.POST or None)
    context = {
        'diary_list':diary_list,
        'form':form,
        'date':d2,
    }
    if request.method == 'POST':
        return _extracted_from_diary_editing(request)
    return render(request, 'diary/diary_editing.html',context)

def _extracted_from_diary_editing(request):
    diary_edit = request.POST['editing_diary']
    result = models.Diary.objects.get(diary_id=diary_id)
    result.diary_text = diary_edit
    result.save()
    return HttpResponseRedirect("../list")



# SNS
def sns_menu(request):
    return render(request, 'sns/sns_menu.html')
def sns_post(request):
    return render(request, 'sns/sns_post.html', {'form':forms.Sns_postForm})
def timeline(request):
    if request.method == "POST":
        # stampのファイル名一覧取得
        files = os.listdir(path="static/images/stamp")
        # 押されたボタンと一致するスタンプを検索
        for file in files:
            if 'images/stamp/'+file in request.POST:
                # postに値を入れて更新
                post = models.Post.objects.get(pk=request.POST['images/stamp/'+file])
                post.stamp_id_list.append(file[:-4])          # 書き換えて
                post.save()                      # 更新
                messages.success(request, "stamp")
                return HttpResponse('<script>history.back();</script>')
    params={'posts':[],'stamps':[]}
    symptom = models.PatientUsers.objects.get(pk=request.session['userID']).patient_symptoms
    one_symptom_ids = models.PatientUsers.objects.filter(patient_symptoms=symptom).all()
    one_symptom_posts = []
    for id in one_symptom_ids:
        if id.__str__() != request.session['userID']:
            one_user_posts = models.Post.objects.filter(patient_id=id).values()
            for post in one_user_posts:
                one_symptom_posts.append(post)
    sorted_posts = sorted(one_symptom_posts, key=lambda x: x['post_date'].__str__())
    for post in sorted_posts:
        params['posts'].append([post['post_text'],post['post_date'],post['post_id']])
    # 使えるスタンプの一覧作成
    stamps = models.StampInformation.objects.all().values()
    for stamp in stamps:
        params['stamps'].append(stamp['stamp_pass'])
    return render(request, 'sns/timeline.html',params)
def sns_reference(request):
    if request.method == "POST":
        if 'sns_post' in request.POST:
            uid = models.PatientUsers.objects.get(patient_id=request.session['userID'])
            today=datetime.datetime.now().date()
            models.Post.objects.create(stamp_id_list=[],patient_id=uid,post_text=request.POST['sns_inputbox'],post_date=today)
            return HttpResponseRedirect('#')
        elif 'delete' in request.POST:
            sns_id = request.POST['delete']
            messages.success(request, sns_id)
            return HttpResponse('<script>history.back();</script>')
        elif 'sns_del' in request.POST:
            models.Post.objects.filter(pk=request.POST['sns_id_del']).delete()
            messages.success(request, "delete")
            return HttpResponse('<script>history.back();</script>')
            
    params = {
        'posts':[],
    }
    user_posts = models.Post.objects.filter(patient_id=request.session['userID']).all()
    for post in user_posts:
        stamp_list = []
        stamp_const=0
        two_stamps=[]
        for id in post.stamp_id_list:
            stamps = models.StampInformation.objects.get(pk=id)
            if stamp_const<2:
                two_stamps.append(stamps.stamp_pass)
                stamp_const+=1
            else:
                stamp_list.append(two_stamps)
                stamp_const=1
                two_stamps=[stamps.stamp_pass]
        if two_stamps!=[]:
            stamp_list.append(two_stamps)
        params['posts'].append([post.post_id,stamp_list,post.post_text,post.post_date])
    return render(request, 'sns/sns_reference.html',params)
# カレンダー
def calendar(request):
    # POST時の処理
    if request.method == "POST":
        if 'register' in request.POST:
            new_patient_id = models.PatientUsers.objects.get(patient_id = request.session['userID'])
            models.Calender.objects.create(patient_id=new_patient_id,calendar_date=request.session['day'],calendar_text=request.POST['calendar_inputbox'])
        elif 'happy_del' in request.POST:
            new_patient_id = models.PatientUsers.objects.get(patient_id = request.session['userID'])
            models.Calender.objects.filter(patient_id=new_patient_id,calendar_date=request.session['day']).delete()
        elif 'month_ago' in request.POST:
            request.session['now_month'+request.session['userID']]-=1
        elif 'month_next' in request.POST:
            request.session['now_month'+request.session['userID']]+=1
    # カレンダー画面に送るparams
    params = {
        'days':[],
        'year_month':'',
        'happy_days':[],
        'print_year_month':'',
        'backimage':'',
    }
    # 年月、日付をparamsに格納
    today = datetime.date.today()
    # sessionがなければ作成
    if not 'now_month'+request.session['userID'] in request.session:
        request.session['now_month'+request.session['userID']] = 1
    end_of_month = today + relativedelta(months=+request.session['now_month'+request.session['userID']],day=1,days=-1)
    end_day = end_of_month.__str__()[-2:]
    year_month=end_of_month.__str__()[:-2]
    params['print_year_month']=year_month[:4]+"年"+year_month[5:-1]+"月"
    params['year_month']=year_month
    params['backimage']=year_month[5:7]
    request.session['year_month']=year_month
    for i in range(1,int(end_day)+1,3):
        if i+1>int(end_day):
            params['days'].append([str(i)])
        elif i+2>int(end_day):
            params['days'].append([str(i),str(i+1)])
        else :
            params['days'].append([str(i),str(i+1),str(i+2)])
    # ここまで
    # ハッピーデーの一覧を取得しparamsに追加
    happy_day = models.Calender.objects.filter(patient_id=request.session['userID'],calendar_date__startswith=request.session['year_month']).values()
    happy_days = []
    for item in happy_day:
        happy_days.append(item['calendar_date'].__str__())
    params['happy_days']=happy_days
    # ここまで
    return render(request, 'calendar/calendar.html',params)
def happy_editing(request):
    params = {
        "form":forms.Happy_editingForm,
        "day":request.session['date']
    }
    params['form']=params['form']({'calendar_editingbox':request.session['text']})
    return render(request, 'calendar/happy_editing.html',params)
def happy_rederence(request):
    if request.method == "POST":
        if 'editing' in request.POST:
            cal_objects = models.Calender.objects.get(patient_id=request.session['userID'],calendar_date=request.session['day']) # 条件を設定してから
            cal_objects.calendar_text = request.POST['calendar_editingbox']        # 書き換えて
            # ...書き換えるカラムは複数でも良い...
            cal_objects.save()
            global params                  # 更新
            params={'calendar_text':request.POST['calendar_editingbox'],'calendar_date':request.session['date']}
            request.session['text'] = cal_objects.calendar_text
            return render(request,'calendar/happy_rederence.html',params)
        else:
            for i in range(1,32):
                # 1日から31日の中で何日が選ばれたかを取得
                if request.session['year_month']+str(i) in request.POST:
                    request.session['day']=request.session['year_month']+str(i)
                    calendar_date = list(request.session['year_month'])
                    calendar_date[4]="年"
                    calendar_date[-1]="月"
                    request.session['date']=''.join(calendar_date)+str(i)+'日'
                    if models.Calender.objects.filter(patient_id=request.session['userID'],calendar_date=request.session['year_month']+str(i)).exists():
                        # ハッピーデーが登録された日付ならば参照画面を表示
                        
                        params=models.Calender.objects.filter(patient_id=request.session['userID'],calendar_date=request.session['year_month']+str(i)).values()[0]
                        params['calendar_date'] = request.session['date']
                        request.session['text'] = params['calendar_text']
                        return render(request, 'calendar/happy_rederence.html',params)
                    else :
                        # 登録されていなければ登録画面を表示
                        return render(request, 'calendar/happy_register.html',{'form':forms.Happy_registrationForm,'day':request.session['date']})
    return render(request, 'calendar/happy_rederence.html',params)

# ToDOメニュー
def ToDO_menu(request):
    return render(request, 'ToDO/ToDO_menu.html')
#ToDOリスト
def ToDO_list(request):
    original = models.Todo.objects.filter(patient_id=request.session['userID'],todo_deletion = False)
    today = datetime.date.today()
    for todo in original:
        if today in todo.achievement_list:
            todo.todo_references = True
            todo.save()
        else:
            todo.todo_references = False
            todo.save()
            #return render(request,'ToDO/ToDO_list.html',{'original':original})
    original = models.Todo.objects.filter(patient_id=request.session['userID'],todo_deletion = False)
    print(original)
    return render(request, 'ToDO/ToDO_list.html', {'original':original})
# ToDO追加
def ToDO_add(request):
    if request.method == "POST":
        if 'todo_add' in request.POST:
            new_patient_id = models.PatientUsers.objects.get(patient_id = request.session['userID'])
            rehab_id = models.RehabMenu.objects.get(pk=9999)
            models.Todo.objects.create(patient_id=new_patient_id,todo_text=request.POST['todo_inputbox'],todo_deletion=False,rehab_id=rehab_id,achievement_list=[])
    return render(request, 'ToDO/ToDO_add.html',{'form':forms.Rehab_todo_addForm,'hoge':'追加項目'})
# ToDO削除
def ToDO_delete(request):
    original = models.Todo.objects.filter(patient_id=request.session['userID'],todo_deletion = False).all()
    context = {'original': original,}
    if request.method == "POST":
        if 'ToDO_del' in request.POST:
            del_list = request.POST.getlist("del")
            for i in del_list:
                del_todo = original.get(pk=i)
                del_todo.todo_deletion = True
                del_todo.save()
            return HttpResponseRedirect('#')
    return render(request, 'ToDO/ToDO_delete.html', context)
# 成果を参照する
def ToDO_reference(request):
    # ログインユーザーの今までのタスク一覧を取得
    # [{todo_id: 1, patient_id: ,todo_text: ,todo_references:, todo_deletion: , rehab_id: , achievement_list: },
    # {todo_id: 1, patient_id: ,todo_text: ,todo_references:, todo_deletion: , rehab_id: , achievement_list: }...]
    user_todo = models.Todo.objects.filter(patient_id=request.session['userID']).values()
    days = []
    todos = []
    print_todo = []
    # 値をひとつずつ取り出し、日付を重複しないように格納
    for one_todo in user_todo:
        # one_todo = { todo_id: 1, patient_id: ,todo_text: ,todo_references:, todo_deletion: , rehab_id: , achievement_list:[] }取り出す
        for day in one_todo['achievement_list']:
            # day = one_todo['achievement_list:[]']リストの要素をひとつずつ取り出す
            if not day in days:
                # daysの中にdayがなければ追加する
                days.append(day)
                # days = ひとつでも達成したタスクがある日付の一覧
    # 達成日、タスク一覧を配列に格納
    for day in days:
        for one_todo in user_todo:
            if day in one_todo['achievement_list']:
                # dayにタスクを達成していれば
                todos.append(one_todo['todo_text'])
                # todosにタスクを追加する
        print_todo.append([day,todos])
        # dayと、dayに達成したタスクの一覧をprint_todoに追加
        todos=[]
    # print_todo = [[日付,[タスク1,タスク2,タスク3]],[日付,[タスク1,タスク2,タスク3]],[日付,[タスク1,タスク2,タスク3]],]
    # ソート(print_todoをdayの降順に並び替える)
    print_todo = sorted(print_todo,reverse=True,key=lambda x:x[0])
    params = {'todos':print_todo}
    return render(request, 'ToDO/ToDO_reference.html', params)
# サポーターToDO
def supporter_ToDO(request):
    if request.method == "POST":
        if 'todo_add' in request.POST:
            new_supporter_id = models.SupporterUsers.objects.filter(supporter_id=request.session['userID'])
            new_patient_id = models.PatientUsers.objects.get(pk=new_supporter_id[0].patient_id)
            rehab_id = models.RehabMenu.objects.get(pk=9999)
            models.Todo.objects.create(patient_id=new_patient_id,todo_text=request.POST['todo_inputbox'],todo_deletion=False,rehab_id=rehab_id,achievement_list=[])
            return HttpResponseRedirect('/supporter/ToDO/')
        elif 'template_ToDO_add' in request.POST:
            todo_ids = request.POST.getlist("todo_id")
            print("\n\n\n\n",todo_ids)
            for id in todo_ids:
                rehab_id = models.RehabMenu.objects.get(pk = id)
                todo_text = rehab_id.rehab_text
                uid = list(request.session['userID'])
                uid[0] = "k"
                uid = ''.join(uid)
                uid = models.PatientUsers.objects.get(pk = uid)
                models.Todo.objects.create(patient_id = uid,todo_text=todo_text,rehab_id = rehab_id,achievement_list = [])
                flag = False
    # S_patient = サポーターIDから患者IDを取り出す,<QuerySet [<SupporterUsers: s000000000>]>
    S_patient = models.SupporterUsers.objects.filter(supporter_id=request.session['userID'])
    # original = 患者ID
    original = models.PatientUsers.objects.get(pk=S_patient[0].patient_id)
    # todo1 = 患者のToDO一覧を取り出す
    todo1 = models.Todo.objects.filter(patient_id=original)
    # RehabMenuを症状別に表示 = [症状,[タスク1,タスク2,タスク3,タスク4,...]]
    # user_template = [{ rehab_id: , rehab_text: , patient_symptoms_list: [] },{ rehab_id: , rehab_text: , patient_symptoms_list: [] },...]
    user_template = models.RehabMenu.objects.values()
    # patient = サポーターIDを取り出す,<QuerySet [<SupporterUsers: s000000000>]>
    patient = models.SupporterUsers.objects.filter(supporter_id=request.session['userID'])
    # user_symptoms = ユーザーの症状を取り出す
    user_symptoms = models.PatientUsers.objects.get(pk=patient[0].patient_id).patient_symptoms
    # 症状,タスク
    symptoms = {"user_symptoms":user_symptoms,"templates":""}    # 症状毎のタスク一覧
    templates = []
    rehab_ids = []
    for id in todo1:
        rehab_ids.append(id.rehab_id.__str__())
    for one_template in user_template:
        # one_template = { rehab_id: , rehab_text: , patient_symptoms_list: [] }取り出す
        if user_symptoms in one_template['patient_symptoms_list']:
        # one_template['patient_symptoms_list:[]']リストの要素をひとつずつ取り出す
            if not str(one_template['rehab_id']) in rehab_ids:
                # templateの中にuser_symptomsがあれば追加する
                templates.append([one_template['rehab_text'],one_template['rehab_id']])
                # templates = 症状に該当するタスクの一覧
    # symptomsにタスク一覧を追加
    symptoms["templates"] = templates
    context = {'symptoms': symptoms, 'todo1': todo1,'form':forms.Rehab_todo_addForm,}
    return render(request, 'ToDO/sp_ToDO.html',context)


def collection_list(request):
    imgs = {'imgs':[]}
    user_training = models.Training.objects.get(pk=request.session['userID'])
    imgs['imgs'].append([user_training.training_id,'images/training/'+ user_training.training_id + '_' + str(user_training.training_stage) + '.png'])
    for img in user_training.collection_id_list:
        imgs['imgs'].append([img,'images/training/'+ img + '_4.png'])
    return render(request,'training/collection_list.html',imgs)


# 正直使ってない
def happy_register(request):
    return render(request, 'calendar/happy_register.html',{"form":forms.Happy_registrationForm})


# #育成機能
def training_select(request):
    if request.method == 'POST':
        # 送る画像の指定
        user_training = models.Training.objects.get(patient_id=request.session['userID'])
        img_pass = {'training_img':'images/training/'+ user_training.training_id + '_' + str(user_training.training_stage) + '.png','happyday':next_happyday(request)}
        return render(request, next_top(request),img_pass)
    return render(request, 'training/training_select.html')

#リハビリ完了top
def rehab_complete_top(request):
    # if request.method == 'POST':
    #     return render(request, 'top.html')
    return render(request, 'rehab_complete_top.html')

def rehab_complete(request):
    return render(request, 'allauth/rehab_complete.html')

def info_confirmation(request):
    if request.method == "POST":
        if 'info_change' in request.POST:
            # サポーターデータ更新
            sp_data = models.SupporterUsers.objects.get(pk=request.session['userID'])
            if request.POST['relation'] == '家族':
                sp_data.connections = True
            else:
                sp_data.connections = False            # 患者データ更新            
            p_pk = 'k'+request.session['userID'][1:]
            p_data = models.PatientUsers.objects.get(pk=p_pk)
            p_data.patient_birthday = request.POST['birth_date']
            p_data.gender = request.POST['gender']
            p_data.patient_symptoms = request.POST['symptoms']
            sp_data.save()
            p_data.save()
    info = {}
    sp_info = models.SupporterUsers.objects.get(pk=request.session['userID'])
    info['sp_id'] = sp_info.supporter_id    
    if sp_info.connections:
        info['connections'] = '家族'    
    else :
        info['connections'] = '病院関係者'    
    p_info = models.PatientUsers.objects.get(pk=sp_info.patient_id)
    info['p_id'] = p_info.patient_id    
    info['birth'] = p_info.patient_birthday    
    info['gender'] = p_info.gender    
    info['symptoms'] = p_info.patient_symptoms    
    return render(request,'allauth/info_confirmation.html',info)
def info_change(request):
    info = {}
    sp_info = models.SupporterUsers.objects.get(pk=request.session['userID'])
    if sp_info.connections:
        info['connections'] = '家族'    
    else :
        info['connections'] = '病院関係者'    
    p_info = models.PatientUsers.objects.get(pk=sp_info.patient_id)
    info['birth'] = forms.Sign_upForm({'birth_date':p_info.patient_birthday})
    info['gender'] = p_info.gender    
    info['symptoms'] = p_info.patient_symptoms    
    return render(request,'allauth/info_change.html',info)

# def sns_test(request):
#     # if request.method == 'POST':
#     #     return render(request, 'top.html') 
#     return render(request, 'sns/test.html')
def next_top(request):
    if request.session['userID'][0] == 's':     
        next_html = 'sp_top.html'
        p_id = models.SupporterUsers.objects.get(pk=request.session['userID']).patient_id       
        if models.PatientUsers.objects.get(pk=p_id).patient_completed:
            next_html = 'supporter_rehab_complete_top.html'   
    else:
            next_html = 'top.html'    
            if models.PatientUsers.objects.get(pk=request.session['userID']).patient_completed:
                next_html = 'rehab_complete_top.html'    
    return next_html
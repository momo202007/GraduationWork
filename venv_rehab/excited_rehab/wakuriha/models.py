# from accounts.models import CustomUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
class PatientUsers(models.Model):
    """患者ユーザーモデル"""
    patient_id = models.CharField(verbose_name = '患者ID', primary_key=True, max_length=10)
    patient_password = models.TextField(verbose_name = 'パスワード', max_length=10)
    patient_birthday = models.DateField(verbose_name = '生年月日')
    patient_symptoms = models.CharField(verbose_name = '症状別分類', max_length=20)
    patient_completed = models.BooleanField(verbose_name = 'リハビリ有無', default=False)
    is_delete = models.BooleanField(verbose_name = '退会フラグ', default=False)
    gender = models.CharField(verbose_name = '性別' ,max_length=10)

    # データをわかりやすく説明するデータ（付帯情報）
    class Meta:
        # 管理画面でのモデルの名前を指定
        verbose_name_plural = 'PatientUser'

    # 管理画面でのモデル内のタイトルフィールド
    def __str__(self):
        return self.patient_id


class SupporterUsers(models.Model):
    """サポートユーザーモデル"""
    supporter_id = models.CharField(verbose_name = 'サポーターID', primary_key=True, max_length=10)
    supporter_password = models.CharField(verbose_name = 'パスワード', max_length=10)
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', db_column='patient_id', on_delete=models.PROTECT)
    connections = models.BooleanField(verbose_name = '患者との関係性', null=True)
    supporter_email = models.EmailField(verbose_name = 'メールアドレス')
    is_delete = models.BooleanField(verbose_name = '退会フラグ', default=False)
    diary_mail = models.BooleanField(verbose_name = '日記メールフラグ', default=True)
    class Meta:
        verbose_name_plural = 'SupporterUser'

    def __str__(self):
        return self.supporter_id


class Diary(models.Model):
    """日記モデル"""
    diary_id = models.AutoField(verbose_name = '日記ID', primary_key=True)
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', db_column='patient_id', on_delete=models.PROTECT)
    diary_date = models.DateTimeField(verbose_name = '年月日', auto_now_add=True)
    diary_text = models.TextField(verbose_name = '日記内容文', max_length=1000)
    diary_images = models.ImageField(verbose_name = '日記画像パス')
    class Meta:
        verbose_name_plural = 'Diary'

    def __str__(self):
        return str(self.diary_id)


class Experience(models.Model):
    """経験談モデル"""
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', primary_key=True, db_column='patient_id', on_delete=models.PROTECT)
    experience_text = models.TextField(verbose_name = '経験談', max_length=2000)
    experience_date = models.DateTimeField(verbose_name = '年月日', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Experience'

    def __str__(self):
        return str(self.patient_id)



class Calender(models.Model):
    """カレンダーモデル"""
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', db_column='patient_id', on_delete=models.PROTECT)
    calendar_date = models.DateField(verbose_name = '年月日')
    calendar_text = models.TextField(verbose_name = '', max_length=300)
    # ユニーク制約
    class Meta:
        # 複合キー
        constraints = [
            models.UniqueConstraint(fields=['patient_id', 'calendar_date'], name='unique_calendar')
        ]
        verbose_name_plural = 'Calender'
    def __str__(self):
        return str(self.patient_id)


class Training(models.Model):
    """育成機能モデル"""
    patient_id = models.TextField(verbose_name = '患者ID', primary_key=True)
    collection_id_list = ArrayField(models.TextField(verbose_name = 'コレクション名一覧', null=True))
    training_id = models.TextField(verbose_name = '育成中コレクション名')
    training_stage = models.IntegerField(verbose_name = '育成段階') # 1から4の値の予定
    class Meta:
        verbose_name_plural = 'Training'
    def __str__(self):
        return self.patient_id

class CollectionInformation(models.Model):
    """育成コレクションモデル"""
    collection_id = models.AutoField(verbose_name = 'コレクションID', primary_key=True)
    training_image_list = ArrayField(models.ImageField(verbose_name = '画像パス一覧', upload_to='', null=True))

    class Meta:
        verbose_name_plural = 'CollectionInformation'

    def __str__(self):
        return self.collection_id


class Post(models.Model):
    """タイムラインモデル"""
    post_id = models.AutoField(verbose_name = '投稿ID', primary_key=True)
    stamp_id_list = ArrayField(models.IntegerField(verbose_name = 'スタンプID一覧'))
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', db_column='patient_id', on_delete=models.PROTECT)
    post_text = models.TextField(verbose_name = '投稿内容', max_length=300)
    post_date = models.DateField(verbose_name = '年月日')

    class Meta:
        verbose_name_plural = 'Post'

    def __str__(self):
        return str(self.post_id)


class StampInformation(models.Model):
    """スタンプモデル"""
    stamp_id = models.AutoField(verbose_name = 'スタンプID', primary_key=True)
    stamp_pass = models.TextField(verbose_name = 'スタンプ画像パス')

    class Meta:
        verbose_name_plural = 'StampInformation'

    def __str__(self):
        return str(self.stamp_id)


class SnsGroup(models.Model):
    """SNSグループモデル"""
    group_id = models.IntegerField(verbose_name = 'グループID', primary_key=True)
    post_id_list = models.IntegerField(verbose_name = '投稿ID一覧')
    patient_id_list = models.CharField(verbose_name = '患者ID一覧', max_length=10)

    class Meta:
        verbose_name_plural = 'SnsGroup'

    def __str__(self):
        return self.group_id


class RehabMenu(models.Model):
    """テンプレートtodo"""
    rehab_id = models.IntegerField(verbose_name = 'リハビリID', primary_key=True)
    rehab_text = models.TextField(verbose_name = 'タスク内容テキスト', max_length=100)
    patient_symptoms_list = ArrayField(models.CharField(verbose_name = '症状別分類ID一覧', max_length=20))

    class Meta:
        verbose_name_plural = 'RehabMenu'

    def __str__(self):
        return self.rehab_text


class Todo(models.Model):
    """リハビリtodoモデル"""
    todo_id = models.AutoField(verbose_name = 'リハビリtodoID', primary_key=True)
    patient_id = models.ForeignKey(PatientUsers, verbose_name = '患者ID', db_column='patient_id', on_delete=models.PROTECT)
    todo_text = models.TextField(verbose_name = 'その他用タスクテキスト', max_length=100, null=True)
    todo_deletion = models.BooleanField(verbose_name = '削除フラグ', default=False)
    todo_references = models.BooleanField(verbose_name = '完了フラグ', default=False)
    rehab_id = models.ForeignKey(RehabMenu, verbose_name = 'リハビリID', db_column='rehab_id', on_delete=models.PROTECT)
    achievement_list = ArrayField(models.DateField(verbose_name = '達成日一覧', null=True))

    class Meta:
        verbose_name_plural = 'Todo'

    def __str__(self):
        return str(self.todo_id)
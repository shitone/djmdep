from django.db import models

# Create your models here.


class AwsArrival(models.Model):
    data_day = models.DateField(primary_key=True)
    station_number = models.CharField(max_length=6, primary_key=True)
    a00 = models.IntegerField()
    a01 = models.IntegerField()
    a02 = models.IntegerField()
    a03 = models.IntegerField()
    a04 = models.IntegerField()
    a05 = models.IntegerField()
    a06 = models.IntegerField()
    a07 = models.IntegerField()
    a08 = models.IntegerField()
    a09 = models.IntegerField()
    a10 = models.IntegerField()
    a11 = models.IntegerField()
    a12 = models.IntegerField()
    a13 = models.IntegerField()
    a14 = models.IntegerField()
    a15 = models.IntegerField()
    a16 = models.IntegerField()
    a17 = models.IntegerField()
    a18 = models.IntegerField()
    a19 = models.IntegerField()
    a20 = models.IntegerField()
    a21 = models.IntegerField()
    a22 = models.IntegerField()
    a23 = models.IntegerField()
    p00 = models.IntegerField()
    p01 = models.IntegerField()
    p02 = models.IntegerField()
    p03 = models.IntegerField()
    p04 = models.IntegerField()
    p05 = models.IntegerField()
    p06 = models.IntegerField()
    p07 = models.IntegerField()
    p08 = models.IntegerField()
    p09 = models.IntegerField()
    p10 = models.IntegerField()
    p11 = models.IntegerField()
    p12 = models.IntegerField()
    p13 = models.IntegerField()
    p14 = models.IntegerField()
    p15 = models.IntegerField()
    p16 = models.IntegerField()
    p17 = models.IntegerField()
    p18 = models.IntegerField()
    p19 = models.IntegerField()
    p20 = models.IntegerField()
    p21 = models.IntegerField()
    p22 = models.IntegerField()
    p23 = models.IntegerField()

    class Meta:
        db_table = "aws_arrival"

    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        cts_array = []
        pqc_array = []
        for i in range(24):
            s = "%02d" % i
            a = self.__dict__['a'+s]
            p = self.__dict__['p'+s]
            if a == None:
                cts_array.append(0)
            else:
                cts_array.append(int(a))
            if p == None:
                pqc_array.append(0)
            else:
                pqc_array.append(int(p))
        return cts_array, pqc_array
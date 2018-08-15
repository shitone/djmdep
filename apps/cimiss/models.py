from django.db import models

# Create your models here.


class AwsArrival(models.Model):
    id = models.AutoField(primary_key=True)
    data_day = models.DateField()
    station_number = models.CharField(max_length=6)
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
        unique_together = (("data_day", "station_number"),)

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
            if a is None:
                cts_array.append(0)
            else:
                cts_array.append(int(a))
            if p is None:
                pqc_array.append(0)
            else:
                pqc_array.append(int(p))
        return cts_array, pqc_array


class AwsSource(models.Model):
    station_number = models.CharField(max_length=6, primary_key=True)
    no_center = models.IntegerField()
    last_no_center = models.IntegerField()

    class Meta:
        db_table = "aws_source"


class RegCenterArrival(models.Model):
    id = models.AutoField(primary_key=True)
    data_day = models.DateField()
    station_number = models.CharField(max_length=6)
    c00 = models.IntegerField()
    c01 = models.IntegerField()
    c02 = models.IntegerField()
    c03 = models.IntegerField()
    c04 = models.IntegerField()
    c05 = models.IntegerField()
    c06 = models.IntegerField()
    c07 = models.IntegerField()
    c08 = models.IntegerField()
    c09 = models.IntegerField()
    c10 = models.IntegerField()
    c11 = models.IntegerField()
    c12 = models.IntegerField()
    c13 = models.IntegerField()
    c14 = models.IntegerField()
    c15 = models.IntegerField()
    c16 = models.IntegerField()
    c17 = models.IntegerField()
    c18 = models.IntegerField()
    c19 = models.IntegerField()
    c20 = models.IntegerField()
    c21 = models.IntegerField()
    c22 = models.IntegerField()
    c23 = models.IntegerField()

    class Meta:
        db_table = "reg_center_arrival"
        unique_together = (("data_day", "station_number"),)
    
    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        reg_array = []
        for i in range(24):
            s = "%02d" % i
            c = self.__dict__['c'+s]
            if c is None:
                reg_array.append(0)
            else:
                reg_array.append(int(c))
        return reg_array


class AwsBattery(models.Model):
    id = models.AutoField(primary_key=True)
    data_day = models.DateField()
    station_number = models.CharField(max_length=6)
    b00 = models.FloatField()
    b01 = models.FloatField()
    b02 = models.FloatField()
    b03 = models.FloatField()
    b04 = models.FloatField()
    b05 = models.FloatField()
    b06 = models.FloatField()
    b07 = models.FloatField()
    b08 = models.FloatField()
    b09 = models.FloatField()
    b10 = models.FloatField()
    b11 = models.FloatField()
    b12 = models.FloatField()
    b13 = models.FloatField()
    b14 = models.FloatField()
    b15 = models.FloatField()
    b16 = models.FloatField()
    b17 = models.FloatField()
    b18 = models.FloatField()
    b19 = models.FloatField()
    b20 = models.FloatField()
    b21 = models.FloatField()
    b22 = models.FloatField()
    b23 = models.FloatField()

    class Meta:
        db_table = "aws_battery"
        unique_together = (("data_day", "station_number"),)

    def init_from_dict(self, init_dic):
        for k in init_dic:
            self.__dict__[k] = init_dic[k]

    def get_array(self):
        battery_array = []
        for i in range(24):
            s = "%02d" % i
            b = self.__dict__['b'+s]
            if b is None:
                battery_array.append(0)
            else:
                battery_array.append(int(b))
        return battery_array

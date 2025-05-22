class SD3078:
    #0x32
    def __init__(self,i2c,charge=True,slvAddr=0x32):
        self.i2c=i2c
        self.add=slvAddr
        
        if charge:
            self.enWrite()
            self.writereg(0x18,b'\x82')
            self.dsWrite()
        
    def readregs(self,regAddr,bytenum):#,int,int
        return self.i2c.readfrom_mem(self.add,regAddr,bytenum)

    def writereg(self,regAddr,buff):#,int,bytes
        self.i2c.writeto(self.add,bytes([regAddr])+buff)
        
    def enWrite(self):
        self.i2c.writeto(self.add,bytes([0x10,0x80]))
        self.i2c.writeto(self.add,bytes([0x0F,0x84]))
    
    def dsWrite(self):
        buff=self.readregs(0x0F,2)
        self.i2c.writeto(self.add,bytes([0x0F,buff[0]&0x7B,buff[1]&0x7F]))
        
    def settime(self,year,mon,day,week,hour,minute,sec,tf12or24,amOrpm=0):#00-99,01~12,01~31,0~6,00-23,00-59,00-59,1:24hours format 0:12hours format, 0:am 1:pm
        if (tf12or24==0 and (hour==00 or hour>12)):
            return 0
        buff=bytes([((sec//10)<<4)+(sec%10),((minute//10)<<4)+(minute%10),(tf12or24<<7)+(amOrpm<<5)+((hour//10)<<4)+(hour%10),week&0x07,((day//10)<<4)+(day%10),((mon//10)<<4)+(mon%10),((year//10)<<4)+(year%10)])
        self.writereg(0x00,buff)
    
    def readtime(self):
        tbuff=self.readregs(0x00,7)
        second=((tbuff[0]&0x70)>>4)*10+(tbuff[0]&0x0F)
        minute=((tbuff[1]&0x70)>>4)*10+(tbuff[1]&0x0F)
        tf12or24=True if tbuff[2]&0x80!=0 else False
        amOrpm=0
        if tf12or24:#24 hours format
            hour=((tbuff[2]&0x30)>>4)*10+(tbuff[2]&0x0F)
        else:
            amOrpm=True if tbuff[2]&0x20!=0 else False
            hour=((tbuff[2]&0x10)>>4)*10+(tbuff[2]&0x0F)
        week=tbuff[3]&0x07
        day=((tbuff[4]&0x30)>>4)*10+(tbuff[4]&0x0F)
        mon=((tbuff[5]&0x10)>>4)*10+(tbuff[5]&0x0F)
        year=((tbuff[6]&0xF0)>>4)*10+(tbuff[6]&0x0F)
        return [tf12or24,amOrpm,hour,minute,second,year,mon,day,week]
    
    def readBattVolt(self):
        buff=self.readregs(0x1A,2)
        return (((buff[0]&0x80)<<1)+buff[1])/100
    
    def readTemp(self):
        buff=self.readregs(0x16,1)
        if buff[0]&0x80!=0:
            temp=buff[0]-256
        else:
            temp=buff[0]
        return temp
        
    def switch12or24h(self,tf12or24):#1:24 hours format 0:12 hours format
        hbuff=self.readregs(0x02,1)
        if ((hbuff[0]&0x80)!=0) and (tf12or24==0):#from 24 hours format to 12 hours format
            hour=((hbuff[0]&0x30)>>4)*10+(hbuff[0]&0xF)
            if(hour>11):
                hour=12 if hour==12 else hour-12
                buff=bytes([0x20+((hour//10)<<4)+(hour%10)])
                self.writereg(0x02,buff)
            else:
                hour=12 if hour==0 else hour
                buff=bytes([((hour//10)<<4)+(hour%10)])
                self.writereg(0x02,buff)
        if ((hbuff[0]&0x80)==0) and (tf12or24==1):#from 12 hours format to 24 hours format
            amOrpm=hbuff[0]&0x20
            hour=((hbuff[0]&0x10)>>4)*10+(hbuff[0]&0xF)
            if amOrpm!=0:
                hour=12 if hour==12 else hour+12
                buff=bytes([0x80+((hour//10)<<4)+(hour%10)])
                self.writereg(0x02,buff)
            else:
                hour=0 if hour==12 else hour
                buff=bytes([0x80+((hour//10)<<4)+(hour%10)])
                self.writereg(0x02,buff)
            
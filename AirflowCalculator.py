
class RegelingRecord:
    verschilMin = 0
    verschilMax = 0
    flow1 = 0
    flow2 = 0
    flow3 = 0
    flow4 = 0
    flow5 = 0
    flow6 = 0

    def __init__(self, verschilMin, verschilMax, flow1, flow2, flow3, flow4, flow5, flow6):
        self.verschilMin = verschilMin
        self.verschilMax = verschilMax
        self.flow1 = flow1
        self.flow2 = flow2
        self.flow3 = flow3
        self.flow4 = flow4
        self.flow5 = flow5
        self.flow6 = flow6



class AirflowCalculator():
    KOUDER5 = -20
    KOUDER4 = -10
    KOUDER3 = -4
    KOUDER2 = -2
    KOUDER1 = -1
    ZELFDE = 0
    WARMER1 = 1
    WARMER2 = 2
    WARMER3 = 4
    WARMER4 = 10
    WARMER5 = 20

    MIN_AIRFLOW = 0
    MAX_AIRFLOW = 100


    regelingen = [
        RegelingRecord(-999,-20, WARMER5,WARMER2,WARMER2,ZELFDE,KOUDER2,KOUDER2),
        RegelingRecord(-20,-10,  WARMER3,WARMER2,WARMER2,ZELFDE,KOUDER2,KOUDER3),
        RegelingRecord(-10,-5,   WARMER3,WARMER2,WARMER2,ZELFDE,KOUDER3,KOUDER4),
        RegelingRecord(-5,0,     WARMER2,WARMER2,WARMER1,ZELFDE, KOUDER3,KOUDER4),
        RegelingRecord(0,5,      WARMER2,WARMER1,ZELFDE,KOUDER2, KOUDER4,KOUDER4),
        RegelingRecord(5,10,     WARMER3,WARMER1,ZELFDE,KOUDER4,KOUDER5,KOUDER5),
        RegelingRecord(10,20,    ZELFDE,ZELFDE,KOUDER3,KOUDER4,KOUDER5,KOUDER5),
        RegelingRecord(20,999,   KOUDER4,KOUDER4,KOUDER4,KOUDER4,KOUDER4,KOUDER4)
    ]

    def __init__(self):
        pass

    def calcAirflow(self, bbqTempSet, currentTemp, lastTemp, currentAirflow):
        if(currentTemp is None or lastTemp is None):
            return 0

        tempVerschil = currentTemp - bbqTempSet
        tempStijging = currentTemp - lastTemp
        regelingRecord = self.findRecord(tempVerschil)
        if tempStijging<-1.5:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow1)
        if tempStijging>=-1.5 and tempStijging<-0.7:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow2)
        if tempStijging>=-0.7 and tempStijging<0:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow3)
        if tempStijging>=0 and tempStijging<0.7:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow4)
        if tempStijging>=0.7 and tempStijging<1.5:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow5)
        if tempStijging>=1.5:
            return self.calcFlow(currentAirflow,tempVerschil, regelingRecord.flow6)

    def calcFlow(self, currentAirflow, tempVerschil, addedFlow):
        newFlow = int(currentAirflow+addedFlow)
        if (newFlow>self.MAX_AIRFLOW):
            newFlow = self.MAX_AIRFLOW
        if (newFlow<self.MIN_AIRFLOW):
            newFlow = self.MIN_AIRFLOW
        return int(newFlow)


    def findRecord(self, tempVerschil):
        for record in self.regelingen:
            if (tempVerschil>=record.verschilMin and tempVerschil<=record.verschilMax):
                return record
        return RegelingRecord(111111,111111,self.ZELFDE,self.ZELFDE,self.ZELFDE,self.ZELFDE,self.ZELFDE)

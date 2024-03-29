def CREATEXLSFROMPDF(path):
    
    import PyPDF2
    import pandas as pd
    from PyPDF2 import PdfFileReader
    def FindAllRawTextfromPDF(PdfPath):
        A=''
        pdf= PyPDF2.PdfFileReader(open(PdfPath, "rb"))
        for page in pdf.pages:
            A += page.extractText()
        return A

    D1=FindAllRawTextfromPDF(path).split("\n")

    EnrollmentNumbers=[]
    EnrollmentNumbersIndexes=[]
    for i in range(len(D1)):
        if(len(D1[i])==11):
            if(D1[i].isdigit()):
    #             print(D1[i])
                EnrollmentNumbersIndexes.append(i)
                EnrollmentNumbers.append(D1[i])
    def CollectFirstSemesterSubjestData(D):
        Ans=[]
        i1=0
        i2=EnrollmentNumbersIndexes[0]
    #     print(i1,i2)
        while(i1<i2):
            Ans.append(D[i1])
            i1 += 1
        return Ans

    def FindSemesterNumberformFirstRow(L):
        SemNumber=0
        for i in range(len(L)):
            if(L[i].find('SEMESTER')>-1):
                L2=L[i].split(" ")
                if(len(L2)>1):
    #                 print(L2)
                    for o in range(len(L2)):
                        if(L2[o].find('SEMESTER')>-1):
                            if(o>0):
    #                             print(L2[o],o)
                                SemNumber=L2[o-1]
                                break
            if(L[i].find('Sem./Year:')>-1):
                L3=L[i].split(" ")
                if(len(L3)>1 and (i<len(L3)-1)):
    #                 print(L3)
                    for e in range(len(L3)):
                        if(L3[e].find('Sem./Year:')>-1):
                            if(e>0):
    #                             print(L3[e],e)
                                SemNumber=L3[e+1]
                                break
        return SemNumber

    Lfirst=CollectFirstSemesterSubjestData(D1)
    ALLLforALLSubjectID=[]
    ALLLforALLSubjectID.append(Lfirst)
    SemsL=[]
    FirstStudentRowSemesterNumber=FindSemesterNumberformFirstRow(Lfirst)
    SemsL.append(FirstStudentRowSemesterNumber)
    def fetchRaw(i1,i2):
        L=[]
        while(i1<i2):
            L.append(D1[i1])
            i1 +=1
        return L

    LL=[]
    for i in range(len(EnrollmentNumbersIndexes)-1):
        LL.append(fetchRaw(EnrollmentNumbersIndexes[i],EnrollmentNumbersIndexes[i+1]))
    LastIndexforLastEnroll=len(D1)-1
    FirstIndexforLastEnroll=EnrollmentNumbersIndexes[len(EnrollmentNumbersIndexes)-1]
    LastStudentList=[]
    while(FirstIndexforLastEnroll<LastIndexforLastEnroll):
        LastStudentList.append(D1[FirstIndexforLastEnroll])
        FirstIndexforLastEnroll += 1
    LL.append(LastStudentList)
    # len(ALLLforALLSubjectID) 
    def FindALLHigherList(L):
        Ans=[]
        for i in range(len(L)):
            if(len(L[i])>200):
                Ans.append(L[i])
        return Ans
    def FindALLHigherListIndexes(L):
        Ans=[]
        for i in range(len(L)):
            if(len(L[i])>200):
                Ans.append(i)
        return Ans
    LLLL= FindALLHigherList(LL)
    for i in range(len(LLLL)):
         ALLLforALLSubjectID.append(LLLL[i])
    DeclaredDateofPDF =''
    Examinationstatus=''
    def FindDeclaredDate(L):
        ans=''
        for i in range(len(L)):
            if(L[i].find('RTSID:')>-1):
    #             print(L[i])
                ans=L[i][7:15]
    #             print(i)
                break;
        return ans
    def FindExaminationStatus(L):
        ans=''
        for i in range(len(L)):
            if(L[i].find('Examination:')>-1):
                NL=L[i].split(' ')
                for j in range(len(NL)):
                    if(NL[j].find('Examination:')>-1):
                        ans=NL[j+1]
                        break
        return ans
    DeclaredDateofPDF=FindDeclaredDate(ALLLforALLSubjectID[0])
    Examinationstatus=FindExaminationStatus(ALLLforALLSubjectID[0])
    def FillLforICPC(L,i1,i2):
        ans=[]
        while(i1<i2):
            ans.append(L[i1])
            i1 = i1+1
        return ans
    def FindIndexofSOESN(L):
        i1=0
        i2=0
        for i in range(len(L)):
            if(L[i].find('(SCHEME OF EXAMINATIONS)')>-1):
    #             print('SOE = ',i, L[i])
                i1=i
                break
        for i in range(len(L)):
            if(L[i].find('S.No.')>-1):
    #             print('S.no = ',i,L[i])
                i2=i
                break
        return i1,i2
    LLforICPC=[]
    for i in ALLLforALLSubjectID:
        L=FindIndexofSOESN(i)
        LLforICPC.append(FillLforICPC(i,L[0],L[-1]))
    def EvaluatePCPN(L):
        PC = ''
        PN = ''
        i1=0
        i2=0
        L1=[]
        L2=[]
        for i in range(len(L)):
            if(L[i].find('Scheme of Programme Code:')>-1 or L[i].find('Programme Code:')>-1):
                L1=L[i].split(' ')
                i1=i
                break
        for i in range(len(L1)):
            if(L1[i].find('Code:')>-1):
                PC =L1[i+1]
                break
        for i in range(len(L1)):
            if(L1[i].find('Name:')>-1):
                for j in L1[i+1:]:
                    PN = PN + j
                break
    #     print('PN = ',PN)
        for i in range(len(L)):
            if(L[i].find('SchemeID:')>-1 or L[i].find('Sem./Year:')>-1):
                L2=L[i].split(' ')
                i2=i
                break
    #     print('L2 = ',L2)
        for i in range(i1+1,i2):
    #         print('L[i]= ',L[i])
            PN = PN + L[i]
    #     print('in L[2]...')
        for i in range(len(L2)):
            if(L2[i].find(')')>-1):
    #             print('L2[i] = ',L2[i])
                PN = PN + L2[i]
                break
    #         print('L2[i] = ',L2[i])
            PN = PN + L2[i]+' '
    #     print('PN = ',PN)
        return PC,PN
    Programme=[]
    for i in LLforICPC:
        L=[]
        ans= EvaluatePCPN(i)
        L.append(ans[0])
        L.append(ans[1])
        Programme.append(L)
    def FindALLDetailsUsingCode(L,code):
        for i in L:
            if(code.find(i[0])>-1):
                return i
    def CreateUniqueElementListforProgram(L):
        output1=[]
        for x in L:
            if x[0] not in output1:
                output1.append(x[0])
        ans=[]
        for i in output1:
            ans.append(FindALLDetailsUsingCode(L,i))    
        return ans
    ProgrammeList1=CreateUniqueElementListforProgram(Programme)
    def CreateActualBranchName(L):
        ans=[]
        ans.append(L[0])
    #     print(L,L[0],L[1])
        branchname=''
        x=0
        for i in range(len(L[1])):
            if(L[1][i].find(')')>-1):
                x=i
                break
        for i in range(0,x+1):
            branchname += L[1][i]
    #     print(branchname)
        ans.append(branchname)
        return ans
    ProgrammeList=[]
    for i in ProgrammeList1:
        ProgrammeList.append(CreateActualBranchName(i))
    def FindALLPeperID(L):
        pid=[]
        pcode=[]
        pname=[]
        Ans=[]
        tp=[]
        for i in range(len(L)):
            if(len(L[i])==5 or len(L[i])==6):
                if(L[i].isdigit()):
                    L1=[]
                    pid.append(L[i])
                    pcode.append(L[i+1])
                    L1.append(L[i])
                    L1.append(L[i+1])
                    if(len(L[i+3])>3):
                        pname.append(L[i+2]+L[i+3])
                        L1.append(L[i+2]+L[i+3])
                        L1.append(L[i+4])
                        L1.append(L[i+5])
                        L1.append(L[i+8])
                    else:
                        pname.append(L[i+2])
                        L1.append(L[i+2])
                        L1.append(L[i+3])
                        L1.append(L[i+4])
                        L1.append(L[i+7])
                    Ans.append(L1)
        return Ans,pid,pname,pcode
    ALLSubjectCodeNameID=list()
    for i in ALLLforALLSubjectID:
        ALLSubjectCodeNameID.append(FindALLPeperID(i)[0])
    PIDSCODE=list()
    for i in ALLSubjectCodeNameID:
        for j in i:
            PIDSCODE.append(j)
    def CreateUniqueElementListforsubject(L):
        output1=[]
        for x in L:
            if x[1] not in output1:
                output1.append(x[1])
        return output1
    output1= CreateUniqueElementListforsubject(PIDSCODE)
    FinalListofCodeIDName1 =[]
    def FindALLDetailsUsingCode(L,code):
        for i in L:
            if(code.find(i[1])>-1):
                return i
    for i in output1:
        FinalListofCodeIDName1.append(FindALLDetailsUsingCode(PIDSCODE,i))
    SubjectList= FinalListofCodeIDName1
    def EvaluateICIN(L):
        IC = ''
        IN = ''
        i1=0
        i2=0
        L1=[]
        L2=[]
        for i in range(len(L)):
            if(L[i].find('Institution Code:')>-1 or L[i].find('Institution:')>-1):
                L1=L[i].split(' ')
                i1=i
                break
        for i in range(len(L1)):
            if(L1[i].find('Code:')>-1):
                IC =L1[i+1]
                break
        for i in range(len(L1)):
            if(L1[i].find('Institution:')>-1):
                for j in L1[i+1:]:
                    IN = IN + j+' '
                break
        IN = IN[:-1]
        for i in range(i1+1,len(L)):
            IN = IN + L[i]

        return IC,IN
    Institute=[]
    for i in LLforICPC:
        L=[]
        ans= EvaluateICIN(i)
        L.append(ans[0])
        L.append(ans[1])
        Institute.append(L) 
    def CreateUniqueElementListforsubject(L):
        output1=[]
        for x in L:
            if x[1] not in output1:
                output1.append(x[1])
        return output1
    output1= CreateUniqueElementListforsubject(Institute)
    FinalListofCodeIDName2 =[]
    def FindALLDetailsUsingCode(L,code):
        for i in L:
            if(code.find(i[1])>-1):
                return i
    for i in output1:
        FinalListofCodeIDName2.append(FindALLDetailsUsingCode(Institute,i))
    InstituteList = FinalListofCodeIDName2
    IndexofStudentsem = FindALLHigherListIndexes(LL)
    def FisrtStudentsIndexes(L):
        Ans=[]
        for i in range(L+1):
            Ans.append(i)
        return Ans
    def BetweenIndexStudent(i1,i2):
        Ans=[]
        for i in range(i1+1,i2+1):
            Ans.append(i)
        return Ans

    def createIndexesofVariousSem(L):
        Ans=[]
        Ans.append(FisrtStudentsIndexes(L[0]))
        if(len(L)>0):
            for i in range(1,len(L)):
                Ans.append(BetweenIndexStudent(L[i-1],L[i]))
        return Ans
    StudentIndexSemVise=[]
    if(len(IndexofStudentsem)>0):
        StudentIndexSemVise=createIndexesofVariousSem(IndexofStudentsem)
        if((len(LL)-IndexofStudentsem[len(IndexofStudentsem)-1])>1):
            StudentIndexSemVise.append(BetweenIndexStudent(IndexofStudentsem[len(IndexofStudentsem)-1],len(LL)-1))
    else:
        StudentIndexSemVise.append(FisrtStudentsIndexes(len(LL)-1))
    NSemIndex=[]
    for i in range(len(ALLLforALLSubjectID)):
    #     print('i = ',i)
        NSemIndex.append(FindSemesterNumberformFirstRow(ALLLforALLSubjectID[i]))
    def RemoveExtraInformation(L):
        A=[]
        i1=0
        i2=0
        for i in range(len(L)):
            if(L[i].find('RESULT TABULATION SHEET')>-1 or L[i].find('RESULT')>-1 or L[i].find('(SCHEME OF EXAMINATIONS)')>-1):
                i2=i
                i1=i
                break
        if(i2>0):
    #         print('Remove Information')
            j=0
            while(j<i2):
                A.append(L[j])
                j += 1

        else:
            A= L
        return A
    AfterRemovedExtraILL=[]
    for i in range(len(LL)):
        AfterRemovedExtraILL.append(RemoveExtraInformation(LL[i]))
    LengthL=list()
    for i in range(len(AfterRemovedExtraILL)):
        LengthL.append(len(AfterRemovedExtraILL[i]))
    #     print(i,len(AfterRemovedExtraILL[i]))
    LengthL.sort()
    from collections import Counter
    c= Counter(LengthL)
    MostCommonL=c.most_common() 
    LowestNumber = LengthL[0]
    HighestNumber= LengthL[len(LengthL)-1]
    MostFreqNumber= MostCommonL[0][0]
    def RemoveSID(s1):
    #     print('sid = ',s1.find('SID:') )
        return s1[s1.index(':',0,len(s1))+2:len(s1)]

    def RemoveSchemaID(s2):
        return s2[s2.index(':',0,len(s2))+2:len(s2)]    
    def RemoveBrakets(S):
        A=[]
        i1 = S.find("(")
        i2 = S.find(")")
        A.append(S[0:i1])
        A.append(S[i1+1:i2])
        return A

    def RemoveSpaces(S):
        if(S.find(" ")<0):
            return S
        else:
            A=[]
            S1=S.split(" ")
            for i in range(len(S1)):
                if(len(S1[i])>0):
                    A.append(S1[i])
            return A
    def CreateEfficientDatafromRawofStudent(L):
        EfL=[]
        EfL.append(L[0])
        EfL.append(L[2])
        if(L[4].find("SID:")>-1):
            EfL.append(RemoveSID(L[4]))
        else:
            EfL.append(L[4])
        if(L[6].find("SchemeID:")>-1):
            EfL.append(RemoveSchemaID(L[6]))
        else:
            EfL.append(L[6])
        for i in range(7,len(L)):
            if(L[i].find('AA')>-1 or L[i].find('DD')>-1 or L[i].find('CC')>-1):
                for i in range(4):
                    EfL.append('A')
                continue
            if(L[i].find('(')>-1):
                if('A' in L[i] or 'D' in L[i] or 'C' in L[i] or 'L' in L[i]):
                    L[i]=L[i][1:]
                BL= RemoveBrakets(L[i])
                for k2 in range(len(BL)):
                    EfL.append(BL[k2])
                continue
            if(L[i].find(' ')>-1):
                SL= RemoveSpaces(L[i])
                for k1 in range(len(SL)):
                    EfL.append(SL[k1])
                continue
        EfL.append('00') 
        return EfL
    LLforDSDB=[]
    for i in range(len(AfterRemovedExtraILL)):
        LLforDSDB.append(CreateEfficientDatafromRawofStudent(AfterRemovedExtraILL[i]))
    def FindTotalSubject(L):
        TotalSIndexes=[]
        for i in range(4,len(L)):
    #         print(i,L[i])
            if(len(L[i])==5 or len(L[i])==6 or len(L[i])==7):
                if(L[i].isdigit()):
    #                 print(i)
                    TotalSIndexes.append(i)
        return TotalSIndexes
    def FillAllIE(L,i1,i2):
        Ans=[]
        diff= i2-i1
    #     print('diff= ',diff)
    #     print('peparid= ',L[i1])
        Ans.append(L[i1])
    #     print('credit = ',L[i1+1])
        Ans.append(L[i1+1])
        if(diff>=5):
            if(L[i1+2].isdigit()):
                Ans.append(L[i1+2])
            else:
                Ans.append('A')
            if(L[i1+3].isdigit()):
                Ans.append(L[i1+3])
            else:
                Ans.append('A')
        else:
    #         print(diff)
            if(diff<3):
                Ans.append('A')
                Ans.append('A')
            if(diff>=4):
                if(L[i1+2].isdigit()):
                    Ans.append(L[i1+2])
                else:
                    Ans.append('A')
                if(L[i1+3].isdigit()):
                    Ans.append(L[i1+3])
                else:
                    Ans.append('A')
        return Ans
    def AddPidIE(L):
        NumberofSubjectL=FindTotalSubject(L)
        TotalSubject= len(NumberofSubjectL)
        ans=[]
        for i in range(len(NumberofSubjectL)-1):
            ans.append(FillAllIE(L,NumberofSubjectL[i],NumberofSubjectL[i+1]))
    #     print('before = ',ans)
        ans.append(FillAllIE(L,NumberofSubjectL[len(NumberofSubjectL)-1],len(L)))
    #     print('after = ',ans)
        return ans
    def ExtractOnlyMainFeatures(L):
        A=[]
        A.append(L[0])
        A.append(L[1])
        A.append(L[2])
        A.append(L[3])
        A.append('00')
        A.append(DeclaredDateofPDF)
        A.append(AddPidIE(L))
        return A
    Final1LL=[]
    for i in range(len(LLforDSDB)):
        Final1LL.append(ExtractOnlyMainFeatures(LLforDSDB[i]))
    def CreateSubjectIDIEStringFinal2(L):
        Ans=[]
    #     print(len(L))
        for i in range(len(L)):
    #         print(L[i][0],L[i][1],L[i][2],L[i][3])
            Ans.append(L[i][0])
            Ans.append(L[i][1])
            Ans.append(L[i][2])
            Ans.append('0')
            Ans.append('0')
            Ans.append('0')
    #         Ans.append('0')
    #         Ans.append('0')        
            Ans.append(L[i][3])
        return Ans
    def CreateFinal2(L):
        LS=[]
        LS.append(L[0])
        LS.append(L[1])
        LS.append(L[2])
        LS.append(L[3])
        LS.append(L[4])
        LS.append(L[5])
        ANSL=(CreateSubjectIDIEStringFinal2(L[6]))
        for i in range(len(ANSL)):
            LS.append(ANSL[i])
        return LS
    Datafram3dL=[]
    for i in range(len(Final1LL)):
        Datafram3dL.append(CreateFinal2(Final1LL[i]))
    def FillSemsterforStudents(L,semnumber,FL):
        for i in range(len(L)):
            FL[L[i]][4]=semnumber

    if(len(NSemIndex)==len(StudentIndexSemVise)):
        for i in range(len(StudentIndexSemVise)):
    #         print(i,len(StudentIndexSemVise[i]))
            FillSemsterforStudents(StudentIndexSemVise[i],NSemIndex[i],Datafram3dL)
    def CreateListforSubject(ML,i1,i2):
        Ans=[]
        while(i1<i2):
            Ans.append(ML[i1])
            i1 += 1
        return Ans

    def CreateCommonInformation(L):
        Ans=[]
        for i in range(6):
            Ans.append(L[i])
        return Ans
    def CreateSubjectRow(L):
        ans=[]
        TotalSubject=int((len(L)-6)/7)
        Indexes=[]
        for i in range(TotalSubject):
            Indexes.append((6)+(7*i))
        Indexes.append(Indexes[-1]+7)
        for i in range(len(Indexes)-1):
            ans.append(CreateListforSubject(L,Indexes[i],Indexes[i+1]))
        return ans
    def CreateAllLabaledData(L):
        ans=[]
        ans.append(CreateCommonInformation(L))
        ans.append(CreateSubjectRow(L))
        return ans
    AfterLabelingCreateL=[]
    for i in range(len(Datafram3dL)):
        AfterLabelingCreateL.append(CreateAllLabaledData(Datafram3dL[i]))
    def EvaluateExactProgrammeName(SL,PL):
        ans=[]
        Nans=[]
        for i in range(len(SL)):
            for j in range(len(PL)):
                an=[]
    #             print(SL[i][0][0][6:9],PL[j][0])
                if(SL[i][0][0][6:9].find(PL[j][0])>-1):
                    an.append(SL[i][0][0][6:9])
                    an.append(PL[j][-1])
                    an.append(SL[i][0][0])
                    ans.append(an)
                    break
        for j in SL:
            for i in ans:
                if(j[0][0][-2:].find(i[-1][-2:])==-1):
                    Nans.append(j[0][0])
                    break
        NewPCPL=[]
        for i in Nans:
            for j in ans:
                NewPCPL1=[]
                if(i[3:6].find(j[-1][3:6])>-1):
    #                 print(i)
                    NewPCPL1.append(i[6:9])
    #                 print(j[1])
                    NewPCPL1.append(j[1])
    #                 print(j[-1])
                    NewPCPL.append(NewPCPL1)
                    break



        return NewPCPL
    LEProgramList=EvaluateExactProgrammeName(AfterLabelingCreateL,ProgrammeList)
    def UpdateProgramList(PL,LEPL):
    #     print(PL)
        for i in LEPL:
            PL.append(i)
        return PL
    NewPL = UpdateProgramList(ProgrammeList,LEProgramList)
    def EvaluateProgrammeInstituteName(x,L):
        ans='LATERAL ENTRY'
        for i in L:
            if(i[0].find(x)>-1):
                ans = i[-1]
                break
        return ans


    def CreateCommonFeatureofStudent(L):
        Batch = '20'+L[0][9:11]
        RollNumber = L[0][0:3]
        InstituteCode = L[0][3:6]
        ProgrammeCode = L[0][6:9]
    #     ResultDeclaredDate=ResultDecared
        ProgrammeName = EvaluateProgrammeInstituteName(ProgrammeCode,NewPL)
        InstituteName = EvaluateProgrammeInstituteName(InstituteCode,InstituteList)
        ans=[]
        for i in L:
            ans.append(i)
        ans.append(Batch)
        ans.append(RollNumber)
        ans.append(Examinationstatus)
        ans.append(InstituteCode)
        ans.append(InstituteName)
        ans.append(ProgrammeCode)
        ans.append(ProgrammeName)
        return ans
    def EvaluateSubjectNameList(x,L):
        ans =[]
        for i in L:
            if(i[0].find(x)>-1):
                ans=i[1:]
        return ans

    def FillSubjectNameCode(L):
        ansSNC = []
        ansSNC = EvaluateSubjectNameList(L[0],SubjectList)
        SubjectName = ''
        SubjectCode = ''
        SubjectType = ''
        SubjectTotalredit=''
        SubjectKind=''
        SubjectName = ansSNC[1]
        SubjectCode = ansSNC[0]
        SubjectTotalredit = ansSNC[2]
        SubjectKind = ansSNC[-1]
        SubjectType = ansSNC[-2]
        ans=[]
        ans.append(L[0])
        ans.append(SubjectCode)
        ans.append(SubjectName)
        ans.append(SubjectType)
        ans.append(SubjectTotalredit)
        ans.append(SubjectKind)
        ans.append(L[1])
        ans.append(L[2])
        ans.append(L[-1])
        return ans

    def CreateCommonFeatureofStudentSubject(L):
        ans=[]
        for i in L:
            ans.append(FillSubjectNameCode(i))
        return ans
    def CreateLLforXLS(L):
        ans1 = CreateCommonFeatureofStudent(L[0])
        ans2 = CreateCommonFeatureofStudentSubject(L[-1])
        ans=[]
        for i in ans1:
            ans.append(i)
        for i in ans2:
            for j in i:
                ans.append(j)
        return ans
    LLforDataFrame =[]
    for i in AfterLabelingCreateL:
        LLforDataFrame.append(CreateLLforXLS(i))
    import pandas as pd
    DataFrameS= pd.DataFrame(LLforDataFrame)
    def CreateSubjectIDIEString(L):
        Ans=[]
    #     print(len(L))
        for i in range(len(L)):
            Ans.append('subjectid'+str(i+1))
            Ans.append('subjectcode'+str(i+1))
            Ans.append('subjectname'+str(i+1))
            Ans.append('subjecttype'+str(i+1))
            Ans.append('subjecttotalcredit'+str(i+1))
            Ans.append('subjectkind'+str(i+1))
            Ans.append('obtainedcredit'+str(i+1))
            Ans.append('internalmark'+str(i+1))
            Ans.append('externalmark'+str(i+1))
        return Ans
    def CreateStringKeys(L):
        LS=[]
        LS=['enrollmentnumber', 'name', 'sid', 'schemaid','semester','declareddate','batch','classrollnumber','examinationtype','institutecode','institutename','programmecode','programmename']
        ANSL=(CreateSubjectIDIEString(L[6]))
        for i in range(len(ANSL)):
            LS.append(ANSL[i])
        return LS
    MaxL=list()
    for i in range(len(Final1LL)):
        MaxL.append(len(Final1LL[i][6]))
    MaxL.sort()
    MAxNumberforKays=MaxL[-1]
    FinalIndexKeys=0
    for i in range(len(Final1LL)):
        if(len(Final1LL[i][6])==MAxNumberforKays):
            FinalIndexKeys=i
            break

    KeysDF=CreateStringKeys(Final1LL[FinalIndexKeys])
    DataFrameS.columns=KeysDF
    S1 = path[79:-4].split(' ')
    ansOutput=''
    for i in S1:
        ansOutput += i
    print('Output file name = ',ansOutput)
    outputPDf = str(ansOutput+''+'.xls')
    outputhpath = '/Users/jatinanand/Documents/projectjatin/jatinproject/ravibasics/static/output/'+outputPDf+''
#     outputhpath=''
    writer = pd.ExcelWriter(outputhpath, engine='xlsxwriter')
    DataFrameS.to_excel(writer)
    writer.save()
    print('end')
    import os
    cwd = os.getcwd()
#     DataFrameS.to_excel('AfterSuggestionRecheck5thSem.xls')
    return outputPDf
            
            
            
    






#     outputPDf = str(path[79:-4]+''+'.xls')
#     outputhpath = '/Users/jatinanand/Documents/projectjatin/jatinproject/ravibasics/static/output/'+outputPDf+''
#     writer = pd.ExcelWriter(outputhpath, engine='xlsxwriter')
#     DataFrameS.to_excel(writer)
#     writer.save()
#     print('end')
#     import os
#     cwd = os.getcwd()
# #     dir_path = os.path.dirname(os.path.realpath(__file__))

#     return cwd+'/'+outputPDf

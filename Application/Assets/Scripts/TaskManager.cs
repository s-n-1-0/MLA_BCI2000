using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
public class TaskManager : MonoBehaviour
{
    public UICanvasController ui;
    [HideInInspector]
    public ArrowController arrow;
    private BVREventController bvr;
    private UnityBCI2000 bci2000;
    public int maxTrainTrialsNum,maxTestTrialsNum;
    public int maxTrialsNum
    {
        get => state.isFeedback ? maxTrainTrialsNum : maxTestTrialsNum;
    }
    public float stimTrainTime,stimTestTime;
    public float stimTime
    {
        get => state.isFeedback ? stimTrainTime : stimTestTime;
    }
    public float[] jitterTimeRange;
    public GameObject buttons;
    public TaskState state { get; private set; }
    private bool isSetConfig = false;
    private void Awake()
    {
        state = new TaskState(GetComponent<UnityBCI2000>());
    }
    private void Start()
    {
        var arrowObj = GameObject.Find("Target");
        var bvrEventController = GameObject.Find("BVREventController").GetComponent<BVREventController>();
        bvr = bvrEventController;
        arrow = arrowObj.GetComponent<ArrowController>();
        arrow.gameObject.SetActive(false);
        bci2000 = GetComponent<UnityBCI2000>();
    }

    private void Update()
    {
        arrow.isArrowLeft = state.trueClassType == TrialClassType.Left;
        if (state.trueClassType != TrialClassType.None && state.predictClassType != TrialClassType.None)
        {
            arrow.isStopedShift = false;  
            arrow.isStripeSameDirectionAsArrow = state.trueClassType == state.predictClassType;
        }
        else
        {
            arrow.isStopedShift = true;
        }
    }

    public void StartTask(bool isNFB) {
        StartCoroutine(_StartTask(isNFB));
    }
    private IEnumerator _StartTask(bool isNFB)
    {
        if (isSetConfig) bci2000.StartBCI2000();
        else bci2000.ResumeBCI2000();
        isSetConfig = true;
        yield return new WaitForSeconds(1);
        buttons.gameObject.SetActive(false);
        state.isFeedback = isNFB;
        ui.SetMaxTrialsNum(maxTrialsNum);
        ui.SetStimTIme(stimTime);
        arrow.SetArrowType(isNFB ? ArrowType.Stripe :  ArrowType.Default);
        //---セットアップ
        var trials = GenerateTrials(maxTrialsNum);
        /*
        int l = 0,r =0;
        foreach(var t in trials)
        {
            if (t == TrialClassType.Left) l++;
            if (t == TrialClassType.Right) r++;
        }
        Debug.Log("合計" + trials.Length.ToString());
        Debug.Log(l);
        Debug.Log(r);
        */
        //---試行
        for (int i = 0; i <  maxTrialsNum; i++)
        {
            ChangeWaitScreen(i + 1);
            yield return new WaitForSeconds((i==0 ? 6f : 0f) + UniformlyRandom());

            bvr.isEvent = true;
            ChangeTargetScreen(trials[i]);
            yield return new WaitForSecondsRealtime(stimTime);
        }
        ChangeWaitScreen(9999);
        buttons.gameObject.SetActive(true);
        bci2000.SuspendBCI2000();
    }
    private void ChangeWaitScreen(int trialNum)
    {
        state.trueClassType = TrialClassType.None;
        state.trialNum = trialNum;
       arrow.gameObject.SetActive(false);
    }
    private void ChangeTargetScreen(TrialClassType nextClass)
    {
        state.trueClassType = nextClass;
        Update();
        arrow.SetEulerAngles();
        arrow.gameObject.SetActive(true); 
    }

    private float UniformlyRandom() => Random.Range(jitterTimeRange[0], jitterTimeRange[1]);

    //TODO: 以下のコード要整理
    private TrialClassType[] GenerateTrials(int count)
    {
        List<TrialClassType> totalList = new List<TrialClassType>();
        while (totalList.Count < count) {
            List<TrialClassType> alternatingList = new List<TrialClassType>();

            for (int i = 0; i < 20; i++) alternatingList.Add(i % 2 == 0 ? TrialClassType.Left : TrialClassType.Right);
            alternatingList = ShuffleList(alternatingList);

            totalList.AddRange(alternatingList);
        }
        totalList = totalList.GetRange(0, count);
        while (checkConsecutiveValues(totalList, 4))
        {
          totalList = sortConsecutiveValues(totalList,4);
            //最初の4つが連続の場合永久ループしかねないので再度生成
            if (totalList.GetRange(0, 4).All(x => x == totalList[0]))
            {
                totalList = GenerateTrials(count).ToList();
            }
        }
        //totalList.ForEach(x => Debug.Log(x));
        return totalList.ToArray();
    }
     List<T> ShuffleList<T>(List<T> list)
    {
        int n = list.Count;
        while (n > 1)
        {
            n--;
            int k = Random.Range(0, n + 1);
            var value = list[k];
            list[k] = list[n];
            list[n] = value;
        }
        return list;
    }
    bool checkConsecutiveValues(List<TrialClassType> list,int max)
    {
        int count = 0;
        TrialClassType prevX = TrialClassType.None;
        foreach(var x in list)
        {
            if (x == prevX)
            {
                count++;
                if(count >= max)
                {
                    //Debug.Log(count);
                    return true;
                }
            }
            else count = 1;
            
            prevX = x;
        }
        return false;
    }

    List<TrialClassType> sortConsecutiveValues(List<TrialClassType> list, int max)
    {
        int count = 0;
        TrialClassType prevX = TrialClassType.None;
        var newList = new List<TrialClassType>();
        foreach (var x in list)
        {
            if (x == prevX)
            {
                count++;
                if (count >= max)
                {
                    count--;
                    newList.Insert(0,x);
                }
                else newList.Add(x);
            }
            else
            {
                newList.Add(x);
                count = 1;
            }
            prevX = x;
        }
        return newList;
    }
}

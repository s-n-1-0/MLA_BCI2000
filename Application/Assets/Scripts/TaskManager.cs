using System.Collections;
using System.Collections.Generic;
using UnityEngine;
public class TaskManager : MonoBehaviour
{
    [HideInInspector]
    public ArrowController arrow;
    private BVREventController bvr;
    public int maxTrialsNum = 30;
    public float[] jitterTimeRange;
    public float stimTime;
    public GameObject buttons;
    public TaskState state { get; } = new TaskState();
    private void Start()
    {
        var arrowObj = GameObject.Find("Target");
        var bvrEventController = GameObject.Find("BVREventController").GetComponent<BVREventController>();
        bvr = bvrEventController;
        arrow = arrowObj.GetComponent<ArrowController>();
        arrow.gameObject.SetActive(false);
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
        buttons.gameObject.SetActive(false);
        state.isNFBMode = isNFB;
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
            yield return new WaitForSeconds((i==0 ? 7f : 0f) + UniformlyRandom());

            bvr.isEvent = true;
            ChangeTargetScreen(trials[i]);
            yield return new WaitForSecondsRealtime(stimTime);
        }
        ChangeWaitScreen(9999);
        buttons.gameObject.SetActive(true);
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

    private TrialClassType[] GenerateTrials(int count)
    {
        List<TrialClassType> totalList = new List<TrialClassType>();
        while (totalList.Count < count) {
            List<TrialClassType> alternatingList = new List<TrialClassType>();

            for (int i = 0; i < 20; i++) alternatingList.Add(i % 2 == 0 ? TrialClassType.Left : TrialClassType.Right);
            alternatingList = ShuffleList(alternatingList);
            totalList.AddRange(alternatingList);
        }
        return totalList.GetRange(0,count).ToArray();
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
}

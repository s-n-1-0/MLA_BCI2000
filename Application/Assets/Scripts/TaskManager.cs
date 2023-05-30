using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TaskManager : MonoBehaviour
{
    public ArrowController arrow;
    public int maxTrialsNum = 30;
    public GameObject buttons;
    public TaskState state { get; } = new TaskState();
    private void Start()
    {
        var arrowObj = GameObject.Find("Target");
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
        var trials = new TrialClassType[maxTrialsNum];
        for (int i = 0; i < maxTrialsNum; i++) trials[i] = (TrialClassType)(1 + Random.Range(0, 2));
       
        //---試行
        for (int i = 0; i <  maxTrialsNum; i++)
        {
            ChangeWaitScreen(i + 1);
            yield return new WaitForSeconds(i==0 ? 10f : 2f);
            
            ChangeTargetScreen(trials[i]);
            yield return new WaitForSecondsRealtime(5f);
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
}

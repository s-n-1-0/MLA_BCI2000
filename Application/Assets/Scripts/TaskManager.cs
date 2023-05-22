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
        if (state.trueClassType != TrialClassType.None)
        {
            arrow.SetArrowType(state.isFeedback && state.predictClassType != TrialClassType.None ? ArrowType.Stripe : ArrowType.Default); //FB有でpredictの結果が返されているなら
            arrow.isArrowLeft = state.trueClassType == TrialClassType.Left;
            arrow.isStripeSameDirectionAsArrow = state.trueClassType == state.predictClassType;
        }
        else
        {
            arrow.SetArrowType(ArrowType.Default);
        }
    }

    public void StartTask(bool isNFB) {
        StartCoroutine(_StartTask(isNFB));
    }
    private IEnumerator _StartTask(bool isNFB)
    {
        buttons.gameObject.SetActive(false);
        state.isNFBMode = isNFB;
        //---セットアップ
        var trials = new TrialClassType[maxTrialsNum];
        for (int i = 0; i < maxTrialsNum; i++) trials[i] = (TrialClassType)(1 + Random.Range(0, 2));
       
        //---試行
        for (int i = 0; i <  maxTrialsNum; i++)
        {
            ChangeWaitScreen(i + 1);
            yield return new WaitForSeconds(1f);
            
            ChangeTargetScreen(trials[i]);
            yield return new WaitForSecondsRealtime(3f);
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
        arrow.SetEulerAngles();
        arrow.gameObject.SetActive(true); 
    }
}

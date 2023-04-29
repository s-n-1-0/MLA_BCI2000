using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Demo4PatternsManager : MonoBehaviour
{
    public ArrowController arrow;
    private void Start()
    {
        var arrowObj = GameObject.Find("Target");
        arrow = arrowObj.GetComponent<ArrowController>();
        arrow.gameObject.SetActive(false);
        StartTask();
    }

    public void StartTask()
    {
        StartCoroutine(_StartTask());
    }
    private IEnumerator _StartTask()
    {
        //---セットアップ
        var trials = new TrialClassType[] { TrialClassType.Right,TrialClassType.Right,TrialClassType.Left,TrialClassType.Left};
        var predicts = new TrialClassType[] { TrialClassType.Right,TrialClassType.Left,TrialClassType.Right,TrialClassType.Left };
        arrow.SetArrowType(ArrowType.Stripe);
        //---試行
        for (int i = 0; i < trials.Length; i++)
        {
            ChangeWaitScreen();
            yield return new WaitForSeconds(1f);
            ChangeTargetScreen(trials[i], predicts[i]);
            yield return new WaitForSecondsRealtime(5f);
        }
        ChangeWaitScreen();
    }
    private void ChangeWaitScreen()
    {
        arrow.gameObject.SetActive(false);
    }
    private void ChangeTargetScreen(TrialClassType trueType,TrialClassType predictType)
    {
        arrow.isArrowLeft = trueType == TrialClassType.Left;
        arrow.isStripeSameDirectionAsArrow = trueType == predictType;
        arrow.gameObject.SetActive(true);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DemoAppManager : MonoBehaviour
{
    private ArrowController arrow;
    public int trialsNum = 30;
    public TaskState state { get; } = new TaskState();
    private void Start()
    {
        var arrowObj = GameObject.Find("Target");
        arrow = arrowObj.GetComponent<ArrowController>();
        arrow.gameObject.SetActive(false);
        StartTask();
    }

    private void Update()
    {
        if (state.trueClassType != TrialClassType.None)
        {
            arrow.SetArrowType(ArrowType.Stripe); //FB有でpredictの結果が返されているなら
            arrow.isArrowLeft = state.trueClassType == TrialClassType.Left;
            arrow.isStripeSameDirectionAsArrow = state.trueClassType == state.predictClassType;
        }
    }

    public void StartTask()
    {
        StartCoroutine(_StartTask());
    }
    private IEnumerator _StartTask()
    {
        //---試行
        while (true)
        {
            state.trueClassType = TrialClassType.None;
            ChangeWaitScreen();
            yield return new WaitForSeconds(1f);
            var trueClass = (TrialClassType)(1 + Random.Range(0, 2));
            state.trueClassType = trueClass;
            ChangeTargetScreen();
            yield return new WaitForSecondsRealtime(5f);

        }
    }
    private void ChangeWaitScreen()
    {
        arrow.gameObject.SetActive(false);
    }
    private void ChangeTargetScreen()
    {
        Update();
        arrow.gameObject.SetActive(true);
    }
}

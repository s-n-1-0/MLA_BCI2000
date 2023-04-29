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
            arrow.SetArrowType(state.isFeedback && state.predictClassType != TrialClassType.None ? ArrowType.Stripe : ArrowType.Default); //FB有でpredictの結果が返されているなら
            arrow.isArrowLeft = state.trueClassType == TrialClassType.Left;
            arrow.isStripeSameDirectionAsArrow = state.trueClassType == state.predictClassType;
        }
        else
        {
            arrow.SetArrowType(ArrowType.Default);
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
            var trueClass = (TrialClassType)(1 + Random.Range(0, 2));
            ChangeWaitScreen();
            yield return new WaitForSeconds(1f);
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
        arrow.gameObject.SetActive(true);
    }
}

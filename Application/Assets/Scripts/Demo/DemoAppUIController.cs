using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DemoAppUIController : MonoBehaviour
{
    private TaskState state;
    void Start()
    {
        state = gameObject.GetComponent<DemoAppManager>().state;
    }

    public void ChangeTargetDirection(bool isLeft)
    {
        state.predictClassType = isLeft ? TrialClassType.Left : TrialClassType.Right;
    }
}

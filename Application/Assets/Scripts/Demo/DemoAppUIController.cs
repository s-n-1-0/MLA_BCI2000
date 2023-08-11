using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DemoAppUIController : MonoBehaviour
{
    private DummyTaskState state;
    void Start()
    {
        state = gameObject.GetComponent<DemoAppManager>().state as DummyTaskState;
    }

    public void ChangeTargetDirection(bool isLeft)
    {
        state._predictClassType = isLeft ? TrialClassType.Left : TrialClassType.Right;
    }
}

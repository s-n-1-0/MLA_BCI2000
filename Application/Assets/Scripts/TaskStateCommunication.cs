using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using static CustomVariableBase;

public class TaskStateCommunication : CustomVariableBase
{
    public override void AddCustomVariables()
    {
        var state = Sender?.BCIObject?.GetComponent<TaskManager>()?.state;
        if (state == null) return;
        //--SEND
        customVariables.Add(new CustomSendVariable(
            "feedback",
            new Func<float>(() => state.isFeedback ? 1 : 0),
            1,
            UnityBCI2000.StateType.UnsignedInt16
        ));
        customVariables.Add(new CustomSendVariable(
            "trueClass",
            new Func<float>(() => (int)state.trueClassType),
            1,
            UnityBCI2000.StateType.UnsignedInt16
        ));
        return;
        //--GET
        customVariables.Add(new CustomGetVariable(
            "predictClass",
            new Action<int>((int i) => { state.predictClassType = (TrialClassType)i; })
        ));
    }
}

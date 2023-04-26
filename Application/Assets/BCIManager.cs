using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BCIManager : CustomVariableBase
{
    public override void AddCustomVariables()
    {
        var state = GetComponent<TaskManager>().state;
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

        //--GET
        customVariables.Add(new CustomGetVariable(
            "predictClass",
            new Action<int>((int i) => { state.predictClassType = (TrialClassType)i; })
        ));
    }
}

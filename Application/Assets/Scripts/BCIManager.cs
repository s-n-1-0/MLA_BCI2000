using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class BCIManager : CustomVariableBase
{
    private void Awake()
    {
        string filePath = Application.streamingAssetsPath + "/BCISettings.json";
        StreamReader reader = new StreamReader(filePath);
        string json = reader.ReadToEnd();
        reader.Close();
        var bciSettings = JsonUtility.FromJson<BCI2000SettingsJson>(json);
        var bci = GetComponent<UnityBCI2000>();
        bci.OperatorPath = bciSettings.operatorPath;
        bci.Module1 = bciSettings.module1Name;
        bci.Module2 = bciSettings.module2Name;
        bci.Module3 = bciSettings.module3Name;
        bci.enabled = true;
    }
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

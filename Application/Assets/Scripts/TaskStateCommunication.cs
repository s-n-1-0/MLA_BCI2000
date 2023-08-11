using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;


//TODO: àÍâûìÆçÏÇ∑ÇÈÇÊÇ§Ç…ÇµÇΩÇØÇ«ÇªÇ‡ÇªÇ‡Ç¢ÇÁÇ»Ç≠Ç»Ç¡ÇΩÅB
public class TaskStateCommunication : MonoBehaviour
{
    Dictionary<string, CustomSetVariable> setValues = new Dictionary<string, CustomSetVariable>();

    private void Awake()
    {
        var bci2000 = GetComponent<UnityBCI2000>();
        var state = GetComponent<TaskManager>().state;
        //--SEND
        setValues.Add("feedback",new CustomSetVariable(bci2000,"feedback", new Func<int>(() => state.isFeedback ? 1 : 0)));
        setValues.Add("trueClass", new CustomSetVariable(bci2000,"trueClass", new Func<int>(() => (int)state.trueClassType)));
        setValues.Add("trialNum", new CustomSetVariable(bci2000,"trialNum", new Func<int>(() => state.trialNum)));
    }
    private void Update()
    {
        var state = GetComponent<TaskManager>().state;
        var bci2000 = GetComponent<UnityBCI2000>();
        var pc =  bci2000.GetState("predictClass");
        state.predictClassType = (TrialClassType)pc;
        foreach (var kvp in setValues)
        {
            kvp.Value.updatingFunc();
        }
    }
}
class CustomSetVariable
{
    string keyName;
    public CustomSetVariable(UnityBCI2000 bci2000,string keyName, Func<int> updatingFunc)
    {
        bci2000.AddState(keyName);
        this.keyName = keyName;
        this.updatingFunc = new Action(() => {
            var newValue = updatingFunc(); 
            if(newValue != prevValue)
            {
                bci2000.SetState(keyName,newValue);
                prevValue = newValue;
            }
        });
    }
    public Action updatingFunc;
    private int prevValue = -1;
}
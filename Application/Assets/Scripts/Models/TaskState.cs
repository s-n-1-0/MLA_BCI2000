using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public interface TaskStateInterface
{
    public bool isFeedback { get; set; }
    public TrialClassType trueClassType { get; set; }
    public int trialNum { get; set; }
    public TrialClassType predictClassType { get; }
}
[System.Serializable]
public class TaskState:TaskStateInterface
{
    public TaskState(UnityBCI2000 bci2000)
    {
        this.bci2000 = bci2000;
        this.trialNumVar =  new CustomSetVariable(bci2000, "trialNum");
        this.trueClassVar = new CustomSetVariable(bci2000, "trueClass");
        this.feedbackVar = new CustomSetVariable(bci2000, "feedback");
    }
    UnityBCI2000 bci2000;
    //---送信
    public bool isFeedback
    {
        get => _isFeedback;
        set
        {
            feedbackVar.Update(value && trueClassType != TrialClassType.None ? 1 : 0); //fb更新
            _isFeedback = value;
        }
    }//;
    private bool _isFeedback = false;
    public TrialClassType trueClassType
    {

        get => (TrialClassType)trueClassVar.value;
        set
        {
            feedbackVar.Update(_isFeedback && value != TrialClassType.None ? 1 : 0); //fb更新
            trueClassVar.Update((int)value);
        }
    }
    public int trialNum
    {
        set =>  trialNumVar.Update(value);
        get => trialNumVar.value;
    }

    private CustomSetVariable trialNumVar;
    private CustomSetVariable trueClassVar;
    private CustomSetVariable feedbackVar;
    //---受信
    public TrialClassType predictClassType {get
        {
            var pc = bci2000.GetState("predictClass");
            return (TrialClassType)pc;
        }
    }



}

public class DummyTaskState : TaskStateInterface
{
    public bool isFeedback { get; set; }
    public TrialClassType trueClassType { get; set; }
    public int trialNum { get; set; }

    public TrialClassType predictClassType { get => _predictClassType; }
    public TrialClassType _predictClassType;
}

class CustomSetVariable
{
    UnityBCI2000 bci2000;
    string keyName;
    public CustomSetVariable(UnityBCI2000 bci2000, string keyName)
    {
        bci2000.AddState(keyName);
        this.keyName = keyName;
        this.bci2000 = bci2000;
    }
    public void Update(int newValue)
    {
        if (newValue != value)
        {
            bci2000.SetState(keyName, newValue);
            value = newValue;
        }
    }
    public int value { get; private set; } = -1;
}

public enum TrialClassType
{
    None = 0,//Noneであれば推論しない
    Left = 1,
    Right =2
}
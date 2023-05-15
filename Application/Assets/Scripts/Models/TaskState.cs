using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class TaskState
{
    //---送信
    public bool isFeedback { get => trueClassType != TrialClassType.None; }
    public TrialClassType trueClassType = TrialClassType.None;
    public int trialNum = 0;

    //---受信
    public TrialClassType predictClassType = TrialClassType.None;

}
public enum TrialClassType
{
    None = 0,//Noneであれば推論しない
    Left = 1,
    Right =2
}
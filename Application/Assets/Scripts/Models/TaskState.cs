using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class TaskState
{
    public bool isFeedback { get => trueClassType != TrialClassType.None; }
    public TrialClassType predictClassType = TrialClassType.None;
    public TrialClassType trueClassType = TrialClassType.None; //Noneであれば推論しない

}
public enum TrialClassType
{
    None = 0,//Noneであれば推論しない
    Left = 1,
    Right =2
}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class BCI2000SettingsJson
{
    public string operatorPath,module1Name,module2Name,module3Name;
    public string[] module1Args = new string[0],module2Args = new string[0],module3Args = new string[0],commandsInProgDir;
    public int maxTrainTrialsNum, maxTestTrialsNum;
    public double jitterTimeRangeStart;
    public double jitterTimeRangeEnd;
    public double stimTrainTime,stimTestTime;
}

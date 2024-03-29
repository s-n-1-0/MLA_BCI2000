﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class BCIManager : MonoBehaviour
{
    public bool isReadJsonToThis = true;
    public bool isReadJsonToTaskManager = true;
    private void Awake()
    {
        string filePath = Application.streamingAssetsPath + "/BCISettings.json";
        StreamReader reader = new StreamReader(filePath);
        string json = reader.ReadToEnd();
        reader.Close();
        var bciSettings = JsonUtility.FromJson<BCI2000SettingsJson>(json);
        var bci = GetComponent<UnityBCI2000>();
        if (isReadJsonToThis)
        {
            bci.OperatorPath = bciSettings.operatorPath;
            bci.Module1 = bciSettings.module1Name;
            bci.Module2 = bciSettings.module2Name;
            bci.Module3 = bciSettings.module3Name;
            bci.Module1Args = bciSettings.module1Args;
            bci.Module2Args = bciSettings.module2Args;
            bci.Module3Args = bciSettings.module3Args;
            bci.initCommands = bciSettings.commandsInProgDir;
        }
        bci.enabled = true;

        if (isReadJsonToTaskManager)
        {
            var task = GetComponent<TaskManager>();
            task.maxTrainTrialsNum = bciSettings.maxTrainTrialsNum;
            task.maxTestTrialsNum = bciSettings.maxTestTrialsNum;
            task.stimTrainTime = (float)bciSettings.stimTrainTime;
            task.stimTestTime = (float)bciSettings.stimTestTime;
            task.jitterTimeRange = new float[] { (float)bciSettings.jitterTimeRangeStart, (float)bciSettings.jitterTimeRangeEnd };
        }

      
    }
    
}

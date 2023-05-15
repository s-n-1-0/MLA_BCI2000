using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class BCIManager : MonoBehaviour
{
    public GameObject bciSenderPrefab;
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
        bci.Module1Args = bciSettings.module1Args;
        bci.Module2Args = bciSettings.module2Args;
        bci.Module3Args = bciSettings.module3Args;
        bci.commandsInProgDir = bciSettings.commandsInProgDir;
        bci.enabled = true;
        var bciSender = Instantiate(bciSenderPrefab).GetComponent<BCI2000StateSender>();
        bciSender.name = bciSenderPrefab.name;
        bciSender.BCIObject = this.gameObject;
    }
    
}
